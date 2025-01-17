from rest_framework import serializers

from authorization.models import User
from clinic.models import Frame

from .models import PhaseClass, PhaseLabel, PhaseView


class PhaseClassSerializer(serializers.ModelSerializer):
    views = serializers.SlugRelatedField(
        slug_field="uuid",
        many=True,
        read_only=True,
    )

    class Meta:
        model = PhaseClass
        fields = ["id", "value", "view_classes", "views"]


class PhaseLabelSerializer(serializers.ModelSerializer):
    frame = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Frame.objects.all(),
    )
    user = serializers.SlugRelatedField(
        slug_field="id",
        queryset=User.objects.all(),
    )
    phase_class = serializers.SlugRelatedField(
        slug_field="value",
        queryset=PhaseClass.objects.all(),
    )

    class Meta:
        model = PhaseLabel
        fields = [
            "frame",
            "user",
            "phase_class",
        ]


class PhaseViewSerializer(serializers.ModelSerializer):
    phase_class = serializers.SlugRelatedField(read_only=True, slug_field="value")
    view_class = serializers.SlugRelatedField(read_only=True, slug_field="value")

    class Meta:
        model = PhaseView
        fields = ["id", "phase_class", "view_class"]
