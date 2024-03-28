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
