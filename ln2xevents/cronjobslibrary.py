from ln2xevents.models import EventPage, CoursePage, PageContent, MarketingContent, LnxImage
from ln2xsalesforce.models import Events, Course

from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED

from django_cron import CronJobBase, Schedule

import datetime, requests, time, math
from moneyed import Money


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
            print('Update salesforce' + datetime.datetime.now().ctime())
#           # Getting authentification token
#           r = requests.get('https://portal.ln2x.com/rest/2.0/login?'
#                   'un=django&pw=s55AD3HWeKa7')
#           jsonResponse = r.json()
#           if jsonResponse['IsSuccess'] == False:
#               print('Authentification Failed on ' +
#                       datetime.datetime.now().ctime())
#           else:
#               token = jsonResponse['SessionId']
#               headers = {
#                       'Authorization': token,
#                       'Content-Type': 'application/json'
#                       }

#               # Getting courses complete
#               url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
#                       + 'SELECT Id' \
#                       + ', ModifiedOn' \
#                       + ', Category__c' \
#                       + ', Course_Banner__c' \
#                       + ', Description__c' \
#                       + ', isPublishedOnWebsite__c' \
#                       + ', Language__c' \
#                       + ', Name' \
#                       + ', Target_Delegates__c' \
#                       + ', Thumb__c' \
#                       + ' FROM Force.Force__Course__c '

#               r = requests.get(url, headers=headers)
#               r.encoding = 'utf-8'

#               receivedAt = datetime.datetime.now()

#               courses = r.json()["Records"]

#               for course in courses:
#                   if not 'Id' in course:
#                       continue
#                   coursePages = CoursePage.objects.filter(salesforce_id=course['Id'])
#                   isNew = False
#                   if coursePages.count() > 0:
#                       coursePage = coursePages.first()
#                   else:
#                       coursePage = CoursePage(salesforce_id=course['Id'])
#                       isNew = True

#                   if True: # isNew or ('ModifiedOn' in course and \
#                           #course['ModifiedOn'] > coursePage.last_sync.timestamp()):
#                       coursePage.gen_description = False
#                       coursePage.in_sitemap = False
#                       if 'isPublishedOnWebsite__c' in course:
#                           if course['isPublishedOnWebsite__c']:
#                               coursePage.status = CONTENT_STATUS_PUBLISHED
#                           else:
#                               coursePage.status = CONTENT_STATUS_DRAFT
#                       if 'Name' in course:
#                           coursePage.title = course['Name']
#                       if 'Language__c' in course:
#                           coursePage.lang_code = \
#                                  langNameToCode(course['Language__c'])
#                       if 'Category__c' in course:
#                           coursePage.category = \
#                                  course['Category__c']
#                       if 'Course_Banner__c' in course:
#                           coursePage.banner = \
#                                   course['Course_Banner__c']
#                       if 'Target_Delegates__c' in course:
#                           coursePage.target_delegates = \
#                                   course['Target_Delegates__c']
#                       if 'Thumb__c' in course:
#                           coursePage.thumb = \
#                                   course['Thumb__c']
#                       if 'Description__c' in course:
#                           coursePage.description = \
#                                   course['Description__c']

#                       coursePage.last_synch = receivedAt
#                       coursePage.save()

#               print('courses OK')


