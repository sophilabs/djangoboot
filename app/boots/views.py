from django.views.generic import TemplateView


class SearchView(TemplateView):
    template_name = 'boots/search.html'


class TrendingView(TemplateView):
    template_name = 'boots/trending.html'


class GroupView(TemplateView):
    template_name = 'boots/group.html'


class BootView(TemplateView):
    template_name = 'boots/boot.html'


class VersionView(TemplateView):
    template_name = 'boots/version.html'