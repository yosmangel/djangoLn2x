from django.contrib import admin

from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import SimpleTemplateResponse
from django.utils.html import escape, escapejs
from django.db import models
from django.forms import TextInput, Textarea, URLInput

from mezzanine.core.admin import TabularDynamicInlineAdmin, BaseTranslationModelAdmin
from mezzanine.pages.admin import PageAdmin

from .models import MultilangKeyword, UnifyPage, Row, RowToPage, Element, Input

from copy import deepcopy
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from mezzanine.pages.models import Page

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(4, "multilang_keywords")
blog_fieldsets[0][1]["fields"].insert(5,"image_url")
blog_fieldsets[0][1]["fields"].append("country")
blog_fieldsets[0][1]["fields"].append("city")
blog_fieldsets[0][1]["fields"].append("source")
blog_fieldsets[0][1]["fields"].append("user")
#blog_fieldsets[0][1]["fields"].remove("categories")

class MyBlogPostAdmin(BlogPostAdmin):
        fieldsets = blog_fieldsets
        filter_horizontal = ('multilang_keywords',)

admin.site.unregister(BlogPost)
admin.site.register(BlogPost, MyBlogPostAdmin)


page_fieldsets = deepcopy(PageAdmin.fieldsets)
page_fieldsets[0][1]["fields"].append("intro")
page_fieldsets[0][1]["fields"].append("background")
page_fieldsets[0][1]["fields"].append("is_background_fixed")
page_fieldsets[0][1]["fields"].append("image_url")
page_fieldsets[0][1]["fields"].append("miniature_url")
page_fieldsets[0][1]["fields"].append("include_contact_form")
page_fieldsets[0][1]["fields"].append("multilang_keywords")
#page_fieldsets[0][1]["fields"].remove("keywords")

class MyPageAdmin(PageAdmin):
        fieldsets = page_fieldsets

admin.site.unregister(Page)
admin.site.register(Page, MyPageAdmin)

class ToUnifyPageInline(admin.TabularInline):
    model = RowToPage
    fields = ['unifypage', 'edit_page',]
    readonly_fields = ['edit_page']

class ToRowInline(TabularDynamicInlineAdmin):
    model = RowToPage
    fields = ['row', 'edit_row',]
    readonly_fields = ['edit_row']

class ElementInline(TabularDynamicInlineAdmin):
    model = Element
    fields = ['edit_self', 'element_type', 'title', 'content', 'icon_class',
            'icon_url', 'size', 'size_sm', 'size_xs', 'is_formula', 'more_url']
    readonly_fields = ['edit_self']
    formfield_overrides = {
            models.CharField: {'widget': TextInput()},
            models.TextField: {'widget': Textarea(attrs={'rows':3})},
            models.URLField: {'widget': URLInput()},
            }

class InputInline(TabularDynamicInlineAdmin):
    model = Input
    formfield_overrides = {
            models.CharField: {'widget': TextInput()},
            }

class RowAdmin(BaseTranslationModelAdmin):
    exclude = ['_order']
    inlines = (ElementInline, ToUnifyPageInline)
    save_as = True

admin.site.register(Row, RowAdmin)

class ElementAdmin(BaseTranslationModelAdmin):
    fieldsets = (
            (None, {
                'fields': (
                    ('row', 'edit_row', 'element_type'),
                    ('title', 'content'),
                    ('is_formula', 'more_url'), ('icon_class', 'icon_url'),
                    ('size', 'size_sm', 'size_xs'),
                    ('css_class')
                    ),
                }),
            ('Form', {
                'fields': ('action', 'button_label'),
                'classes': ('collapsed',),
                }),
            )
    readonly_fields = ['edit_row']
    inlines = (InputInline,)
    save_as = True

    def in_menu(self):
        return False

admin.site.register(Element, ElementAdmin)

class UnifyPageAdmin(MyPageAdmin):
    inlines = (ToRowInline,)
    exclude = ('rows',)
    save_as = True
    filter_horizontal = ('multilang_keywords',)

admin.site.register(UnifyPage, UnifyPageAdmin)

class MultilangKeywordAdmin(BaseTranslationModelAdmin):
    save_as = True

admin.site.register(MultilangKeyword, MultilangKeywordAdmin)