#               # Getting events complete
#               url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
#                       + 'SELECT Id' \
#                       + ', ModifiedOn' \
#                       + ', Attendees_Total__c' \
#                       + ', Course__c' \
#                       + ', CurrencyIsoCode' \
#                       + ', Display_Agenda_Days__c' \
#                       + ', Display_session_times__c' \
#                       + ', Early_Bird_Deadline__c' \
#                       + ', Event_Description__c' \
#                       + ', Event_End_Date__c' \
#                       + ', Event_External_NAME__c' \
#                       + ', Event_Macro_Region__c' \
#                       + ', Event_Start_Date__c' \
#                       + ', Event_Ticket_Price__c' \
#                       + ', Event_Times__c' \
#                       + ', EventURL__c' \
#                       + ', Geolocation__Latitude__s' \
#                       + ', Geolocation__Longitude__s' \
#                       + ', Group_Discount__c' \
#                       + ', isPublishedOnWebsite__c' \
#                       + ', Language__c' \
#                       + ', Location_Thumb__c' \
#                       + ', Name' \
#                       + ', Speaker_Intro_Text__c' \
#                       + ', Sponsor_Intro_Text__c' \
#                       + ', Sponsor_Listing_Custom_Title__c' \
#                       + ', Standard_Price__c' \
#                       + ', Status__c' \
#                       + ', Terms_Conditions__c' \
#                       + ', Address__c' \
#                       + ', Venue_City__c' \
#                       + ', Venue_Country__c' \
#                       + ', Venue_Description__c' \
#                       + ', Venue_Name__c' \
#                       + ', Web_Default_Seat_Left__c' \
#                       + ' FROM Force.Force__Events__c '

#               r = requests.get(url, headers=headers)
#               r.encoding = 'utf-8'

#               receivedAt = datetime.datetime.now()

#               events = r.json()["Records"]

            for event in Events.objects.all():
                eventPages = EventPage.objects.filter(
                        salesforce_id=event.id)
                isNew = False
                if eventPages.count() > 0:
                    if event.is_deleted or event.status == "Failed":
                        eventPages.first.delete()
                        continue
                    else:
                        eventPage = eventPages.first()
                else:
                    if event.is_deleted or event.status == "Failed":
                        continue
                    else:
                        eventPage = EventPage(salesforce_id=event.id)
                        isNew = True

                if True: # isNew or event.modified_on > eventPage.last_sync.timestamp()):

                    eventPage.gen_description = False
                    eventPage.in_sitemap = False
                    if event.is_published_on_website:
                        eventPage.status = CONTENT_STATUS_PUBLISHED
                    else:
                        eventPage.status = CONTENT_STATUS_DRAFT
                    eventPage.title = event.name
                    eventPage.course = CoursePage.objects \
                            .filter(salesforce_id=event.course) \
                            .first()
                    eventPage.lang_code = \
                           langNameToCode(event.language)
                    eventPage.macro_region = \
                           event.event_macro_region
