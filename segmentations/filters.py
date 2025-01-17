from django_filters import FilterSet

from segmentations.models import SegmentationLabel


class SegmentationLabelFilterSet(FilterSet):
    class Meta:
        model = SegmentationLabel
        fields = {
            # "segmentation_class__uuid": ["in"],
            "frame__media__dicom__uuid": ["exact"],
            "frame__media__dicom__study__uuid": ["exact"],
            "frame__uuid": ["in"],
        }
