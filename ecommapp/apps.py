# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class EcommappConfig(AppConfig):
    name = 'ecommapp'  
    def ready(self):
        import elasticsearchapp.signals
