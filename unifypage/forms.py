from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail

from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from ln2xevents.models import EventPage, CoursePage
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget as PhoneNumberPrefixWidgetBase
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.accounts.forms import ProfileForm, LoginForm
from captcha.fields import CaptchaField


class PhoneNumberPrefixWidget(PhoneNumberPrefixWidgetBase):
    def value_from_datadict(self, data, files, name):
        values = super(PhoneNumberPrefixWidgetBase, self).value_from_datadict(
                data, files, name)
        if all(values):
            return '%s.%s' % tuple(values)
        return ""

class ContactForm(forms.Form):
    first_name = forms.CharField(label=_("First Name"), max_length=100)
    last_name = forms.CharField(label=_("Last Name"), max_length=100)
    job_title = forms.CharField(label=_("Job title"), max_length=100)
    company_name = forms.CharField(label=_("Organisation/Company Name"),
            max_length=100)
    email_address = forms.EmailField(label=_("Email address"), )
    event = forms.ModelChoiceField(label=_("Event"),
            queryset=EventPage.objects.filter(status=CONTENT_STATUS_PUBLISHED),
            required=False)
    course = forms.ModelChoiceField(label=_("Course"),
            queryset=CoursePage.objects.filter(status=CONTENT_STATUS_PUBLISHED),
            required=False)
    phone_number = PhoneNumberField(label=_("Phone number"), required=False,
            widget=PhoneNumberInternationalFallbackWidget)
    comments = forms.CharField(label=_("Comments"), widget=forms.Textarea(attrs={'rows':2,}),
            required=False)


def process(form):
    if form.is_valid():
        firstName = form.cleaned_data['first_name']
        lastName = form.cleaned_data['last_name']
        company  = form.cleaned_data['company_name']
        job  = form.cleaned_data['job_title']
        formEmail  = form.cleaned_data['email_address']
        event  = form.cleaned_data['event']
        course  = form.cleaned_data['course']
        phoneNumber  = form.cleaned_data['phone_number']
        comments  = form.cleaned_data['comments']

        # Email to staff
        subject = firstName + ' ' + lastName + ' showed interrest in '
        if event:
            subject += 'the event ' + event.title
        elif course:
            subject += 'the course ' + course.title
        else:
            subject += 'the website'
        body = 'Name : ' + firstName + ' ' + lastName
        body += '<br />Company : ' + company
        body += '<br />Job : ' + job
        if phoneNumber:
            body += '<br />Phone number : ' + str(phoneNumber)
        if comments:
            body += '<br />Comments : ' + comments
        if event:
            body += '<br />Relative event : ' + event.title + \
                    '<br /><a href="https://na1.salesforce.com/' + \
                    event.salesforce_id + '">SalesForce</a>' + \
                    '<br /><a href="https://portal.ln2x.com/' + \
                    event.salesforce_id + '">Magentrix</a>'
        elif course:
            body += '<br />Relative course : <a href="' + \
                    'https://na1.salesforce.com/' + course.salesforce_id + \
                    '">' + course.title + '</a>'



        send_mail( subject, body, settings.DEFAULT_FROM_EMAIL,
                {settings.DEFAULT_TO_EMAIL,}, html_message=body,
                fail_silently=False )

    else:
        pass

class GuestCommentForm(ThreadedCommentForm):
    def __init__(self, request, *args, **kwargs):
        super(GuestCommentForm, self).__init__(request, *args, **kwargs)
        if not request.user.is_authenticated():
            self.fields['captcha'] = CaptchaField()


class SignUpCaptchaForm(ProfileForm):
    def __init__(self, request, *args, **kwargs):
        super(SignUpCaptchaForm, self).__init__(request, *args, **kwargs)
        self.fields['captcha'] = CaptchaField()

class LogInCaptchaForm(LoginForm):
        captcha = CaptchaField()
