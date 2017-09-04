# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import BaseCategory

class HomeView(ListView):
    model=BaseCategory
    context_object_name = 'base_category'
    


# Create your views here.
