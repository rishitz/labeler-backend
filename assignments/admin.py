from django.contrib import admin

from .models import DicomLabelingJob, FullStudyAnnotationSet, StudyLabelingJob


@admin.register(FullStudyAnnotationSet)
class FullStudyAnnotationSetAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "name", "user"]
    search_fields = [
        "uuid",
        "icid",
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    autocomplete_fields = ["user"]
    list_filter = ["user"]


@admin.register(StudyLabelingJob)
class StudyLabelingJobAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "study", "user", "annotation_set"]
    search_fields = [
        "uuid",
        "icid",
        "study__uuid",
        "study__foreign_id",
        "user__email",
        "user__first_name",
        "user__last_name",
        "annotation_set__name",
    ]
    autocomplete_fields = ["study", "user", "annotation_set"]
    list_filter = ["user", "study", "annotation_set"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("study", "user", "annotation_set")
        )


@admin.register(DicomLabelingJob)
class DicomLabelingJobAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "dicom",
        "user",
        "study_labeling_job",
        "annotation_set",
    ]
    search_fields = [
        "uuid",
        "icid",
        "dicom__uuid",
        "dicom__study__uuid",
        "dicom__manufacturer",
        "user__email",
        "user__first_name",
        "user__last_name",
        "annotation_set__name",
        "study_labeling_job__uuid",
    ]
    list_filter = ["user", "dicom", "study_labeling_job", "annotation_set"]
    autocomplete_fields = ["dicom", "user", "study_labeling_job", "annotation_set"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("dicom", "user", "study_labeling_job", "annotation_set")
        )
