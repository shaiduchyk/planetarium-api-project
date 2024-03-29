import pathlib
import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from rest_framework.exceptions import ValidationError


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups"
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions'
    )


def movie_image_path(instance, filename) -> pathlib.Path:
    filename = (f"slugify {instance.name}-{uuid.uuid4()}"
                + pathlib.Path(filename).suffix)
    return pathlib.Path("uploads/planetariums/") / pathlib.Path(filename)


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    image = models.ImageField(upload_to=movie_image_path, null=True)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=63)
    themes = models.ManyToManyField(ShowTheme)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE
    )
    show_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.astronomy_show.title)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="reservations"
    )

    def __str__(self):
        return f"{self.created_at} - {self.user}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for (ticket_attr_value,
             ticket_attr_name,
             planetarium_dome_attr_name) in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome,
                                  planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name:
                            f"{ticket_attr_name} "
                            f"number must be in available range: "
                            f"(1, {planetarium_dome_attr_name}): "
                            f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (f"Ticket: {self.id},"
                f"(row: {self.row}, seat: {self.seat})."
                f"Session info: {self.show_session}\n")

    class Meta:
        unique_together = (
            "show_session", "reservation", "row", "seat"
        )
        ordering = ("row", "seat")
