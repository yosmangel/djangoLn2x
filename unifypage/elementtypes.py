from django.utils.translation import ugettext_lazy as _

BOX = 1
IMAGE = 2
OFFER = 3
COUNTER = 4
ROWDEPENDANT = 5
PROGRESSBARV = 6
TESTIMONIALS = 7
COURSEBLOCK = 8
FORM = 9
IMAGEZOOM = 10
BLOGPOSTBLOCK = 11

NAMES = (
    (ROWDEPENDANT, _("Row Dependant")),
    (IMAGE, _("Image")),
    (COUNTER, _("Counter")),
    (PROGRESSBARV, _("Vertical Progress Bar")),
    (TESTIMONIALS, _("Testimonials")),
    (BOX, _("Box")),
    (COURSEBLOCK, _("Course Block")),
    (FORM, _("Form")),
    (IMAGEZOOM, _("Image zoom")),
    (BLOGPOSTBLOCK, _("Blog Post Block")),
    #(IMAGE, _("Image")),
    #(OFFER, _("Offer")),
)
