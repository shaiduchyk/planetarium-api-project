from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    class Meta:
        model = ShowSession
        fields = ("id", "planetarium_dome", "astronomy_show", "show_time")

    def get_astronomy_show(self, obj):
        return obj.astronomy_show.title

    def get_planetarium_dome(self, obj):
        return obj.planetarium_dome.name


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("name",)


class ShowThemeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class ShowThemeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("id", "name")


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

    class Meta:
        model = PlanetariumDome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "image",
        )


class TicketSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)

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
        fields = ("id", "row", "seat", "show_session", "planetarium_dome")


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer(many=False, read_only=True)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        reservation = Reservation.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(reservation=reservation, **ticket_data)
        return reservation
