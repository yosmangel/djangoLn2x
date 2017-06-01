from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.forms import HiddenInput
from django.utils import translation
from django.http import HttpResponseNotFound

from datetime import datetime

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from unifypage.models import UnifyPage, MultilangKeyword
from unifypage.forms import ContactForm, process
from unifypage.views import unifypage as unifypage_view
from ln2xevents.models import EventPage, PageContent, CoursePage
from ln2xevents.filtermodels import EventPageFilter, CoursePageFilter

from el_pagination.decorators import page_template


@page_template(u"ln2xevents/listelems.html", key='entry_list')
def eventslist(request, slug, template=u"ln2xevents/events/eventslist.html",
        extra_context=None):
    events = EventPage.objects.exclude(course__isnull=True)
    if not request.user.has_perm('staff'):
        events = events.filter(status=CONTENT_STATUS_PUBLISHED)
    f = EventPageFilter(request.GET, queryset=events)
    events = events.filter(lang_code=request.LANGUAGE_CODE)
    nb_events = request.GET.get('elem_number', '4')
    thumb_view = request.GET.get('thumb_view', False)

    event_entry_list = f.qs
    list_elem_template = 'ln2xevents/events/eventslistelem.html'
    if thumb_view:
        list_elem_template = 'ln2xevents/events/eventslistelemthumb.html'
    if slug == 'events/browse':
        today = datetime.now().date()
        event_entry_list = event_entry_list.filter(end_date__gt=today)
    if slug == 'events/archive':
        today = datetime.now().date()
        event_entry_list = event_entry_list.filter(end_date__lt=today)
    if slug == 'events/email-schedule':
        today = datetime.now().date()
        event_entry_list = event_entry_list.filter(end_date__gt=today)
        list_elem_template = 'ln2xevents/events/emaileventslistelem.html'
    context = {
            'events': events,
            'filter': f,
            'list_elem_template': list_elem_template,
            'entry_list': event_entry_list,
            'nb_entry_values': [4, 10, 20, 100],
            'nb_entry': nb_events,
            }
    context.update(extra_context or {})
    if request.is_ajax():
        context['no_entry'] = PageContent.objects \
                        .filter(reference='NoEventFoundContent', \
                        lang_code=request.LANGUAGE_CODE) \
                        .first()
    return unifypage_view(request, slug, template, extra_context=context)


def eventpage(request, slug, subpage='', \
        template=u"ln2xevents/events/eventpage.html",extra_context=None):
    print(slug, subpage)
    events = EventPage.objects.filter(slug=slug)
    if not request.user.has_perm('staff'):
        events = events.filter(status=CONTENT_STATUS_PUBLISHED)
    event = events.first()

    if not event:
        events = EventPage.objects.filter(old_slugs__slug=slug)
        if not request.user.has_perm('staff'):
            events = events.filter(status=CONTENT_STATUS_PUBLISHED)
        event = events.first()
        if event:
            return redirect(event.get_absolute_url())
        else:
            return HttpResponseNotFound("This event does not exist")

    if not event.course:
        return HttpResponseNotFound("This event has no course")

    context = {
            'event': event,
            'editable_obj': event,
            'meta_title': event.title,
            'title': event.course.title,
            'header_title': event.course.title + ' - ' + event.city,
            'lang_code': event.lang_code,
            'course': event.course,
            'base_template': "ln2xevents/events/eventpage.html",
            }

    if subpage == '':
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                process(form)
            else:
                print('not valid')
        else:
            form = ContactForm()
        form.fields['course'].widget = HiddenInput()
        form.fields['event'].widget = HiddenInput()
        form.fields['event'].initial = event
        form.fields['course'].initial = event.course

        next_events = event.next_sessions()

        sponsors_types = event.types_sponsor_list()
        old_sponsors = None
        sponsors_content = event.sponsors_content()
        if not sponsors_types:
            old_sponsors = event.old_sponsor_list()
            sponsors_content = event.old_sponsors_content()

        specific_contents = {
                'who_attends_content': event.who_attends_content(),
                'testimonials_content': event.testimonials_content(),
                'agenda_content': event.agenda_content(),
                'trainers_content': event.trainers_content(),
                'sponsors_content': sponsors_content,
                'speakers_content': event.speakers_content(),
                'venue_content': event.venue_content(),
                'next_sessions_content': event.next_sessions_content(),
                'no_next_sessions_content': event.no_next_sessions_content(),
                }

        context.update({
                'form': form,
                'next_events': next_events,
                'next_sessions': event.next_sessions(),
                'keywords': event.keywords_list(),
                'imgbreaks': event.course.image_breakers_list_cycle(),
                'sponsors_types': sponsors_types,
                'old_sponsors': old_sponsors,
                'speakers': event.speakers_list(),
                'session_list': event.all_session_list(),
                'general_contents': event.general_contents(),
                'specific_contents': specific_contents,
                })
        if event.display_session_times:
            context.update({
                'session_list': event.confirmed_session_list(),
                })
        context.update(specific_contents)

    elif subpage == 'agenda':
        template = "ln2xevents/events/eventagendapage.html"
        context.update({
            'course_session_list': event.course_session_list(),
            'confirmed_session_list': event.confirmed_session_list(),
            'content': event.agenda_content(),
            })
    elif subpage == 'speakers':
        template = "ln2xevents/events/eventspeakerspage.html"
    elif subpage == 'sponsors':
        template = "ln2xevents/events/eventsponsorspage.html"
    else:
        return HttpResponseNotFound('The subpage ' + subpage +
                ' does not exist')
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)

