from django.contrib import admin

from .models import QualityLabel


@admin.register(QualityLabel)
class QualityLabelAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "user", "dicom", "quality_class"]
    search_fields = [
        "uuid",
        "icid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "dicom__uuid",
        "dicom__study__uuid",
    ]
    list_filter = ["user", "quality_class"]
    autocomplete_fields = [
        "dicom",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "dicom")
