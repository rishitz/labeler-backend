import django_filters

from clinic.models import Dicom, Frame


class DicomFilter(django_filters.FilterSet):
    study = django_filters.CharFilter(
        method="filter_study",
        required=True,
    )

    def filter_study(self, queryset, name, value):
        return queryset.filter(
            study__uuid=value,
        )

    class Meta:
        model = Dicom
        fields = {}


class FrameFilter(django_filters.FilterSet):
    study = django_filters.CharFilter(
        method="filter_study",
        required=True,
    )

    def filter_study(self, queryset, name, value):
        return queryset.filter(
            media__dicom__study__uuid=value,
        )

    class Meta:
        model = Frame
        fields = {}
