import datetime
from haystack import indexes
from boots.models import Boot


class BootIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    slug = indexes.CharField(model_attr='slug')
    team_slug = indexes.CharField(model_attr='team__slug')
    team_email = indexes.CharField(model_attr='team__email')
    created = indexes.DateTimeField(model_attr='created')
    modified = indexes.DateTimeField(model_attr='modified')

    #type = indexes.FacetCharField(model_attr='type')
    #tags = indexes.FacetMultiValueField()

    def get_model(self):
        return Boot

    def index_queryset(self, using=None):
        return self.get_model().objects.all()