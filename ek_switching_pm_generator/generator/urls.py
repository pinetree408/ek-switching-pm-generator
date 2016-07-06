# coding: utf-8
from django.conf.urls import patterns, url
import generator.views as views

urlpatterns = patterns('',
    url(
        regex=r'^generator/$',
        view=views.GeneratorView.as_view(),
        name='generator',
    ),
)
