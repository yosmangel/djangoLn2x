from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings

import datetime
from itertools import chain, cycle
from babel.dates import format_date

from mezzanine.core.fields import RichTextField
from mezzanine.generic.fields import KeywordsField
from mezzanine.core.models import Displayable, Orderable
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.utils.urls import admin_url
from mezzanine.core.managers import DisplayableManager

from djmoney.models.fields import MoneyField

from unifypage.models import MultilangKeyword

LEVELS = (
    ('advanced', _('Expert')),
    ('mid-level', _('Professional')),
    ('basic', _('Introductory'))
)

REGIONFILTER = (
        ('ASIA', _('Asia')),
        ('EMEA', _('Europe, the Middle East and Africa')),
        ('LATAM', _('Latin America')),
        ('North America', _('North America')),
        ('Oceania', _('Oceania')),
        ('The Caribbean', _('The Caribbean')),
        ('Other', _('Other')),
        )

class SalesforceSynced(models.Model):
    """
    Abstract model for objects synced with SalesForce
    """
    salesforce_id = models.CharField(unique=True, max_length=18, null=True)
    last_sync = models.DateTimeField(_("Last Sync"),
            default=timezone.now, blank=True, null=True)

    class Meta:
        abstract = True

class CoursePage(SalesforceSynced, Displayable):
    """
    The model for the page corresponding to a Salesforce Course, with extra
    fields for the page
    """
    DELIVERY_FORMAT = (
            ('Conference', _('Conference')),
            ('Seminar', _('Seminar')),
            ('Training', _('Training')),
            ('e-Learning', _('e-Learning')),
            )
    SUBJECT_CATEGORIES = (
            ('Payment System Security, Risk & Compliance',
                _('Payment System Security, Risk & Compliance')),
            ('Payment System Management',
                _('Payment System Management')),
            ('Information Security and Privacy',
                _('Information Security and Privacy')),
            ('Secure Coding & Testing',
                _('Secure Coding & Testing')),
            )
    COURSE_LEVEL = (
            ('Advanced', _('Advanced')),
            ('Foundation', _('Foundation')),
            ('Professional', _('Professional')),
            )


    delivery_format = models.CharField(_("Delivery Format"), max_length=50,
            choices=DELIVERY_FORMAT, blank=True, null=True)
    lang_code = models.CharField(_("Language code"), max_length=2, default="en")
    banner = models.URLField(_("Banner"), blank=True, null=True, max_length=500)
    thumb = models.URLField(_("Thumb"), blank=True, null=True, max_length=500)
    level = models.CharField(_("Level"), max_length=15, \
            choices=LEVELS, default='basic')
    subject_category = models.CharField(_("Subject Category"), max_length=255,
            choices=SUBJECT_CATEGORIES, blank=True, null=True)
    duration = models.IntegerField(_("Duration(min)"), blank=True, null=True)
    agenda = RichTextField(_("Agenda"), blank=True, null=True)
    who_attends = models.CharField(_("Who Attends"), max_length=255,
            blank=True, null=True)
    objectives = RichTextField(_("Objectives"), blank=True, null=True)
    pre_requisites = RichTextField(_("Pre-requisites"), blank=True, null=True)
    ref_source = models.CharField(_("Ref/Source"), max_length=255,
            blank=True, null=True)
    languages_availables = models.CharField(_("Languages Availables"),
            max_length=255, blank=True, null=True)
    course_level = models.CharField(_("Course Level"), max_length=50,
            choices=COURSE_LEVEL, blank=True, null=True)


    target_delegates = models.IntegerField(_("Target Delegates"), default=0)

    multilang_keywords = models.ManyToManyField(MultilangKeyword, \
            related_name='course_pages', blank=True)

    product_reference = models.CharField(max_length=18, null=True)

    def is_published(self):
        return self.status == CONTENT_STATUS_PUBLISHED

    def keywords_list(self):
        return list(self.multilang_keywords.all().order_by('word'))

    class Meta:
        verbose_name = _("Course Page")
        verbose_name_plural = _("Course Pages")
        ordering = ['title',]

    def next_sessions(self):
        nextSessions = EventPage.objects.are_not_past()
        nextSessions = nextSessions.filter(course__lang_code=get_language()).order_by('course__subject_category')
        nextSessions = sorted(list(nextSessions),
                key = lambda event: (event.course != self, event.start_date))
        return nextSessions

    def session_list(self):
        return list(
                self.sessions.filter(published=True).order_by('slot_number')
                )

    def image_breakers_list_cycle(self):
        query = self.image_breakers.all()
        if query:
            l = []
            for img in query:
                l.append(img)
                l.append(img)
            result = cycle(l)
        else:
            result = cycle([CourseImageBreaker(
                image='https://s3.eu-central-1.amazonaws.com/ln2ximages/' \
                        'Backgrounds/gallaxy-connected.png'),])
        return result

    def general_contents(self):
        return list(chain(self.contents.filter(content__lang_code=self.lang_code, content__content_type="General")))

    def get_content(self, contentType, defaultName):
        result = self.contents.filter(
                content__lang_code=self.lang_code,
                content__content_type=contentType).order_by('creation_date').first()
        if result is None:
            content = PageContent.objects.filter(
                    lang_code=self.lang_code,
                    reference=defaultName).first()
            result = MarketingContent(content=content)
        return result

    def who_attends_content(self):
        return self.get_content("WhoAttends", "Default_WhoAttends")

    def speakers_content(self):
        result = self.get_content("Speakers", "DefaultSpeakersTab")
        return result

    def sponsors_content(self):
        result = self.get_content("Sponsors", "DefaultSponsorsTab")
        return result

    def speakers_list(self):
        speakers = list(self.speakers.all())
        return speakers

    def trainers_content(self):
        return self.get_content("Trainers", None)

    def agenda_content(self):
        result = self.get_content("Agenda", "AgendaLabel")
        if not result.content.title or result.content.title == '':
            result.content.title = 'Agenda'
        if not result.content.rich_text or result.content.rich_text == '':
            result.content.rich_text = self.agenda
        return result

    def agenda_default_content(self):
        result = self.get_content("AgendaLabel", "AgendaLabel")
        if result.content.title == '':
            result.content.title = 'Agenda'
        return result

    def next_sessions_content(self):
        result = self.get_content("NextSession", "DefaultNextSesionTab")
        if result.content.title == '':
            result.content.title = _('Next Sessions')
        return result

    def no_next_sessions_content(self):
        result = self.get_content("NoNextSessionTab", "NoNextSessionTab")
        if result.content.title == '':
            result.content.title = _('Next Sessions')
        return result

    def confirmed_session_list(self):
        return list(
                self.sessions.filter(published=True).order_by('slot_number')
                )

    def course_session_list(self):
        return self.session_list()

    def all_session_list(self):
        return self.session_list()

    def days_session_list(self):
        return list(list(self.session_list()))

    def all_sponsor_list(self):
        all_sponsors = list()
        events = list(self.events.order_by('-start_date'))
        for event in events:
            for eventSponsor in event.all_sponsors_list():
                for allSponsor in all_sponsors:
                    if allSponsor.account_name == eventSponsor.account_name:
                        break
                else:
                    all_sponsors.append(eventSponsor)
        return sorted(all_sponsors, key = lambda sponsor: sponsor.account_name)



    def venue_content(self):
        return self.get_content("Venue", "NoVenueTab")

    def testimonials_content(self):
        return self.get_content("TestimonialTab", "DefaultTestimonialTab")

    def get_absolute_url(self):
        return '/course/' + self.slug + '/'

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit Course</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''

    edit_self.allow_tags = True

