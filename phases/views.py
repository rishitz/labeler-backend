from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clinic.models import Frame
from labeler.rest_framework import viewsets

from .models import PhaseClass, PhaseLabel, PhaseView
from .serializers import PhaseClassSerializer, PhaseLabelSerializer, PhaseViewSerializer


class PhaseClassViewSet(viewsets.CamelCaseModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    queryset = PhaseClass.objects.all().order_by("value").prefetch_related("views")
    serializer_class = PhaseClassSerializer


class PhaseLabelViewSet(viewsets.CamelCaseModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PhaseLabelSerializer
    queryset = (
        PhaseLabel.objects.all()
        .select_related("frame", "user", "phase_class")
        .order_by("-id")
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "frame__uuid": ["exact"],
        "phase_class__value": ["exact"],
    }
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        instances = []

        for phase_data in request.data:
            phase_class = PhaseClass.objects.get(value=phase_data["phase"])
            frame = Frame.objects.get(uuid=phase_data["frame"])
            user = request.user

            phase_label, _ = PhaseLabel.objects.get_or_create(
                user=user,
                frame=frame,
                phase_class=phase_class,
            )
            instances.append(phase_label)

        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhaseViewViewSet(viewsets.CamelCaseModelViewSet):
    queryset = PhaseView.objects.select_related("phase_class", "view_class").all()
    serializer_class = PhaseViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["phase_class__value", "view_class__value"]
