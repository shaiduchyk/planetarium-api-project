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
        )
        read_only_fields = ("image",)


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description")


class PlanetariumDomeDetailSerializer(PlanetariumDomeSerializer):
    pass


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user")


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat", "show_session", "reservation")


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name")
