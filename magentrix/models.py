from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_cron import CronJobBase, Schedule

import requests, datetime, time, math

from moneyed import Money


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    attendee_number = models.IntegerField(_("Attendee Number"), blank=True)
    end_date = models.DateField(_("End Date"), null=True)

class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    opportunity_ratio = models.IntegerField(_("Opportunity Ratio"), null=True)

class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(_("Name"), max_length=80)
    description = models.CharField(_("Description"), max_length=32768)
    lang_code = models.CharField(_("Language code"), max_length=2, default="en")
    creation_date = models.DateField(_("Creation Date"), null=True)

class Testimonial(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    contact_name = models.CharField(_("Contact Name"), max_length=100)
    contact_title = models.CharField(_("Contact Title"), max_length=1300)
    text = models.CharField(_("Text"), max_length=32768)
    ranking = models.PositiveSmallIntegerField(_("Ranking"), default=5)
    lang_code = models.CharField(_("Language code"), max_length=2, default="en")
    creation_date = models.DateField(_("Creation Date"), null=True)

def langNameToCode(name):
    if name == 'Spanish':
        return 'es'
    elif name == 'French':
        return 'fr'
    else:
        return 'en'

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 15 # every 15 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'magentrix.updates'    # a unique code

    def do(self):
        try:
            print('Update Magentrix' + datetime.datetime.now().ctime())
            # Getting authentification token
            r = requests.get('https://portal.ln2x.com/rest/2.0/login?'
                    'un=django&pw=s55AD3HWeKa7')
            jsonResponse = r.json()
            if jsonResponse['IsSuccess'] == False:
                print('Authentification Failed on ' +
                        datetime.datetime.now().ctime())
            else:
                token = jsonResponse['SessionId']
                headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                        }
                # Getting events
                url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
                        + 'SELECT Id' \
                        + ', Attendees_Total__c' \
                        + ', Event_End_Date__c' \
                        + ', Status__c' \
                        + ' FROM Force.Force__Events__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                events = r.json()["Records"]

                for mEvent in events:
                    dEvents = Event.objects.filter(id=mEvent['Id'])
                    if dEvents.count() > 0:
                        if 'Status__c' in mEvent and \
                                mEvent['Status__c'] == "Failed":
                            dEvents[0].delete()
                            continue
                        else:
                            dEvent = dEvents[0]
                    else:
                        if 'Status__c' in mEvent and \
                                mEvent['Status__c'] == "Failed":
                            continue
                        else:
                            dEvent = Event(id=mEvent['Id'])
                    dEvent.attendee_number = mEvent['Attendees_Total__c']
                    if 'Event_End_Date__c' in mEvent:
                        dEvent.end_date = datetime.datetime.strptime(
                            mEvent['Event_End_Date__c'], "%Y-%m-%dT%H:%M:%S" )
                    dEvent.save()
                print('events OK')

                # Getting accounts
                url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
                        + 'SELECT Id' \
                        + ', Average_Opportunity_Ratio__c' \
                        + ' FROM Force.Force__Account ' \

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                accounts = r.json()["Records"]

                for mAccount in accounts:
                    dAccounts = Account.objects.filter(id=mAccount['Id'])
                    if dAccounts.count() > 0:
                        dAccount = dAccounts[0]
                    else:
                        dAccount = Account(id=mAccount['Id'])
                    if 'Average_Opportunity_Ratio__c' in mAccount:
                        dAccount.opportunity_ratio = \
                                mAccount['Average_Opportunity_Ratio__c']
                    dAccount.save()
                print('accounts OK')

                # Getting testimonials
                url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
                        + 'SELECT Id' \
                        + ', Authorised__c' \
                        + ', Contact__r.FirstName' \
                        + ', Contact__r.LastName' \
                        + ', Course__r.Language__c' \
                        + ', Contact_Title__c' \
                        + ', Ranking__c' \
                        + ', CreatedOn' \
                        + ', Testimonial_Text__c' \
                        + ' FROM Force.Force__Testimonial__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                testis = r.json()["Records"]

                for mTesti in testis:
                    dTestis = Testimonial.objects.filter(id=mTesti['Id'])
                    if dTestis.count() > 0:
                        if 'Authorised__c' not in mTesti or \
                                ('Authorised__c' in mTesti and \
                                mTesti['Authorised__c'] == "False") \
                                or 'Testimonial_Text__c' not in mTesti \
                                or ('Testimonial_Text__c' in mTesti \
                                and mTesti['Testimonial_Text__c'] == ""):
                            dTestis[0].delete()
                            continue
                        else:
                            dTesti = dTestis[0]
                    else:
                        if 'Authorised__c' not in mTesti or \
                                ('Authorised__c' in mTesti and \
                                mTesti['Authorised__c'] == "False") \
                                or 'Testimonial_Text__c' not in mTesti \
                                or ('Testimonial_Text__c' in mTesti \
                                and mTesti['Testimonial_Text__c'] == ""):
                            continue
                        else:
                            dTesti = Testimonial(id=mTesti['Id'])
                    dTesti.contact_title = mTesti['Contact_Title__c']
                    dTesti.text = mTesti['Testimonial_Text__c']
                    if 'Ranking__c' in mTesti:
                        dTesti.ranking = mTesti['Ranking__c']
                    dTesti.contact_name = mTesti['Contact__r']['FirstName'] \
                            + ' ' + mTesti['Contact__r']['LastName']
                    dTesti.lang_code = langNameToCode(mTesti['Course__r']['Language__c'])
                    if 'CreatedOn' in mTesti:
                        dTesti.creation_date = datetime.datetime.strptime(
                            mTesti['CreatedOn'], "%Y-%m-%dT%H:%M:%S" )


                    dTesti.save()
                print('Testimonials OK')

                print('end')
        except Exception as e: print(e)

