from django.contrib import admin

from .models import PhaseClass, PhaseLabel, PhaseView


class PhaseViewInline(admin.TabularInline):
    model = PhaseView
    extra = 0


@admin.register(PhaseClass)
class PhaseClassAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "value"]
    search_fields = ["uuid", "icid", "value"]
    list_filter = []
    inlines = [PhaseViewInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("views")


@admin.register(PhaseLabel)
class PhaseLabelAdmin(admin.ModelAdmin):
    list_display = ["uuid", "icid", "frame", "user", "phase_class"]
    search_fields = [
        "uuid",
        "icid",
        "frame__uuid",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phase_class__value",
    ]
    list_filter = ["user", "phase_class"]
    autocomplete_fields = [
        "frame",
        "user",
        "phase_class",
    ]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("frame", "user", "phase_class")
        )
