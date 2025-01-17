from django.contrib import admin

from .models import SegmentationClass, SegmentationLabel


@admin.register(SegmentationClass)
class SegmentationClassAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "value",
    ]
    search_fields = [
        "uuid",
        "value",
    ]


@admin.register(SegmentationLabel)
class SegmentationLabelAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "user",
        "frame",
        "segmentation_class",
        "cardiac_cycle_phase",
        "file",
    ]
    search_fields = [
        "uuid",
        "icid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "frame__uuid",
        "segmentation_class__value",
        "cardiac_cycle_phase__value",
    ]
    list_filter = [
        "user",
        "segmentation_class",
        "cardiac_cycle_phase",
    ]
    autocomplete_fields = [
        "user",
        "frame",
        "segmentation_class",
        "cardiac_cycle_phase",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "user",
                "frame",
                "segmentation_class",
                "quality_label",
                "cardiac_cycle_phase",
                "review_user",
            )
        )
