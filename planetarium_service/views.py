from django.contrib.admin import actions
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from planetarium_service.models import (
    PlanetariumDome,
    ShowSession,
    ShowTheme,
    AstronomyShow,
    Reservation,
    Ticket,
)
from planetarium_service.serializers import (
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowThemeSerializer,
    AstronomyShowSerializer,
    ReservationSerializer,
    TicketSerializer,
    PlanetariumDomeImageSerializer, PlanetariumDomeDetailSerializer
)


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image"
    )
    def upload_image(self, request, pk=None):
        planetarium_dome = self.get_object()
        serializer = self.get_serializer(planetarium_dome, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeSerializer
        if self.action == "retrieve":
            return PlanetariumDomeDetailSerializer
        if self.action == "upload_image":
            return PlanetariumDomeImageSerializer

        return PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
