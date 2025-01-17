from django.contrib import admin

from .models import (
    KeypointClass,
    KeypointCollectionClass,
    KeypointCollectionLabel,
    KeypointLabel,
)


class ViewClassInline(admin.TabularInline):
    model = KeypointCollectionClass.view_classes.through
    extra = 0
    verbose_name = "View Class"
    verbose_name_plural = "View Classes"


class PhaseClassInline(admin.TabularInline):
    model = KeypointCollectionClass.phase_classes.through
    extra = 0
    verbose_name = "Phase Class"
    verbose_name_plural = "Phase Classes"


@admin.register(KeypointCollectionClass)
class KeypointCollectionClassAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "value"]
    search_fields = ["uuid", "icid", "value"]
    exclude = ["view_classes", "phase_classes"]
    inlines = [ViewClassInline, PhaseClassInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("view_classes", "phase_classes")
        )


@admin.register(KeypointCollectionLabel)
class KeypointCollectionLabelAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "user",
        "frame",
        "cardiac_cycle_phase",
        "keypoint_collection_class",
    ]
    search_fields = [
        "uuid",
        "icid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "frame__uuid",
        "cardiac_cycle_phase__value",
        "keypoint_collection_class__value",
    ]
    list_filter = [
        "user",
        "keypoint_collection_class",
    ]
    autocomplete_fields = [
        "user",
        "frame",
        "cardiac_cycle_phase",
        "keypoint_collection_class",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "user",
                "frame",
                "cardiac_cycle_phase",
                "keypoint_collection_class",
                "review_user",
            )
        )


@admin.register(KeypointClass)
class KeypointClassAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "value",
        "keypoint_collection_class",
        "keypoint_pair",
        "order",
    ]
    search_fields = [
        "uuid",
        "icid",
        "value",
        "keypoint_collection_class__value",
        "keypoint_pair__value",
    ]
    list_filter = [
        "keypoint_collection_class",
    ]
    autocomplete_fields = [
        "keypoint_collection_class",
        "keypoint_pair",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("keypoint_pair", "keypoint_collection_class")
        )


@admin.register(KeypointLabel)
class KeypointLabelAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "keypoint_class",
        "keypoint_collection",
        "x",
        "y",
    ]
    search_fields = [
        "uuid",
        "icid",
        "keypoint_class__value",
        "keypoint_collection__uuid",
        "keypoint_collection__user__email",
    ]
    list_filter = [
        "keypoint_class",
        "keypoint_collection",
    ]
    autocomplete_fields = [
        "keypoint_class",
        "keypoint_collection",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("keypoint_class", "keypoint_collection")
        )