#                   if 'Event_Description__c' in event:
#                       eventPage.description = \
#                               event['Event_Description__c']
#                   else:
#                       eventPage.description = ''
#                   if 'Terms_Conditions__c' in event:
#                       eventPage.terms_conditions = \
#                               event['Terms_Conditions__c']
#                   if 'Event_Start_Date__c' in event:
#                       eventPage.start_date = datetime.datetime.strptime(
#                           event['Event_Start_Date__c'], \
#                                   "%Y-%m-%dT%H:%M:%S" )
#                   if 'Early_Bird_Deadline__c' in event:
#                       eventPage.early_bird_deadline = \
#                               datetime.datetime.strptime( \
#                               event['Early_Bird_Deadline__c'], \
#                                   "%Y-%m-%dT%H:%M:%S" )
#                   if 'Event_End_Date__c' in event:
#                       eventPage.end_date = datetime.datetime.strptime(
#                           event['Event_End_Date__c'], \
#                                   "%Y-%m-%dT%H:%M:%S" )
#                   if 'Display_Agenda_Days__c' in event:
#                       eventPage.display_agenda_days = \
#                               event['Display_Agenda_Days__c']
#                   if 'Display_session_times__c' in event:
#                       eventPage.display_session_times = \
#                               event['Display_session_times__c']
#                   if 'Event_Times__c' in event:
#                       eventPage.times = event['Event_Times__c']
#                   if 'EventURL__c' in event:
#                       eventPage.slug = event['EventURL__c']
#                   if 'Web_Default_Seat_Left__c' in event:
#                       eventPage.seats_left = max(\
#                               event['Web_Default_Seat_Left__c'], \
#                               0)
#                   if 'Attendees_Total__c' in event:
#                       eventPage.attendee_number = \
#                               event['Attendees_Total__c']
#                   if 'Event_Ticket_Price__c' in event and \
#                           'CurrencyIsoCode' in event:
#                       eventPage.ticket_price = \
#                               Money(event['Event_Ticket_Price__c'], \
#                               event['CurrencyIsoCode'])
#                   if 'Standard_Price__c' in event and \
#                           'CurrencyIsoCode' in event:
#                       eventPage.standard_price = \
#                               Money(event['Standard_Price__c'], \
#                               event['CurrencyIsoCode'])
#                   if 'Group_Discount__c' in event:
#                       eventPage.nb_group_discount = \
#                               event['Group_Discount__c']
#                   if 'Address__c' in event:
#                       eventPage.address = \
#                               event['Address__c']
#                   if 'Venue_City__c' in event:
#                       eventPage.city = \
#                               event['Venue_City__c']
#                   if 'Venue_Country__c' in event:
#                       eventPage.country = \
#                               event['Venue_Country__c']
#                   if 'Venue_Description__c' in event:
#                       eventPage.venue_description = \
#                               event['Venue_Description__c']
#                   if 'Venue_Name__c' in event:
#                       eventPage.venue_name = \
#                               event['Venue_Name__c']
#                   if 'Geolocation__Latitude__s' in event:
#                       eventPage.latitude = \
#                               event['Geolocation__Latitude__s']
#                   if 'Geolocation__Longitude__s' in event:
#                       eventPage.longitude = \
#                               event['Geolocation__Longitude__s']
#                   if 'Location_Thumb__c' in event:
#                       eventPage.location_thumb = \
#                               event['Location_Thumb__c']
#                   if 'Speaker_Intro_Text__c' in event:
#                       eventPage.speaker_intro = \
#                               event['Speaker_Intro_Text__c']
#                   if 'Sponsor_Intro_Text__c' in event:
#                       eventPage.sponsor_title = \
#                               event['Sponsor_Intro_Text__c']
#                   if 'Sponsor_Listing_Custom_Title__c' in event:
#                       eventPage.sponsor_list_title = \
#                               event['Sponsor_Listing_Custom_Title__c']
#                   eventPage.last_synch = receivedAt
                    eventPage.save()

            print('events OK')


#               # Getting contents
#               url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
#                       + 'SELECT Id' \
#                       + ', ModifiedOn' \
#                       + ', Content_Type__c' \
#                       + ', ContentReference__c' \
#                       + ', Language__c' \
#                       + ', Rich_Text__c' \
#                       + ', Title__c' \
#                       + ' FROM Force.Force__Content__c '

#               r = requests.get(url, headers=headers)
#               r.encoding = 'utf-8'

#               receivedAt = datetime.datetime.now()

#               contents = r.json()["Records"]

#               for content in contents:
#                   if not 'Id' in content:
#                       continue
#                   pageContents = PageContent.objects. \
#                           filter(salesforce_id=content['Id'])
#                   isNew = False
#                   if pageContents.count() > 0:
#                       pageContent = pageContents.first()
#                   else:
#                       pageContent = PageContent(salesforce_id=content['Id'])
#                       isNew = True

#                   if True: # isNew or ('ModifiedOn' in content and \
#                           #content['ModifiedOn'] > pageContent.last_sync.timestamp()):

#                       if 'Title__c' in content:
#                           pageContent.title = \
#                                   content['Title__c']
#                       if 'Rich_Text__c' in content:
#                           pageContent.rich_text = content['Rich_Text__c']
#                       if 'Content_Type__c' in content:
#                           pageContent.content_type = \
#                                  content['Content_Type__c']
#                       if 'ContentReference__c' in content:
#                           pageContent.reference = \
#                                  content['ContentReference__c']
#                       if 'Language__c' in content:
#                           pageContent.lang_code = \
#                                  langNameToCode(content['Language__c'])

