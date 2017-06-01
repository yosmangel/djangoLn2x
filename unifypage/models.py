from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page, Displayable
from mezzanine.core.models import Orderable, CONTENT_STATUS_PUBLISHED
from mezzanine.core.fields import RichTextField
from mezzanine.utils.urls import admin_url
from mezzanine.core.templatetags.mezzanine_tags import editable
from mezzanine.blog.models import BlogPost

from datetime import date
import numpy, math

from . import rowtypes
from . import elementtypes
from . import inputtypes
from magentrix.models import Event, Account, Testimonial

class MultilangKeyword(models.Model):
    """
    A keyword associated to different models and translatable
    """
    word = models.CharField(_("Word"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Multilang Keyword")
        verbose_name_plural = _("Multilang Keywords")
        ordering = ("word",)

    def __str__(self):
        if self.word is None:
            return 'No English'
        else:
            return self.word

class UnifyPage(Page):
    """
    A user-built page using Unify Template
    """
    miniature_url = models.CharField(_("Miniature URL"), max_length=200, \
            blank=True)
    preview_text = models.CharField(_("Preview Text"), max_length=100, \
            blank=True)
    intro = RichTextField(_("Introduction text"), blank=True)
    background = models.CharField(_("Background"), max_length=500,
            blank=True)
    is_background_fixed = models.BooleanField(_("Fixed Background"),
            default=False, help_text=_('Display the Background with a "fixed"'\
                    ' effect'))
    include_contact_form = models.BooleanField(_("Include Contact Form"),
            default=False)

    multilang_keywords = models.ManyToManyField(MultilangKeyword, \
            related_name='pages', blank=True)

    class Meta:
        verbose_name = _("Unify Page")
        verbose_name_plural = _("Unify Pages")

    def edit_self(self):
        """
        Returns a link to this item change form
        """
        if self.id:
            return '<a href="%s">' \
                'Edit Page</a>' % admin_url(self.__class__, "change",
                self.id)
        return ''

    edit_self.allow_tags = True

    def all_children(self):
        pages = list(self.children.order_by("_order"))
        result = list()
        for page in pages:
            result.append(page.unifypage)
        children = list(result)
        for child in children:
            child_children = list(child.unifypage.all_children())
            if child_children:
                result.extend(child_children)
        return result

    def section_pages(self):
        if self.slug == '/':
            result = list(UnifyPage.objects.filter(parent=None))
        else:
            page_list = list()
            parent = self
            while parent.parent:
                parent = parent.parent
            parent = parent.unifypage
            result = parent.all_children()
            result.insert(0, parent)
        result.remove(self)
        return result

    def is_public(self):
        return self.status == CONTENT_STATUS_PUBLISHED



class Row(Orderable):
    """
    A user-built row
    """

    name = models.CharField(_("Name (hidden)"), max_length=50, blank=True,
            help_text=_("A name to help differenciate the rows when setting" \
                    " order"))
    title = models.CharField(_("Title"), max_length=50, blank=True)
    intro = RichTextField(_("Introduction"), blank=True)
    row_type = models.IntegerField(_("Type"), choices=rowtypes.NAMES)
    background = models.CharField(_("Background"), max_length=500,
            blank=True, help_text=_("CSS background property<br/>" \
                    "Can take: url(your_image_url), <br/>" \
                    "A color name (exemple grey), <br/>" \
                    "rgba(red, green, blue, opacity) with red, green and " \
                    "blue between 0 and 255 and opacity between 0 and 1,<br/>" \
                    "#hexvalue...<br/>" \
                    "Or default_image to put the same as the page"))
    is_fixed = models.BooleanField(_("Fixed Background"),
            default=False, help_text=_('Display the Background with a "fixed"'\
                    ' effect'))
    more_url = models.CharField(_("Link to more(row)"), max_length=200,
            blank=True, help_text="A button a the bottom of the row will link "
            "to this URL. For a Youtube video Row, "
            "put here the ID of the video")


    css_class = models.CharField("CSS Class", max_length=200, blank=True,
            help_text='To potentially  add a CSS class to the englobing div')

    def edit_self(self):
        """
        Returns a link to this item change form
        """
        if self.id:
            return '<a href="%s">' \
                'Edit Row</a>' % admin_url(self.__class__, "change",
                self.id)
        return ''

    edit_self.allow_tags = True

    def is_container(self):
        return self.row_type == rowtypes.CONTAINER

    def is_parallaxc(self):
        return self.row_type == rowtypes.PARALLAXC

    def is_parallaxc1(self):
        return self.row_type == rowtypes.PARALLAXC1

    def is_parallaxc2(self):
        return self.row_type == rowtypes.PARALLAXC2

    def is_parallaxc3(self):
        return self.row_type == rowtypes.PARALLAXC3

    def is_parallaxc4(self):
        return self.row_type == rowtypes.PARALLAXC4

    def is_gallery(self):
        return self.row_type == rowtypes.GALLERY

    def is_service_block_4(self):
        return self.row_type == rowtypes.SERVICEBLOCK4

    def is_team_3(self):
        return self.row_type == rowtypes.TEAM3

    def is_testimonials_6(self):
        return self.row_type == rowtypes.TESTIMONIALS6

    def is_owl_carousel(self):
        return self.row_type == rowtypes.OWLCAROUSEL

    def is_logo_owl_carousel(self):
        return self.row_type == rowtypes.LOGOCAROUSEL

    def is_breadcrumb_3(self):
        return self.row_type == rowtypes.BREADCRUMB3

    def is_basic_map(self):
        return self.row_type == rowtypes.BASICMAP

    def is_youtube_video(self):
        return self.row_type == rowtypes.YOUTUBEVIDEO

    def is_masonry(self):
        return self.row_type == rowtypes.MASONRY

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Row")
        verbose_name_plural = _("Rows")
        order_with_respect_to = "unifypage"

class RowToPage(Orderable):
    unifypage = models.ForeignKey(UnifyPage, related_name="toRows")
    row = models.ForeignKey(Row, related_name="toUnifypages")

    def edit_row(self):
        return self.row.edit_self()

    edit_row.allow_tags = True

    def edit_page(self):
        return self.unifypage.edit_self()

    edit_page.allow_tags = True


class Element(Orderable):
    """
    A user-built element
    """

    row = models.ForeignKey(Row, related_name="elements")
    element_type = models.IntegerField(_("Type"), choices=elementtypes.NAMES)
    title = models.CharField(_("Title"), max_length=50, blank=True)
    content = RichTextField(_("Main Content"), blank=True)
    icon_class = models.CharField(_("Icon class"), max_length=50, blank=True, \
            help_text=_('One of the available icons for ' \
            '<a href="https://htmlstream.com/preview/unify-v1.9.7/' \
            'shortcode_icon_general.html">unify</a>, for Font awesome add fa before (ex:' \
            'fa  fa-gg)'))
    icon_url = models.CharField(_("Icon URL"), max_length=200, blank=True)
    size = models.IntegerField(_("Size"), default=0,
            help_text=_('Row are separated in 12 columns, this is the number'\
                    'of columns (0 for automatic/equal for each elements)'\
                    '<a href='\
                    '"http://getbootstrap.com/css/#grid-example-basic">'\
                    ' help</a>'))
    size_sm = models.IntegerField(_("Size (~tablet)"), default=0)
    size_xs = models.IntegerField(_("Size (~mobile)"), default=0)
    is_formula = models.BooleanField(_("Formula"), default=False,
            help_text=_("Contains a formula"))
    # can_disappear = models.BooleanField(_("Can Disappear"), default=False,
    #         help_text=_("If true the content will disappear if screen "
    #                     "width is reduced."))
    more_url = models.CharField(_("Link to more(elem)"), max_length=200,
            blank=True)

    action = models.CharField(_("Link to send"), max_length=200, blank=True)
    button_label = models.CharField(_("Button Label"), max_length=200,
            blank=True)
    css_class = models.CharField("CSS Class", max_length=200, blank=True,
            help_text='To potentially  add a CSS class to the englobing div')


    def edit_row(self):
        return self.row.edit_self()

    edit_row.allow_tags = True

    def edit_self(self):
        """
        Returns a link to this item change form
        """
        if self.id:
            return '<a href="%s">' \
                'Details</a>' % admin_url(self.__class__, "change",
                self.id)
        return ''

    edit_self.allow_tags = True

    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")

    def pfcontent(self):
        if self.is_formula:
            return self.formula()
        else:
            return self.content

    def icon(self):
        result = ''
        if self.icon_class != "":
            result += '<i class="icon icon-lg center-block ' + \
                    self.icon_class + '"></i>'
        if self.icon_url != "":
            result += '<img src="' + self.icon_url + '" style="width:50px;">'
        return result

    def formula(self):
        result = self.content
        if "-CoffeesSinceCreation-" in result:
            result = result.replace("-CoffeesSinceCreation-",
                    str(numpy.busday_count(date(2009, 8, 1),date.today())*10))
        if "-WorkingHoursSinceCreation-" in result:
            result = result.replace("-WorkingHoursSinceCreation-",
                    str(numpy.busday_count(date(2009, 8, 1),date.today())*8))
        if "-WholeTotalAttendees-" in result:
            totalAttendees = 0
            for event in Event.objects.filter(end_date__lt=date.today()):
                totalAttendees += event.attendee_number
            result = result.replace("-WholeTotalAttendees-",
                    str(totalAttendees))
        if "-NbOrganisations-" in result:
            organisations = 0
            for account in Account.objects.filter(opportunity_ratio__gte=1):
                organisations += 1
            result = result.replace("-NbOrganisations-",
                    str(organisations))

        return result

    def get_testimonial_block(self, lang):
        block = ''
        if self.is_formula:
            block += '<div class="row">'
            titles = self.title.split(',')
            for title in titles:
                num = int(title)
                block += '<div class="col-md-'
                value = 12//len(titles)
                if value == 0:
                    value = 1
                block += str(value)
                block += ' col-sm-'
                value = 24//len(titles)
                if value > 6:
                    value = 12
                elif value == 0:
                    value = 1
                block += str(value)
                block += ' col-xs-'
                value = 48//len(titles)
                if value > 6:
                    value = 12
                elif value == 0:
                    value = 1
                block += str(value)
                block += ' margin-bottom-20">'
                block += '<div class="testimonials-info rounded-bottom">'
                block += '<div class="testimonials-desc">'
                testis = Testimonial.objects.filter(ranking=1,lang_code=lang). \
                            order_by('creation_date', 'contact_name')
                if testis.count() > int(num):
                    testi = testis[int(num)]
                else:
                    testis2 = Testimonial.objects.filter(ranking=2,
                            lang_code=lang).order_by('creation_date',
                                    'contact_name')
                    if testis2.count() > int(num) - testis.count():
                        testi = testis2[int(num) - testis.count()]
                    else:
                        testis3 = Testimonial.objects.filter(ranking=1,
                                lang_code='en').order_by('creation_date',
                                        'contact_name')
                        if testis3.count() > int(num) - testis2.count():
                            testi = testis3[int(num) - testis2.count()]
                        else:
                            return ''
                block += '<p><i>' + testi.text + '</i></p>'
                block += '<small>' + testi.contact_title + '</small>'
                block += '</div>'
                block += '</div>'
                block += '</div>'
            block += '</div>'
        else:
            block += '<div class="testimonials-desc">'
            if self.icon_class != "":
                block += '<i class="' + self.icon_class + '"></i>'
            elif self.icon_url != "":
                block += '<img src="' + self.icon_url + '" style="width:50px;">'
            block += '<p>' + self.content + '</p>'
            block += '<small>' + self.title + '</small>'
            block += '</div>'
        return block

    def get_colums_values(self, elemnb):
        values = 'col-md-'
        if self.size == 0:
            value = 12//elemnb
            if value == 0:
                value = 1
        else:
            value = self.size
        values += str(value) + ' col-sm-'
        if self.size_sm == 0:
            value = 24//elemnb
            if value > 6:
                value = 12
            elif value == 0:
                value = 1
        else:
            value = self.size_sm
        values += str(value) + ' col-xs-'
        if self.size_xs == 0:
            value = 48//elemnb
            if value > 6:
                value = 12
            elif value == 0:
                value = 1
        else:
            value = self.size_xs
        values += str(value)
        return values

    def is_row_dependant(self):
        return self.element_type == elementtypes.ROWDEPENDANT

    def is_box(self):
        return self.element_type == elementtypes.BOX

    def is_image(self):
        return self.element_type == elementtypes.IMAGE

    def is_offer(self):
        return self.element_type == elementtypes.OFFER

    def is_counter(self):
        return self.element_type == elementtypes.COUNTER

    def is_progress_bar_v(self):
        return self.element_type == elementtypes.PROGRESSBARV

    def is_testimonial(self):
        return self.element_type == elementtypes.TESTIMONIALS

    def is_course_block(self):
        return self.element_type == elementtypes.COURSEBLOCK

    def is_blog_post_block(self):
        return self.element_type == elementtypes.BLOGPOSTBLOCK

    def is_blockgrid_2(self):
        return self.element_type == elementtypes.BLOCKGRID2

    def is_form(self):
        return self.element_type == elementtypes.FORM

    def is_image_zoom(self):
        return self.element_type == elementtypes.IMAGEZOOM

    def __str__(self):
        return self.title


class Input(Orderable):
    """
    A form input
    """

    element = models.ForeignKey(Element, related_name="inputs")
    input_type = models.IntegerField(_("Type"), choices=inputtypes.NAMES)
    name = models.CharField(_("Name"), max_length=200, blank=True)
    value = models.CharField(_("Default Value"), max_length=200, blank=True)
    label = models.CharField(_("Label"), max_length=200, blank=True)
    placeholder = models.CharField(_("Placeholder"), max_length=200, blank=True)
    required = models.BooleanField(_("Required"), default=True)
    icon_class = models.CharField(_("Icon Class"), max_length=200, blank=True)
    rows = models.IntegerField(_("Number of rows"), null=True, blank=True)
    size = models.IntegerField(_("Size(1-12)"), default=12)

    class Meta:
        verbose_name = _("Input")
        verbose_name_plural = _("Inputs")

    def get_type(self):
        if self.input_type == inputtypes.TEXTINPUT:
            return 'text'
        elif self.input_type == inputtypes.TEXTAREA:
            return 'textarea'
        elif self.input_type == inputtypes.EMAIL:
            return 'email'
        elif self.input_type == inputtypes.CHECKBOX:
            return 'checkbox'
        else:
            return 'text'

    def label_type(self):
        if (self.input_type == inputtypes.TEXTINPUT or
            self.input_type == inputtypes.EMAIL):
            return 'input'
        elif self.input_type == inputtypes.TEXTAREA:
            return 'textarea'
        elif self.input_type == inputtypes.CHECKBOX:
            return 'checkbox'
        else:
            return 'input'