@page_template(u"ln2xevents/listelems.html", key='entry_list')
def courseslist(request, slug, template=u"ln2xevents/courseslist.html",
        extra_context=None):
    courses = CoursePage.objects.all()
    if not request.user.has_perm('staff'):
        courses = courses.filter(status=CONTENT_STATUS_PUBLISHED)
    f = CoursePageFilter(request.GET, queryset=courses)
    courses = courses.filter(lang_code=request.LANGUAGE_CODE)
    nb_courses = request.GET.get('elem_number', '4')
    course_entry_list = f.qs
    if slug == 'courses/browse':
        today = datetime.now().date()
        course_entry_list = course_entry_list.filter(end_date__gt=today)
    context = {
            'courses': courses,
            'filter': f,
            'list_elem_template': 'ln2xevents/courseslistelem.html',
            'entry_list': course_entry_list,
            'nb_entry_values': [4, 10, 20, 100],
            'nb_entry': nb_courses,
            }
    context.update(extra_context or {})
    if request.is_ajax():
        context['no_entry'] = PageContent.objects \
                        .filter(reference='NoCourseFoundContent', \
                        lang_code=request.LANGUAGE_CODE) \
                        .first()
    return unifypage_view(request, slug, template, extra_context=context)

def coursepage(request, slug, subpage='', \
        template=u"ln2xevents/coursepage.html", extra_context=None):
    courses = CoursePage.objects.filter(slug=slug)
    if not request.user.has_perm('staff'):
        courses = courses.filter(status=CONTENT_STATUS_PUBLISHED)
    course = courses.first()

    if not course:
        courses = CoursePage.objects.filter(old_slugs__slug=slug)
        if not request.user.has_perm('staff'):
            courses = courses.filter(status=CONTENT_STATUS_PUBLISHED)
        course = courses.first()
        if course:
            return redirect(course.get_absolute_url())
        else:
            return HttpResponseNotFound("This course does not exist")

    context = {
            'course': course,
            'editable_obj': course,
            'meta_title': course.title,
            'title': course.title,
            'header_title': course.title,
            'base_template': "ln2xevents/coursepage.html",
            }

    if subpage == '':
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                process(form)
            else:
                print('not valid')
        else:
            form = ContactForm()
        form.fields['course'].widget = HiddenInput()
        form.fields['event'].widget = HiddenInput()
        form.fields['event'].initial = None
        form.fields['course'].initial = course

        next_events = course.next_sessions()

        specific_contents = {
                'who_attends_content': course.who_attends_content(),
                'testimonials_content': course.testimonials_content(),
                'agenda_content': course.agenda_content(),
                'trainers_content': course.trainers_content(),
                'sponsors_content': None,
                'speakers_content': course.speakers_content(),
                'venue_content': None,
                'next_sessions_content': course.next_sessions_content(),
                'no_next_sessions_content': course.no_next_sessions_content(),
                }

        context.update({
                'lang_code': course.lang_code,
                'course': course,
                'form': form,
                'next_events': next_events,
                'next_sessions': course.next_sessions(),
                'keywords': course.keywords_list(),
                'imgbreaks': course.image_breakers_list_cycle(),
                'sponsors_types': None,
                'speakers': course.speakers_list(),
                'session_list': course.all_session_list(),
                'general_contents': course.general_contents(),
                'specific_contents': specific_contents,
                })
        context.update(specific_contents)

    elif subpage == 'agenda':
        template = "ln2xevents/events/eventagendapage.html"
        context.update({
            'course_session_list': course.session_list(),
            'content': course.agenda_content(),
            })
    else:
        return HttpResponseNotFound('No subpage' + subpage)
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)
