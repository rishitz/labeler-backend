from django.db import transaction
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from clinic.models import Frame
from keypoints.models import (
    KeypointClass,
    KeypointCollectionClass,
    KeypointCollectionLabel,
    KeypointLabel,
)
from labeler.rest_framework import viewsets
from phases.models import PhaseClass

from .serializers import (
    KeypointClassSerializer,
    KeypointCollectionClassSerializer,
    KeypointCollectionLabelSerializer,
    KeypointLabelSerializer,
)


class KeypointCollectionClassViewSet(viewsets.CamelCaseModelViewSet):
    queryset = (
        KeypointCollectionClass.objects.all()
        .order_by("value")
        .prefetch_related("view_classes", "phase_classes")
    )
    serializer_class = KeypointCollectionClassSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["value"]
    http_method_names = ["get"]


class KeypointCollectionLabelViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]
    serializer_class = KeypointCollectionLabelSerializer

    queryset = (
        KeypointCollectionLabel.objects.all()
        .order_by(
            "keypoint_collection_class__value",
            "user__username",
        )
        .select_related(
            "cardiac_cycle_phase",
            "frame",
            "keypoint_collection_class",
            "user",
        )
        .prefetch_related(
            Prefetch(
                "keypoints",
                queryset=KeypointLabel.objects.select_related(
                    "keypoint_class__keypoint_pair",
                ).order_by(
                    "keypoint_class__order",
                ),
            ),
        )
    )

    filterset_fields = {
        "frame__media__dicom__uuid": ["exact"],
        "frame__media__dicom__study__uuid": ["exact"],
        "frame__uuid": ["in"],
        "keypoint_collection_class__uuid": ["exact"],
    }

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Upsert endpoint for `KeypointCollectionLabel`, the request body must include a list of
        `KeypointCollectionLabel` objects with their respective `KeypointLabel` and `PhaseClass` values.
        This endpoint supports bulk updating for efficiency.
        """
        results = []
        data = request.data

        user = request.user
        frame_uuids = set(
            [keypoint_collection.get("frame") for keypoint_collection in data]
        )
        cardiac_cycle_phase_values = set(
            [
                keypoint_collection.get("cardiac_cycle_phase")
                for keypoint_collection in data
            ]
        )
        keypoint_collection_class_values = set(
            [
                keypoint_collection.get("keypoint_collection_class")
                for keypoint_collection in data
            ]
        )
        keypoint_class_uuids = set(
            [
                keypoint["keypoint_class_uuid"]
                for collection in data
                for keypoint in collection.get("keypoints", [])
            ]
        )

        frames = Frame.objects.in_bulk(
            frame_uuids,
            field_name="uuid",
        )
        cardiac_cycle_phases = PhaseClass.objects.in_bulk(
            cardiac_cycle_phase_values,
            field_name="value",
        )
        keypoint_collection_classes = KeypointCollectionClass.objects.in_bulk(
            keypoint_collection_class_values,
            field_name="value",
        )
        keypoint_classes = KeypointLabel.objects.in_bulk(
            keypoint_class_uuids,
            field_name="uuid",
        )

        keypoint_data = [
            {
                **keypoint,
                "keypoint_class": keypoint_classes[keypoint["keypoint_class_uuid"]],
                "keypoint_collection_class": keypoint_collection_classes[
                    collection["keypoint_collection_class"]
                ],
                "frame": frames[collection["frame"]],
            }
            for collection in data
            for keypoint in collection.get("keypoints", [])
        ]

        with transaction.atomic():

            keypoint_collections = {}

            for keypoint_collection_payload in data:
                frame = frames.get(keypoint_collection_payload["frame"])
                keypoint_collection_class = keypoint_collection_classes.get(
                    keypoint_collection_payload["keypoint_collection_class"]
                )
                cardiac_cycle_phase = cardiac_cycle_phases.get(
                    keypoint_collection_payload.get("cardiac_cycle_phase")
                )

                keypoint_collection, _ = KeypointCollectionLabel.objects.get_or_create(
                    user=user,
                    frame=frame,
                    keypoint_collection_class=keypoint_collection_class,
                )

                keypoint_collection.cardiac_cycle_phase = cardiac_cycle_phase

                keypoint_collections[(user, frame, keypoint_collection_class)] = (
                    keypoint_collection
                )

            KeypointCollectionLabel.objects.bulk_update(
                keypoint_collections.values(),
                fields=["cardiac_cycle_phase"],
            )

            keypoints = []

            for keypoint_payload in keypoint_data:
                keypoint_collection = keypoint_collections.get(
                    (
                        user,
                        keypoint_payload["frame"],
                        keypoint_payload["keypoint_collection_class"],
                    )
                )
                keypoint_class = keypoint_payload.get("keypoint_class")

                keypoint, _ = KeypointLabel.objects.get_or_create(
                    keypoint_class=keypoint_class,
                    keypoint_collection=keypoint_collection,
                )

                keypoint.x = keypoint_payload["x"]
                keypoint.y = keypoint_payload["y"]

                keypoints.append(keypoint)

            KeypointLabel.objects.bulk_update(
                keypoints,
                fields=["x", "y"],
            )

        results = self.serializer_class(
            keypoint_collections.values(),
            many=True,
        ).data

        response = Response(
            results,
            status=HTTP_201_CREATED,
        )

        return response


class KeypointClassViewSet(viewsets.CamelCaseModelViewSet):
    queryset = KeypointClass.objects.prefetch_related(
        "keypoint_pair", "keypoint_collection_class"
    ).all()
    serializer_class = KeypointClassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["value", "keypoint_collection_class__value"]


class KeypointLabelViewSet(viewsets.CamelCaseModelViewSet):
    queryset = KeypointLabel.objects.prefetch_related(
        "keypoint_class", "keypoint_collection"
    ).all()
    serializer_class = KeypointLabelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["keypoint_class__value", "keypoint_collection__id"]
