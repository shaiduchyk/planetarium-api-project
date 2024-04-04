from django.db import transaction
from rest_framework import serializers

from planetarium_service.models import (
    PlanetariumDome,
    ShowSession,
    ShowTheme,
    AstronomyShow,
    Reservation,
    Ticket,
)


class PlanetariumDomeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = ("id", "image")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = PlanetariumDome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "image",
            "capacity"
        )
        read_only_fields = ("image",)


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    planetarium_dome = serializers.SerializerMethodField()
    astronomy_show = serializers.SerializerMethodField()

    def get_astronomy_show(self, obj):
        return obj.astronomy_show.title

    def get_planetarium_dome(self, obj):
        return obj.planetarium_dome.name


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class ShowThemeListSerializer(ShowThemeSerializer):
    pass


class ShowThemeDetailSerializer(ShowThemeSerializer):
    pass


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes_names = serializers.SerializerMethodField()

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "themes_names")

    def get_themes_names(self, obj):
        return [theme.name for theme in obj.themes.all()]


class PlanetariumDomeDetailSerializer(PlanetariumDomeSerializer):
    pass


class TicketSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)

        row = data.get("row")
        seat = data.get("seat")
        show_session_id = data.get("show_session")

        if Ticket.objects.filter(row=row, seat=seat,
                                 show_session_id=show_session_id).exists():
            raise serializers.ValidationError("This seat is already occupied.")

        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session",
            "planetarium_dome",
            "reservation"
        )


class TicketListSerializer(TicketSerializer):
    show_session = serializers.SerializerMethodField()
    reservation = serializers.SerializerMethodField()

    def get_show_session(self, obj):
        return obj.show_session.astronomy_show.title

    def get_reservation(self, obj):
        return obj.reservation.user.username


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")

    def create(self, validated_data):
        reservations_data = [Reservation(**item) for item in validated_data]

        with transaction.atomic():
            reservations = Reservation.objects.bulk_create(reservations_data)

        return reservations


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ("id", "user", "tickets")

    def get_user(self, obj):
        return obj.user.username