#                       pageContent.last_synch = receivedAt
#                       pageContent.save()

#               print('contents OK')

#               # Getting marketing contents
#               url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
#                       + 'SELECT Id' \
#                       + ', ModifiedOn' \
#                       + ', Course__c' \
#                       + ', Content__c' \
#                       + ', Event__c' \
#                       + ' FROM Force.Force__Marketing_Content__c '

#               r = requests.get(url, headers=headers)
#               r.encoding = 'utf-8'

#               receivedAt = datetime.datetime.now()

#               marketingContents = r.json()["Records"]

#               for marketingContent in marketingContents:
#                   if not 'Id' in marketingContent:
#                       continue
#                   marketingContents = MarketingContent.objects. \
#                           filter(salesforce_id=marketingContent['Id'])
#                   isNew = False
#                   if marketingContents.count() > 0:
#                       marketContent = marketingContents.first()
#                   else:
#                       marketContent = \
#                               MarketingContent( \
#                               salesforce_id=marketingContent['Id'])
#                       isNew = True

#                   if True: # isNew or ('ModifiedOn' in content and \
#                           #content['ModifiedOn'] > \
#                           #marketingContent.last_sync.timestamp()):

#                       if 'Course__c' in marketingContent:
#                           marketContent.course = CoursePage.objects \
#                                   .filter(salesforce_id=marketingContent['Course__c']) \
#                                   .first()

#                       if 'Event__c' in marketingContent:
#                           marketContent.event = EventPage.objects \
#                                   .filter(salesforce_id=marketingContent['Event__c']) \
#                                   .first()

#                       if 'Content__c' in marketingContent:
#                           marketContent.content = PageContent.objects \
#                                   .filter(salesforce_id=marketingContent['Content__c']) \
#                                   .first()

#                       marketContent.last_synch = receivedAt
#                       marketContent.save()

#               print('Mark contents OK')



#               # Getting images
#               url = 'https://portal.ln2x.com/rest/2.0/query?q=' \
#                       + 'SELECT Id' \
#                       + ', ModifiedOn' \
#                       + ', LNX_Image_URL__c' \
#                       + ', ImageType__c' \
#                       + ', MarketingContent__c' \
#                       + ' FROM Force.Force__LNXImage__c '

#               r = requests.get(url, headers=headers)
#               r.encoding = 'utf-8'

#               receivedAt = datetime.datetime.now()

#               mlnxImages = r.json()["Records"]

#               for mlnxImage in mlnxImages:
#                   if not 'Id' in mlnxImage:
#                       continue
#                   lnxImages = LnxImage.objects. \
#                           filter(salesforce_id=mlnxImage['Id'])
#                   isNew = False
#                   if lnxImages.count() > 0:
#                       lnxImage = lnxImages.first()
#                   else:
#                       lnxImage = \
#                               LnxImage( \
#                               salesforce_id=mlnxImage['Id'])
#                       isNew = True

#                   if True: # isNew or ('ModifiedOn' in content and \
#                           #content['ModifiedOn'] > \
#                           #lnxImage.last_sync.timestamp()):

#                       if 'LNX_Image_URL__c' in mlnxImage:
#                           lnxImage.url = mlnxImage['LNX_Image_URL__c']

#                       if 'ImageType__c' in mlnxImage:
#                           lnxImage.image_type = mlnxImage['ImageType__c']


#                       if 'MarketingContent__c' in mlnxImage:
#                           lnxImage.mark_content = MarketingContent.objects \
#                                   .filter(salesforce_id= \
#                                           mlnxImage['MarketingContent__c']) \
#                                   .first()


#                       lnxImage.last_synch = receivedAt
#                       lnxImage.save()

#               print('LNX Images OK')

#               print('end')
        except Exception as e: print(e)