class CourseImageBreaker(Orderable):
    course = models.ForeignKey(CoursePage, related_name="image_breakers", null=True)
    image = models.URLField(_("Image URL"), blank=True, max_length=500)

class EventManager(DisplayableManager):
    def are_not_past(self):
        today = datetime.date.today()
        return self.filter(end_date__gt=today, course__isnull=False)

    def are_past(self):
        today = datetime.date.today()
        return self.filter(end_date__lt=today, course__isnull=False)

    def are_published(self):
        return self.filter(status=CONTENT_STATUS_PUBLISHED)

class EventPage(SalesforceSynced, Displayable):
    """
    The model for the page corresponding to a Salesforce Event, with extra
    fields for the page
    """

    class Meta:
        verbose_name = _("Event Page")
        verbose_name_plural = _("Event Pages")
        ordering = ['-start_date', 'country',]

    objects = EventManager()

    course = models.ForeignKey(CoursePage, related_name="events", null=True)

    lang_code = models.CharField(_("Language code"), max_length=2, default="en")
    macro_region = models.CharField(_("Macro Region"), max_length=1300,
            blank=True, null=True)

    terms_conditions = RichTextField(_("Terms and Conditions"), blank=True,
            null=True)

    start_date = models.DateField(_("Start Date"), null=True)
    end_date = models.DateField(_("End Date"), null=True)
    early_bird_deadline = models.DateField(_("Early Bird Deadline"), null=True)

    display_agenda_days = models.BooleanField(_("Display Agenda Days"),
            default=False)
    display_session_times = models.BooleanField(_("Display Session Times"),
            default=False)
    times = models.CharField(_("Event Times"), max_length=200, blank=True,
            null=True)
    seats_left = models.IntegerField(_("Number of Seats Left"), default=0)
    sold_out = models.BooleanField(_("Sold Out"), default=False)

    attendee_number = models.IntegerField(_("Number of Attendee"), default=0)

    ticket_price = MoneyField(_("Ticket Price"), max_digits=18,
            decimal_places=2, default_currency='GBP')
    standard_price = MoneyField(_("Standard Price"), max_digits=6,
            decimal_places=2, default_currency='GBP')
    nb_group_discount = models.IntegerField(_("Nb Tickets Group Discount"),
            null=True)

    address = models.TextField(_("Address"), max_length=255, blank=True,
            null=True)
    city = models.CharField(_("City"), max_length=255, blank=True,
            null=True)
    country = models.CharField(_("Country"), max_length=255, blank=True,
            null=True)
    macro_region = models.CharField(_("Macro Region"), max_length=1300, blank=True, null=True)
    venue_description = models.TextField(_("Venue Description"),
            max_length=32768, blank=True, null=True)
    venue_name = models.CharField(_("Venue Name"), max_length=255, blank=True,
            null=True)
    latitude = models.DecimalField(_("Latitude"), max_digits=5,
            decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(_("Longitude"), max_digits=5,
            decimal_places=2, blank=True, null=True)

    location_thumb = models.URLField(_("Location Thumb"), blank=True, null=True)

    speaker_intro = RichTextField(_("Speaker Intro"), blank=True, null=True)
    sponsor_intro = RichTextField(_("Sponsor Intro"), blank=True, null=True)
    sponsor_list_title = models.CharField(_("Sponsor List Title"),
            max_length=30, blank=True, null=True)

    multilang_keywords = models.ManyToManyField(MultilangKeyword, \
            related_name='event_pages', blank=True)

    def is_published(self):
        return self.status == CONTENT_STATUS_PUBLISHED

    def keywords_list(self):
        keywords = set(self.multilang_keywords.all())
        keywords.update(set(self.course.keywords_list()))
        return sorted(keywords, key=lambda keyword: keyword.word)

    def date(self):
        langCode = self.course.lang_code
        result = format_date(self.start_date, "EEEE dd",
                locale=langCode)
        if self.start_date != self.end_date:
            if self.start_date.month != self.end_date.month:
                result += format_date(self.start_date, " MMMM",
                        locale=langCode)
                if self.start_date.year != self.end_date.year:
                    result += format_date(self.start_date, " yyyy",
                            locale=langCode)
            result += format_date(self.end_date, " - EEEE dd MMMM yyyy",
                    locale=langCode)
        else:
                result += format_date(self.start_date, " MMMM yyyy",
                        locale=langCode)
        return result

    def short_date(self):
        langCode = self.course.lang_code
        result = format_date(self.start_date, "dd",
                locale=langCode)
        if self.start_date != self.end_date:
            if self.start_date.month != self.end_date.month:
                result += format_date(self.start_date, " MMM",
                        locale=langCode)
                if self.start_date.year != self.end_date.year:
                    result += format_date(self.start_date, " yyyy",
                            locale=langCode)
            result += format_date(self.end_date, " - dd MMM yyyy",
                    locale=langCode)
        else:
                result += format_date(self.start_date, " MMM yyyy",
                        locale=langCode)
        return result

    def _get_region(self):
        for region in REGIONS:
            if self.country in region:
                return region
            else:
                return 'other'
    region = property(_get_region)

    def next_sessions(self):
        next_sessions = self.course.next_sessions() if \
                self.course else None
        if next_sessions and self in next_sessions:
            next_sessions.remove(self)
        return next_sessions

    def seats_occupied(self):
        return int((self.course.target_delegates - self.seats_left) / \
                self.course.target_delegates * 100)

    def remaining_days(self):
        return (self.start_date - datetime.date.today()).days

    def early_bird_days(self):
        return (self.early_bird_deadline - datetime.date.today()).days

    def is_past(self):
        return self.start_date < datetime.date.today()

    def still_earlybird(self):
        return self.early_bird_deadline > datetime.date.today()

    def general_contents(self):
        return list(chain(self.contents.filter(content__lang_code=self.lang_code, content__content_type="General"),self.course.contents.filter(content__lang_code=self.lang_code, content__content_type="General")))

    def get_content(self, contentType, defaultName):
        result = self.contents.filter(
                content__lang_code=self.lang_code,
                content__content_type=contentType).order_by('creation_date').first()
        if result is None:
            result = self.course.contents.filter(
                    content__lang_code=self.lang_code,
                    content__content_type=contentType).order_by('creation_date').first()
        if result is None:
            content = PageContent.objects.filter(
                    lang_code=self.lang_code,
                    reference=defaultName).first()
            result = MarketingContent(content=content)
        return result

    def who_attends_content(self):
        return self.get_content("WhoAttends", "Default_WhoAttends")

    def speakers_content(self):
        result = self.get_content("Speakers", "DefaultSpeakersTab")
        return result

    def sponsors_content(self):
        result = self.get_content("Sponsors", "DefaultSponsorsTab")
        return result

    def old_sponsors_content(self):
        content = PageContent.objects.filter(
                lang_code=self.lang_code,
                reference="DefaultOldSponsorsTab").first()
        result = MarketingContent(content=content)
        return result

    def speakers_list(self):
        speakers = list(self.speakers.all())
        if not speakers:
            speakers = self.course.speakers_list
        return speakers

    def trainers_content(self):
        return self.get_content("Trainers", None)

    def agenda_content(self):
        result = self.get_content("Agenda", "AgendaLabel")
        if not result.content.title or result.content.title == '':
            result.content.title = 'Agenda'
        if not result.content.rich_text or result.content.rich_text == '':
            result.content.rich_text = self.course.agenda
        return result

    def agenda_default_content(self):
        result = self.get_content("AgendaLabel", "AgendaLabel")
        if result.content.title == '':
            result.content.title = 'Agenda'
        return result

    def next_sessions_content(self):
        result = self.get_content("NextSession", "DefaultNextSesionTab")
        if result.content.title == '':
            result.content.title = _('Next Sessions')
        return result

    def no_next_sessions_content(self):
        result = self.get_content("NoNextSessionTab", "NoNextSessionTab")
        if result.content.title == '':
            result.content.title = _('Next Sessions')
        return result

    def confirmed_session_list(self):
        return list(
                self.sessions.filter(published=True).order_by('slot_number')
                )

    def course_session_list(self):
        return self.course.session_list()

    def all_session_list(self):
        result = self.confirmed_session_list()
        result.extend(self.course_session_list())
        return result

    def days_session_list(self):
        allSessions = self.sessions.filter(published=True). \
                order_by('start_time')
        day = list()
        days = list()
        day.append(allSessions[0])
        days.append(day)
        for session in allSessions[1:]:
            if session.start_time.date() == day[0].start_time.date():
                day.append(session)
            else:
                day = list()
                day.append(session)
                days.append(day)
        return days

    def all_sponsors_list(self):
        return list(self.sponsors.all());

    def types_sponsor_list(self):
        allSponsors = self.sponsors.all(). \
                order_by('sponsor_type', 'name')
        typeLists = None
        if allSponsors:
            typeList = list()
            typeLists = list()
            typeLists.append(typeList)
            typeList.append(allSponsors[0])
            for sponsor in allSponsors[1:]:
                if sponsor.sponsor_type == typeList[0].sponsor_type:
                    typeList.append(sponsor)
                else:
                    typeList = list()
                    typeList.append(sponsor)
                    typeLists.append(typeList)
        return typeLists

    def old_sponsor_list(self):
        return self.course.all_sponsor_list()

    def venue_content(self):
        return self.get_content("Venue", "NoVenueTab")

    def testimonials_content(self):
        return self.get_content("TestimonialTab", "DefaultTestimonialTab")

    def testimonials_block(self):
        pass


    def get_absolute_url(self):
        return '/event/' + self.slug + '/'

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit eventPage</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''

    edit_self.allow_tags = True

    def edit_course(self):
        return self.course.edit_self() if self.course else ''

    edit_course.allow_tags = True

class OldSlug(models.Model):
    """
    Old urls of an event or course page
    """
    slug = models.CharField(_('URL'), max_length=2000, null=True, blank=True)
    event_page = models.ForeignKey(EventPage, related_name='old_slugs',
            null=True, blank=True)
    course_page = models.ForeignKey(CoursePage, related_name='old_slugs',
            null=True, blank=True)

class Session(SalesforceSynced):
    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

    name = models.CharField(max_length=80, verbose_name='Name', \
            null=True, blank=True)
    course = models.ForeignKey(CoursePage, models.DO_NOTHING,
            blank=True, null=True, related_name='sessions')
    event = models.ForeignKey(EventPage, models.DO_NOTHING, blank=True,
            null=True, related_name='sessions')
    content_reference = models.URLField(verbose_name='Content Reference', \
            blank=True, null=True)
    published = models.BooleanField(default=False)
    abstract = models.TextField(verbose_name='Abstract', \
            blank=True, null=True)
    code = models.CharField(max_length=30, verbose_name='Code',\
            blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='End Time', \
            blank=True, null=True)
    session_format = models.CharField(max_length=255, \
            verbose_name='Session Format', choices=[
                ('Case study with customer(s)', 'Case study with customer(s)'),
                ('Hands-on training', 'Hands-on training'),
                ('Panel with customers', 'Panel with customers'),
                ('Demo with customer(s)', 'Demo with customer(s)'),
                ('Presentation without customer(s)',
                    'Presentation without customer(s)'),
                ('BREAK', 'BREAK')
                ], blank=True, null=True)
    slot_number = models.IntegerField(verbose_name='Session Slot Number',
            choices=zip( range(1,12), range(1,12)), blank=True, null=True)
    start_time = models.DateTimeField(
            verbose_name='Session Start Time', blank=True, null=True)
    take = models.TextField(verbose_name='Session Takeaways',
            blank=True, null=True)
    theme = models.CharField( max_length=255,
            verbose_name='Session Theme', choices=[
                ('Product Roadmap', 'Product Roadmap'), ('Mobile', 'Mobile'),
                ('AppExchange', 'AppExchange'), ('Apex', 'Apex'),
                ('SSS', 'SSS'), ('PRM', 'PRM'), ('UE', 'UE'),
                ('Marketing', 'Marketing'), ('Core Needs', 'Core Needs'),
                ('Vertical', 'Vertical'), ('New Release', 'New Release')
                ], blank=True, null=True)
    sponsored = models.BooleanField(default=False)
    public_name = models.TextField(verbose_name='Session Public Name',
            blank=True, null=True)
    image = models.URLField(verbose_name='SessionImage',
            blank=True, null=True)

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit session</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''
    edit_self.allow_tags = True

    def right_time_timezone(self):
#	self.start_time = self.start_time.time.astimezone(timezone('Europe/London'))
#       self.end_time = timezone('Europe/London').localize(self.end_time)  
        
        return self

    def __str__(self):
        return self.public_name or 'No public name'

class Speaker(SalesforceSynced):
    """
    Equivalent of Speaker on SalesForce, simplified for Django
    """

    class Meta:
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")

    contact_name = models.CharField(_('Name'), max_length=121, null=True, blank=True)
    contact_title = models.CharField(_('Title'), max_length=128, null=True, blank=True)
    account_name = models.CharField(_('Account Name'), max_length=128, null=True, blank=True)
    event = models.ForeignKey(EventPage, related_name="speakers", blank=True,
            null=True)
    course = models.ForeignKey(CoursePage, related_name="speakers", blank=True,
            null=True)
    bio = models.CharField(_('Bio'), max_length=32768, null=True, blank=True)
    custom_profile_image = models.URLField(_('Custom Profile Image'), \
            blank=True, null=True)
    custom_name = models.CharField(_('Custom Name'), max_length=250, \
            blank=True, null=True)
    anonymous_contact_name = models.BooleanField( \
            _('Anonymous Contact Name'), default=True)
    anonymous_title_name = models.BooleanField( \
            _('Anonymous Title Name'), default=True)
    anonymous_account_name = models.BooleanField( \
            _('Anonymous Account Name'), default=True)
    speaker_country = models.CharField(_('Speaker Country'), max_length=1300, \
            blank=True, null=True)
    speaker_rating = models.DecimalField(_('Speaker Rating'), max_digits=5, \
            decimal_places=2, blank=True, null=True)

    def public_name(self):
        if self.custom_name:
            return self.custom_name
        else:
            result = ''
            if self.contact_name and not self.anonymous_contact_name:
                result += self.contact_name
            if self.contact_title and not self.anonymous_title_name:
                if result != '':
                    result += ', '
                result += self.contact_title
            if self.account_name and not self.anonymous_account_name:
                if result != '' and result[:-2] != ' ,':
                    result += ', '
                result += self.account_name
            return result

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit Speaker</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''

    edit_self.allow_tags = True

    def __str__(self):
        return self.public_name() or 'Speaker'

class Sponsor(SalesforceSynced):

    class Meta():
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'

    name = models.CharField(_('Name'), max_length=80, null=True, blank=True)
    event = models.ForeignKey(EventPage, related_name="sponsors", blank=True,
            null=True)

    account_name = models.CharField(_('Account Name'), max_length=80,
            null=True, blank=True)
    account_logo = models.URLField(_('Account Logo'), blank=True, null=True)
    account_description = models.TextField(_('Account Description'),
            blank=True, null=True)

    sponsor_type = models.CharField(_('Sponsor Type'), max_length=255,
            choices=[
                ('Strategic Partners', 'Strategic Partners'),
                ('Sponsors', 'Sponsors'),
                ('Media Partners', 'Media Partners'),
                ('In Partnership with', 'In Partnership with')],
            blank=True, null=True)
    custom_description = models.TextField(_('Custom Description'), blank=True,
            null=True)
    custom_name = models.CharField(_('Custom Name'), max_length=255,
            blank=True, null=True)
    custom_logo = models.URLField(_('Custom Logo'), blank=True, null=True)

    def label(self):
        "Text to show to introduce the sponsor"
        content = PageContent.objects.filter(content_type='SponsorType',
                reference=self.sponsor_type, lang_code=self.event.lang_code
                ).first()
        label = dict()    

        if content:
            label['singular'] = content.rich_text
            label['plural'] = content.title[2:]
        return label or None

    def public_name(self):
        if self.custom_name:
            return self.custom_name
        else:
            return self.account_name

    def public_description(self):
        if self.custom_description:
            return self.custom_description
        else:
            return self.account_description or ''

    def public_logo(self):
        if self.custom_logo:
            return self.custom_logo
        else:
            return self.account_logo

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit Sponsor</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''

    edit_self.allow_tags = True

    def __str__(self):
        return self.public_name() or 'Sponsor'

class PageContent(SalesforceSynced):
    """
    Equivalent of Marketing Content on SalesForce, simplified for Django
    """

    class Meta:
        verbose_name = _("Page Content")
        verbose_name_plural = _("Page Contents")

    title = models.CharField(_("Title"), max_length=250, blank=True, null=True)
    rich_text = RichTextField(_("Rich Text"), max_length=32768, blank=True,
            null=True)

    content_type = models.CharField(_("Type"), max_length=50, blank=True,
            null=True)
    reference = models.CharField(_("Reference"), max_length=250, blank=True,
            null=True)
    lang_code = models.CharField(_("Language code"), max_length=2, default="en")

    is_keyword_filter = models.BooleanField(default=False)

    def edit_self(self):
        if self.id:
            return '<a href="%s">' \
                    'Edit Content</a>' % admin_url(self.__class__, "change",
                    self.id)
        return ''

    edit_self.allow_tags = True

    def __str__(self):
        return self.title or 'No title'

class MarketingContent(SalesforceSynced):
    """
    Equivalent of Marketing Content on SalesForce, simplified for Django
    """

    class Meta:
        verbose_name = _("Marketing Content")
        verbose_name_plural = _("Marketing Contents")

    course = models.ForeignKey(CoursePage, related_name="contents", blank=True,
            null=True)
    event = models.ForeignKey(EventPage, related_name="contents", blank=True,
            null=True)
    content = models.ForeignKey(PageContent, related_name="contents",
            blank=True, null=True)

    creation_date = models.DateField(_("Creation Date"), null=True)

    def image_64px(self):
        return self.images.filter(image_type="Icon 64px").first()

    def images_128px(self):
        return self.images.filter(image_type="Icon 128px")

    def images_3col(self):
        return self.images.filter(image_type="3_col")

    def edit_self(self):
        if self.id:
            return '<a href="%s"> Edit Marketing Content</a>' % admin_url(
                    self.__class__, "change", self.id)
        return ''

    edit_self.allow_tags = True

    def edit_course(self):
        return self.course.edit_self() if self.course else ''

    edit_course.allow_tags = True

    def edit_event(self):
        return self.event.edit_self() if self.event else ''

    edit_event.allow_tags = True

    def edit_content(self):
        return self.content.edit_self() if self.content else ''

    edit_content.allow_tags = True


class LnxImage(SalesforceSynced):
    """
    Equivalent of LNX Image on SalesForce, simplified for Django
    """

    image_type = models.CharField(_("Type"), max_length=50, blank=True,
            null=True)
    url = models.URLField(_("URL"), blank=True, null=True)

    mark_content = models.ForeignKey(MarketingContent, related_name="images",
            null=True)

    def edit_self(self):
        if self.id:
            return '<a href="%s"> Edit Image</a>' % admin_url(
                    self.__class__, "change", self.id)
        return ''
    edit_self.allow_tags = True

    def edit_mark_content(self):
        return self.mark_content.edit_self() if self.mark_content else ''

    edit_mark_content.allow_tags = True

class Testimonial(SalesforceSynced):
    """
    Equivalent of Testimonial on SalesForce, simplified for Django
    """

    ranking = models.IntegerField(_("Ranking"), default=5)
    lang_code = models.CharField(_("Language code"), max_length=2, default="en")
    creation_date = models.DateTimeField(_("Creation Date"),
            default=timezone.now, blank=True, null=True)
    contact_title = models.CharField(_("Contact Title"), max_length=1300,
            blank=True, null=True)
    course = models.ForeignKey(CoursePage, related_name="testimonials", \
            null=True)
    testimonial_text = models.TextField(_("Text"), max_length=32768, blank=True,
            null=True)
    featured = models.BooleanField(_("Featured"), default=False)

