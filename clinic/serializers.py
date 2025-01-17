from rest_framework import serializers

from .models import Dicom, Frame, Media, Study


class StudySerializer(serializers.ModelSerializer):
    dicoms = serializers.SlugRelatedField(
        "uuid",
        many=True,
        read_only=True,
    )
    _number_of_dicoms = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Study
        fields = [
            "created_at",
            "dicoms",
            "_number_of_dicoms",
            "designation",
            "uuid",
        ]


class FrameSerializer(serializers.ModelSerializer):
    dicom = serializers.SlugRelatedField(
        "uuid",
        source="media.dicom",
        read_only=True,
    )
    dimensions = serializers.SerializerMethodField()

    class Meta:
        model = Frame
        fields = [
            "uuid",
            "created_at",
            "dicom",
            "file",
            "index",
            "dimensions",
        ]

    def get_dimensions(self, obj):
        return obj.dimensions


class MediaSerializer(serializers.ModelSerializer):

    # dicom = DicomSerializer()
    study = StudySerializer()

    class Meta:
        model = Media
        fields = ["id", "dicom", "file", "extension", "study"]


class DicomSerializer(serializers.ModelSerializer):
    media_type = serializers.SerializerMethodField()
    study = serializers.SlugRelatedField(
        "uuid",
        read_only=True,
    )

    def get_media_type(self, obj):
        return "Video" if obj.media and obj.media.ext == "mp4" else "Single Frame"

    class Meta:
        model = Dicom
        fields = [
            "created_at",
            "frames_per_second",
            "index",
            "media_type",
            "physical_delta_x",
            "physical_delta_y",
            "pixel_height",
            "pixel_width",
            "study",
            "type",
            "uuid",
        ]


class DicomRetrieveSerializer(serializers.ModelSerializer):
    frames = FrameSerializer(
        source="media.frames",
        read_only=True,
        many=True,
    )
    media = MediaSerializer(
        read_only=True,
    )

    class Meta:
        model = Dicom
        fields = [
            "created_at",
            "frames",
            "frames_per_second",
            "index",
            "media",
            "physical_delta_x",
            "physical_delta_y",
            "pixel_height",
            "pixel_width",
            "type",
            "uuid",
        ]
