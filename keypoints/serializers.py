from rest_framework import serializers

from phases.serializers import PhaseClassSerializer
from views.serializers import ViewClassSerializer

from .models import (
    KeypointClass,
    KeypointCollectionClass,
    KeypointCollectionLabel,
    KeypointLabel,
)


class KeypointCollectionClassSerializer(serializers.ModelSerializer):
    phase_classes = PhaseClassSerializer(
        read_only=True,
        many=True,
    )
    view_classes = ViewClassSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = KeypointCollectionClass
        fields = [
            "uuid",
            "value",
            "phase_classes",
            "view_classes",
        ]


class KeypointCollectionLabelSerializer(serializers.ModelSerializer):
    phase_class = serializers.SlugRelatedField(
        "value",
        read_only=True,
    )
    frame = serializers.SlugRelatedField(
        "uuid",
        read_only=True,
    )
    keypoint_collection_class = serializers.SlugRelatedField(
        "value",
        read_only=True,
    )

    class Meta:
        model = KeypointCollectionLabel
        fields = [
            "phase_class",
            "frame",
            "keypoint_collection_class",
            "user",
            "review_user",
            "accepted",
            "deny_reason",
            "updated_at",
            "uuid",
        ]


class KeypointClassSerializer(serializers.ModelSerializer):
    keypoint_pair = serializers.SlugRelatedField(read_only=True, slug_field="value")
    keypoint_collection_class = serializers.SlugRelatedField(
        read_only=True, slug_field="value"
    )

    class Meta:
        model = KeypointClass
        fields = [
            "id",
            "value",
            "keypoint_pair",
            "keypoint_collection_class",
            "order",
        ]


class KeypointLabelSerializer(serializers.ModelSerializer):
    keypoint_class = serializers.SlugRelatedField(read_only=True, slug_field="value")
    keypoint_collection = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = KeypointLabel
        fields = ["id", "keypoint_class", "keypoint_collection", "x", "y"]
