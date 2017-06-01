from django.contrib import admin

from mezzanine.core.admin import TabularDynamicInlineAdmin

from ln2xevents.models import EventPage, CoursePage, PageContent, MarketingContent, LnxImage, CourseImageBreaker, Testimonial, Session, Speaker, Sponsor, OldSlug

class CourseImageBreakInline(TabularDynamicInlineAdmin):
    model = CourseImageBreaker
    fields = ['image']

class MarketingContentInline(TabularDynamicInlineAdmin):
    model = MarketingContent
    fields = ['edit_self', 'content', 'edit_content', 'course', 'edit_course',
            'event', 'edit_event']
    readonly_fields = ['edit_self', 'content', 'edit_content', 'course',
            'edit_course', 'event', 'edit_event']

class SessionInline(TabularDynamicInlineAdmin):
    model = Session
    fields = ['edit_self', 'slot_number', 'public_name', 'published',]
    readonly_fields = ['edit_self', 'slot_number', 'public_name', 'published',]
    ordering = ['slot_number',]


class SpeakerInline(TabularDynamicInlineAdmin):
    model = Speaker
    readonly_fields = ['edit_self', 'public_name',]
    fields = ['edit_self', 'public_name',]

class SpeakerAdmin(admin.ModelAdmin):
    class Meta:
        model = Speaker

    readonly_fields = ['public_name',]

admin.site.register(Speaker, SpeakerAdmin)

class SponsorInline(TabularDynamicInlineAdmin):
    model = Sponsor
    readonly_fields = ['edit_self', 'public_name',]
    fields = ['edit_self', 'public_name',]

class SponsorAdmin(admin.ModelAdmin):
    class Meta:
        model = Sponsor

    readonly_fields = ['public_name',]

admin.site.register(Sponsor, SponsorAdmin)

class PageContentAdmin(admin.ModelAdmin):
    class Meta:
        model = PageContent

    list_display = ('reference', 'title', 'lang_code', 'content_type')
    list_filter = (
            'reference', 'title', 'lang_code',
            'content_type',
            )
    search_fields = ('title', 'content_type', 'reference', 'rich_text',)
    exclude = ('is_keyword_filter',)
    readonly_fields = ['title', 'salesforce_id', 'last_sync', 'lang_code',
            'rich_text', 'content_type', 'reference']
    inlines = (MarketingContentInline,)

admin.site.register(PageContent, PageContentAdmin)

class LnxImageAdmin(admin.ModelAdmin):
    class Meta:
        model = LnxImage

    list_display = ('mark_content',)
    list_filter = ('mark_content',)
    exclude = ('mark_content', )
    readonly_fields = ['salesforce_id', 'last_sync', 'image_type', 'url',
            'edit_mark_content']

admin.site.register(LnxImage, LnxImageAdmin)

class LnxImageInline(TabularDynamicInlineAdmin):
    model = LnxImage
    fields = ['edit_self', 'image_type', 'url',]
    readonly_fields = ['edit_self', 'image_type', 'url',]

class OldSlugInline(TabularDynamicInlineAdmin):
    model = OldSlug
    fields = ['slug',]

class MarketingContentAdmin(admin.ModelAdmin):
    class Meta:
        model = MarketingContent

    list_display = ('course', 'event', 'content',)
    list_filter = ('course', 'event', 'content',)
    search_fields = ('course__title', 'event__title','content__title',
            'content__reference', 'content__rich_text')
    readonly_fields = ['salesforce_id', 'last_sync', 'creation_date',
            'content', 'edit_content', 'course',
            'edit_course', 'event', 'edit_event',]
    inlines = (LnxImageInline,)

admin.site.register(MarketingContent, MarketingContentAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    class Meta:
        model = Testimonial

    list_display = ('testimonial_text', 'creation_date', 'lang_code', 'ranking')
    list_filter = ('contact_title', 'testimonial_text',)

admin.site.register(Testimonial, TestimonialAdmin)

class SessionAdmin(admin.ModelAdmin):
    class Meta:
        model = Session

admin.site.register(Session, SessionAdmin)

class EventPageAdmin(admin.ModelAdmin):
    class Meta:
        model = EventPage

    list_display = ('title', 'start_date',)
    list_filter = ('title', 'start_date', 'course__delivery_format',)
    search_fields = ('title', 'slug',)
    filter_horizontal = ('multilang_keywords',)
    exclude = ('keywords', 'publish_date', 'expiry_date', 'short_url',
            'gen_description', '_meta_title')
    readonly_fields = ['status', 'title', 'slug', 'description', 'course',
            'edit_course', 'salesforce_id', 'last_sync',
            'lang_code', 'macro_region',
            'terms_conditions', 'start_date', 'end_date',
            'early_bird_deadline', 'display_agenda_days',
            'display_session_times', 'times', 'seats_left', 'sold_out',
            'attendee_number', 'ticket_price', 'standard_price',
            'nb_group_discount', 'address', 'city', 'country', 'macro_region',
            'venue_description', 'venue_name', 'latitude', 'longitude',
            'location_thumb', 'speaker_intro', 'sponsor_intro',
            'sponsor_list_title',]
    inlines = (MarketingContentInline, SpeakerInline, SponsorInline,
            SessionInline, OldSlugInline, )

admin.site.register(EventPage, EventPageAdmin)

class EventPageInline(TabularDynamicInlineAdmin):
    model = EventPage
    fields = ['edit_self', 'slug', ]
    readonly_fields = ['edit_self', 'slug', ]

class CoursePageAdmin(admin.ModelAdmin):
    class Meta:
        model = CoursePage

    list_display = ('title', 'lang_code',)
    list_filter = ('title', 'lang_code',)
    search_fields = ('title',)
    filter_horizontal = ('multilang_keywords',)
    exclude = ('keywords', 'publish_date', 'expiry_date', 'short_url',
            'gen_description', '_meta_title')
    readonly_fields = ['status', 'title', 'slug', 'description',
            'salesforce_id', 'last_sync', 'lang_code', 'delivery_format',
            'banner', 'thumb', 'level', 'subject_category', 'duration',
            'agenda', 'who_attends', 'objectives', 'pre_requisites',
            'ref_source', 'languages_availables', 'course_level',
            'target_delegates', 'product_reference', ]
    inlines = (CourseImageBreakInline, OldSlugInline, EventPageInline,
            MarketingContentInline, SessionInline, )

admin.site.register(CoursePage, CoursePageAdmin)
