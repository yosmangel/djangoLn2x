from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.conf import settings

from django_filters import rest_framework as filters

from ln2xevents.models import EventPage, CoursePage, PageContent, \
LEVELS, REGIONFILTER

from crispy_forms.helper import FormHelper

from datetime import datetime

from unifypage.models import MultilangKeyword

class EventPageFilter(filters.FilterSet):
    lang_code = filters.MultipleChoiceFilter(name='lang_code', \
            lookup_expr='exact', choices=settings.LANGUAGES, \
            widget=forms.CheckboxSelectMultiple, initial='en', \
            label=_('Language'))
    keywords = filters.ModelMultipleChoiceFilter(
            name='course__multilang_keywords',
            queryset=MultilangKeyword.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            label=_('Keywords'))
    level = filters.MultipleChoiceFilter(name='course__level', \
            lookup_expr='exact', choices=LEVELS, \
            widget=forms.CheckboxSelectMultiple, \
            label=_('Level'))
    delivery_method = filters.MultipleChoiceFilter(name='course__delivery_format', \
            lookup_expr='exact',\
            choices= [ (key,cat) for key,cat in CoursePage.DELIVERY_FORMAT if key != 'e-Learning'], \
            widget=forms.CheckboxSelectMultiple, \
            label=_('Delivery Method'))
    region = filters.MultipleChoiceFilter(name='macro_region', \
            lookup_expr='exact', choices=REGIONFILTER, \
            widget=forms.CheckboxSelectMultiple, \
            label=_('Regions'))
    o = filters.OrderingFilter(
            choices=(
                ('start date', _('Start date')),
                ('course', _('Course')),
                ),
            fields={
                'start_date': 'start date',
                'course__title': 'course',
                },
            initial= 'start date',
            help_text=''
            )

    class Meta:
        model = EventPage
        fields = {
                }

class CoursePageFilter(filters.FilterSet):
    lang_code = filters.MultipleChoiceFilter(name='lang_code', \
            lookup_expr='exact', choices=settings.LANGUAGES, \
            widget=forms.CheckboxSelectMultiple, initial='en', \
            label=_('Language'))
    keywords = filters.ModelMultipleChoiceFilter(
            name='multilang_keywords',
            queryset=MultilangKeyword.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            label=_('Keywords'))
    level = filters.MultipleChoiceFilter(name='level', \
            lookup_expr='exact', choices=LEVELS, \
            widget=forms.CheckboxSelectMultiple, \
            label=_('Level'))
    delivery_method = filters.MultipleChoiceFilter(name='delivery_format', \
            lookup_expr='exact', choices=CoursePage.DELIVERY_FORMAT, \
            widget=forms.CheckboxSelectMultiple, \
            label=_('Delivery Method'))
    o = filters.OrderingFilter(
            choices=(
                ('title', _('Title')),
                ),
            fields={
                'title': 'title',
                },
            initial= 'title',
            help_text=''
            )

    class Meta:
        model = CoursePage
        fields = {
                }

