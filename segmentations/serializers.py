from rest_framework import serializers

from phases.models import PhaseClass
from segmentations.models import SegmentationClass, SegmentationLabel


class SegmentationClassSerializer(serializers.ModelSerializer):
    view_classes = serializers.SlugRelatedField("uuid", many=True, read_only=True)

    class Meta:
        model = SegmentationClass
        fields = [
            "uuid",
            "value",
            "view_classes",
        ]


class SegmentationLabelSerializer(serializers.ModelSerializer):
    phase_class = serializers.SlugRelatedField(
        "value",
        queryset=PhaseClass.objects.all(),
    )
    dicom = serializers.SlugRelatedField(
        "uuid",
        source="frame.media.dicom",
        read_only=True,
    )
    segmentation_class = serializers.SlugRelatedField(
        "value",
        read_only=True,
    )
    frame = serializers.SlugRelatedField(
        "uuid",
        read_only=True,
    )
    frame_index = serializers.IntegerField(
        source="frame.index",
        read_only=True,
    )

    class Meta:
        model = SegmentationLabel
        fields = [
            "phase_class",
            "created_at",
            "dicom",
            "segmentation_class",
            "file",
            "frame",
            "frame_index",
            "is_fully_visible",
            "paths",
            "uuid",
        ]
