from modeltranslation.translator import translator, TranslationOptions
from .models import EventPage, CoursePage, CourseImageBreaker, MarketingContent, LnxImage, Session, Speaker, Sponsor, OldSlug

class TranslatedEmpty(TranslationOptions):
    fields = ()
translator.register(CourseImageBreaker, TranslatedEmpty)
translator.register(LnxImage, TranslatedEmpty)
translator.register(MarketingContent, TranslatedEmpty)
translator.register(CoursePage, TranslatedEmpty)
translator.register(EventPage, TranslatedEmpty)
translator.register(Session, TranslatedEmpty)
translator.register(Speaker, TranslatedEmpty)
translator.register(Sponsor, TranslatedEmpty)
translator.register(OldSlug, TranslatedEmpty)
