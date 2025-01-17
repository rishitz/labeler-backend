from django.contrib import admin

from clinic.models import Dicom, Frame, Media, Study


@admin.register(Dicom)
class DicomAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "manufacturer",
        "type",
        "number_of_frames",
    ]
    search_fields = [
        "uuid",
        "icid",
        "manufacturer",
    ]
    list_filter = [
        "manufacturer",
        "type",
    ]
    autocomplete_fields = ["study"]


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "index",
        "file",
    ]
    search_fields = [
        "uuid",
        "icid",
        "index",
        "dicom__uuid",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("media__dicom")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "dicom",
        "extension",
        "file",
    ]
    search_fields = [
        "uuid",
        "icid",
        "file",
        "dicom__manufacturer",
        "dicom__uuid",
        "dicom__study__uuid",
    ]
    list_filter = [
        "extension",
    ]
    autocomplete_fields = ["dicom"]


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "number_of_dicoms",
        "number_of_usable_dicoms",
        "designation",
    ]
    search_fields = [
        "uuid",
        "icid",
        "dicoms__manufacturer",
    ]
    list_filter = [
        "created_at",
        "dicoms__manufacturer",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("dicoms")
