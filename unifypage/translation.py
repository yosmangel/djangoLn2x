from modeltranslation.translator import translator, TranslationOptions
from .models import MultilangKeyword, UnifyPage, Row, RowToPage, Element, Input

class TranslatedMultilangKeyword(TranslationOptions):
    fields = ('word',)

class TranslatedUnifyPage(TranslationOptions):
    fields = ('intro',)

class TranslatedRow(TranslationOptions):
    fields = ('title', 'intro', 'more_url',)

class TranslatedRowToPage(TranslationOptions):
    fields = ()

class TranslatedElement(TranslationOptions):
    fields = ('title', 'content', 'more_url',)

class TranslatedInput(TranslationOptions):
    fields = ('label', 'placeholder', 'value')

translator.register(MultilangKeyword, TranslatedMultilangKeyword)
translator.register(UnifyPage, TranslatedUnifyPage)
translator.register(Row, TranslatedRow)
translator.register(RowToPage, TranslatedRowToPage)
translator.register(Element, TranslatedElement)
translator.register(Input, TranslatedInput)
