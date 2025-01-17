from rest_framework import serializers

from clinic.models import Dicom
from views.models import ViewClass, ViewLabel


class ViewClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewClass
        fields = [
            "created_at",
            "media_type",
            "type",
            "uuid",
            "view",
            "window",
        ]


class ViewLabelSerializer(serializers.ModelSerializer):
    dicom = serializers.SlugRelatedField(
        "uuid",
        read_only=True,
    )
    view_class = serializers.SlugRelatedField(
        "uuid",
        read_only=True,
    )

    class Meta:
        model = ViewLabel
        fields = [
            "created_at",
            "dicom",
            "uuid",
            "view_class",
        ]

    def create(self, validated_data):
        dicom = Dicom.objects.get(uuid=self.initial_data["dicom"])
        user = self.context["request"].user
        view_class = ViewClass.objects.filter(
            uuid=self.initial_data.get("view_class")
        ).first()

        view_label, _ = ViewLabel.objects.get_or_create(
            user=user,
            dicom=dicom,
        )

        view_label.view_class = view_class
        view_label.save()

        return view_label
