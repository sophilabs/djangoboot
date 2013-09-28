from django.conf.urls import patterns
from django.views.generic import TemplateView

from accounts.views import GroupCreateView, GroupUpdateView, GroupDeleteView


urlpatterns = patterns('',
    (r'^group/create', GroupCreateView.as_view(template_name='<template>')),
    (r'^group/(?P<slug>[\w-]+)/update', GroupUpdateView.as_view(template_name='<template>')),
    (r'^group/(?P<slug>[\w-]+)/delete', GroupDeleteView.as_view(template_name='<template>')),
)