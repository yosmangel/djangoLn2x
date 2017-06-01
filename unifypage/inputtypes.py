from django.utils.translation import ugettext_lazy as _

TEXTINPUT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4

NAMES = (
    (TEXTINPUT, _("Text Input")),
    (TEXTAREA, _("Text Area")),
    (EMAIL, _("Email")),
    (CHECKBOX, _("Checkbox")),
)
