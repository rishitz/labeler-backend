from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from clinic.models import Frame
from labeler.rest_framework import viewsets
from phases.models import PhaseClass
from segmentations.filters import SegmentationLabelFilterSet
from segmentations.models import SegmentationClass, SegmentationLabel
from segmentations.serializers import (
    SegmentationClassSerializer,
    SegmentationLabelSerializer,
)


class SegmentationClassViewSet(viewsets.CamelCaseModelViewSet):

    queryset = (
        SegmentationClass.objects.all()
        .order_by("value")
        .prefetch_related("view_classes")
    )
    serializer_class = SegmentationClassSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["value"]
    http_method_names = ["get"]


class SegmentationLabelViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = [
        "get",
        "post",
    ]
    filterset_class = SegmentationLabelFilterSet
    serializer_class = SegmentationLabelSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    queryset = (
        SegmentationLabel.objects.all()
        .select_related(
            "phase_class",
            "segmentation_class",
            "frame__media__dicom",
        )
        .order_by(
            "-created_at",
        )
    )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Upsert endpoint for `SegmentationLabels`, the request body must include a list of `SegmentationLabel` objects
        with their respective `paths`, `SegmentationClass`, and `PhaseClass` values.
        Supports bulk updating for efficiency.
        """

        results = []
        data = request.data

        user = request.user
        frame_uuids = set([segmentation.get("frame") for segmentation in data])
        phase_class_values = set(
            [segmentation.get("phase_class") for segmentation in data]
        )
        segmentation_class_values = set(
            [segmentation.get("segmentation_class") for segmentation in data]
        )

        frames = Frame.objects.in_bulk(
            frame_uuids,
            field_name="uuid",
        )
        phase_classes = PhaseClass.objects.in_bulk(
            phase_class_values,
            field_name="value",
        )
        segmentation_classes = SegmentationClass.objects.in_bulk(
            segmentation_class_values,
            field_name="value",
        )

        segmentations = {}

        with transaction.atomic():
            for segmentation_payload in data:
                frame = frames.get(segmentation_payload["frame"])
                segmentation_class = segmentation_classes.get(
                    segmentation_payload["segmentation_class"]
                )
                phase_class = phase_classes.get(segmentation_payload.get("phase_class"))

                segmentation_label, _ = SegmentationLabel.objects.get_or_create(
                    user=user,
                    frame=frame,
                    segmentation_class=segmentation_class,
                )

                segmentation_label.phase_class = phase_class
                segmentation_label.paths = segmentation_payload.get("paths")
                segmentation_label.is_fully_visible = segmentation_payload[
                    "is_fully_visible"
                ]

                segmentations[(frame, segmentation_class, user)] = segmentation_label

            SegmentationLabel.objects.bulk_update(
                segmentations.values(),
                fields=[
                    "phase_class",
                    "paths",
                    "is_fully_visible",
                ],
            )

            for segmentation_payload in data:
                data_url = segmentation_payload.get("data_url")

                if not data_url:
                    continue

                frame = frames.get(segmentation_payload["frame"])
                segmentation_class = segmentation_classes.get(
                    segmentation_payload["segmentation_class"]
                )
                segmentation = segmentations[(frame, segmentation_class, user)]
                segmentation.extension = "png"
                segmentation.save_bytes(data_url)

        results = self.serializer_class(
            segmentations.values(),
            many=True,
        ).data

        response = Response(
            results,
            status=HTTP_201_CREATED,
        )

        return response
