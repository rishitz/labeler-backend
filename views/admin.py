from django.contrib import admin

from .models import ViewClass, ViewLabel


@admin.register(ViewClass)
class ViewClassAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "media_type", "type", "window", "view"]
    search_fields = [
        "uuid",
        "icid",
        "media_type",
        "type",
        "window",
        "view",
    ]
    list_filter = [
        "media_type",
        "type",
        "window",
        "view",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request)


@admin.register(ViewLabel)
class ViewLabelAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "icid",
        "user",
        "dicom",
        "view_class",
    ]
    search_fields = [
        "uuid",
        "icid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "dicom__uuid",
        "dicom__study__uuid",
        "view_class__window",
        "view_class__view",
    ]
    list_filter = [
        "user",
        "view_class",
    ]
    autocomplete_fields = [
        "user",
        "dicom",
        "view_class",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "user",
                "dicom",
                "view_class",
            )
        )
