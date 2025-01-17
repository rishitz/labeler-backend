from rest_framework import serializers

from authorization.serializers import UserSerializer
from clinic.models import Dicom
from clinic.serializers import StudySerializer

from .models import DicomLabelingJob, FullStudyAnnotationSet, StudyLabelingJob


class FullStudyAnnotationSetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FullStudyAnnotationSet
        fields = ["id", "name", "user"]


class StudyLabelingJobSerializer(serializers.ModelSerializer):
    study = StudySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    annotation_set = FullStudyAnnotationSetSerializer(read_only=True)

    class Meta:
        model = StudyLabelingJob
        fields = ["id", "study", "user", "annotation_set"]


class DicomLabelingJobSerializer(serializers.ModelSerializer):
    annotation_set = serializers.SlugRelatedField(
        slug_field="id",
        queryset=FullStudyAnnotationSet.objects.all(),
    )
    dicom = serializers.SlugRelatedField(
        slug_field="uuid",
        queryset=Dicom.objects.all(),
    )

    class Meta:
        model = DicomLabelingJob
        fields = [
            "annotation_set",
            "dicom",
            "user",
            "study_labeling_job",
        ]

    def create(self, validated_data):
        annotation_set = FullStudyAnnotationSet.objects.get(
            id=self.initial_data["annotation_set"]
        )
        dicom = Dicom.objects.get(uuid=self.initial_data["dicom"])
        user = self.context["request"].user
        study_labeling_job = validated_data["study_labeling_job"]

        dicom_labeling_job, created = DicomLabelingJob.objects.get_or_create(
            annotation_set=annotation_set,
            dicom=dicom,
            user=user,
            study_labeling_job=study_labeling_job,
        )
        return dicom_labeling_job
