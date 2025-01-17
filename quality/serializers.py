from rest_framework import serializers

from authorization.models import User
from clinic.models import Dicom
from quality.models import QualityLabel


class QualityLabelSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="email", queryset=User.objects.all())
    dicom = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Dicom.objects.all()
    )
    quality_class = serializers.ChoiceField(
        choices=QualityLabel.quality_class.field.choices
    )

    def validate(self, attrs):
        if QualityLabel.objects.filter(
            user=attrs["user"], dicom=attrs["dicom"]
        ).exists():
            raise serializers.ValidationError(
                "Duplicate quality label for this user and dicom."
            )
        return attrs

    class Meta:
        model = QualityLabel
        fields = ["id", "user", "dicom", "quality_class"]
