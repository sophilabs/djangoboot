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
    star_count = indexes.IntegerField(model_attr='star_count')
    star_count_day = indexes.IntegerField(model_attr='star_count_day')
    star_count_week = indexes.IntegerField(model_attr='star_count_week')
    star_count_month = indexes.IntegerField(model_attr='star_count_month')

    #type = indexes.FacetCharField(model_attr='type')
    #tags = indexes.FacetMultiValueField()

    def get_model(self):
        return Boot

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def load_all_queryset(self):
        return super(BootIndex, self).load_all_queryset().select_related('team', 'tags')