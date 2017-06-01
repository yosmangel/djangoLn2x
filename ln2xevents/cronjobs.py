from ln2xevents.models import EventPage, OldSlug, CoursePage, PageContent, MarketingContent, LnxImage, Testimonial, Speaker, Session, Sponsor

from mezzanine.core.models import CONTENT_STATUS_DRAFT, CONTENT_STATUS_PUBLISHED

from django.utils.text import slugify

from django_cron import CronJobBase, Schedule

import datetime, requests, time, math, pytz
from moneyed import Money

def langNameToCode(name):
    if name == 'Spanish':
        return 'es'
    elif name == 'French':
        return 'fr'
    else:
        return 'en'

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 14 # every 15 mins

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'salesforce.updates'    # a unique code

    def do(self):
        try:
            calls = 0
            print('Update salesforce' + datetime.datetime.now(datetime.timezone.utc).ctime())
            # Getting authentification token
            url = 'https://login.salesforce.com/services/oauth2/token'
            data = { "grant_type": "password",
                    "client_id": \
                            "3MVG99OxTyEMCQ3h4Z4bxy48lW5JQOQUdW06y4xLFWzooJ." \
                            "8N0SrcvD4W6RVo18LztVucQE2beGHGn8BeQKwT",
                    "client_secret": "6359050871463269979",
                    "username": "daisy@liquidnexxus.com",
                    "password": "Almendra112",
                    }

            r = requests.post(url, data=data)
            jsonResponse = r.json()
            if 'access_token' not in jsonResponse:
                print('Authentification Failed on ' +
                        datetime.datetime.now(datetime.timezone.utc).ctime())
            else:
                token = jsonResponse['access_token']
                headers = {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json',
                        'X-PrettyPrint': '1',
                        }

                # Getting courses complete
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Category__c' \
                        + ', Course_Banner__c' \
                        + ', Description__c' \
                        + ', isPublishedOnWebsite__c' \
                        + ', Language__c' \
                        + ', Name' \
                        + ', ProductReference__c' \
                        + ', Target_Delegates__c' \
                        + ', Thumb__c' \
                        + ', Type__c' \
                        + ', Subject_Category__c' \
                        + ', Duration__c' \
                        + ', Agenda__c' \
                        + ', WHO_ATTENDS__c' \
                        + ', Objectives__c' \
                        + ', Pre_requisites__c' \
                        + ', REF_Source__c' \
                        + ', Languages_Available__c' \
                        + ', Course_Level__c' \
                        + ' FROM Course__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                courses = response["records"]
                stop = False

                while not stop:
                    for course in courses:
                        if not 'Id' in course:
                            continue
                        coursePages = CoursePage.objects.filter(salesforce_id=course['Id'])
                        isNew = False
                        if coursePages.count() > 0:
                            coursePage = coursePages.first()
                        else:
                            coursePage = CoursePage(salesforce_id=course['Id'])
                            isNew = True

                        if 'SystemModstamp' in course:
                            time = course['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > coursePage.last_sync:
                            coursePage.gen_description = False
                            coursePage.in_sitemap = False
                            if 'isPublishedOnWebsite__c' in course:
                                if course['isPublishedOnWebsite__c']:
                                    coursePage.status = CONTENT_STATUS_PUBLISHED
                                    coursePage.in_sitemap = True
                                else:
                                    coursePage.status = CONTENT_STATUS_DRAFT
                                    coursePage.in_sitemap = False
                            if 'Name' in course:
                                coursePage.title = course['Name']
                                slug = slugify(course['Name'])
                                if not isNew and \
                                        coursePage.slug != slug:
                                            oldslug = OldSlug(
                                                    course_page=coursePage,
                                                    slug=coursePage.slug)
                                            oldslug.save()
                                coursePage.slug = slug
                            if 'Language__c' in course:
                                coursePage.lang_code = \
                                       langNameToCode(course['Language__c'])
                            if 'Category__c' in course:
                                coursePage.delivery_format = \
                                       course['Category__c']
                            if 'Course_Banner__c' in course:
                                coursePage.banner = \
                                        course['Course_Banner__c']
                            if 'Description__c' in course and \
                                    course['Description__c']:
                                coursePage.description = \
                                        course['Description__c']
                            if 'ProductReference__c' in course:
                                coursePage.product_reference = \
                                        course['ProductReference__c']
                            if 'Target_Delegates__c' in course:
                                coursePage.target_delegates = \
                                        course['Target_Delegates__c']
                            if 'Thumb__c' in course:
                                coursePage.thumb = \
                                        course['Thumb__c']
                            if 'Type__c' in course:
                                if course['Type__c'] == 'Mid-Level' or \
                                        course['Type__c'] == 'Licensed Mid-Level':
                                            coursePage.level = 'mid-level'
                                elif course['Type__c'] == 'Advanced' or \
                                        course['Type__c'] == 'Licensed Advanced':
                                            coursePage.level = 'advanced'
                                else:
                                    coursePage.level = 'basic'
                            if 'Subject_Category__c' in course:
                                coursePage.subject_category = \
                                        course['Subject_Category__c']
                            if 'Duration__c' in course:
                                coursePage.duration = \
                                        course['Duration__c']
                            if 'Agenda__c' in course:
                                coursePage.agenda = \
                                        course['Agenda__c']
                            if 'WHO_ATTENDS__c' in course:
                                coursePage.who_attends = \
                                        course['WHO_ATTENDS__c']
                            if 'Objectives__c' in course:
                                coursePage.objectives = \
                                        course['Objectives__c']
                            if 'Pre_requisites__c' in course:
                                coursePage.pre_requisites = \
                                        course['Pre_requisites__c']
                            if 'REF_Source__c' in course:
                                coursePage.ref_source = \
                                        course['REF_Source__c']
                            if 'Languages_Available__c' in course:
                                coursePage.languages_availables = \
                                        course['Languages_Available__c']
                            if 'Course_Level__c' in course:
                                coursePage.course_level = \
                                        course['Course_Level__c']

                            coursePage.last_sync = receivedAt
                            coursePage.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        courses = response["records"]

                print('courses OK')


                # Getting events complete
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Attendees_Total__c' \
                        + ', Course__c' \
                        + ', CurrencyIsoCode' \
                        + ', Display_Agenda_Days__c' \
                        + ', Display_session_times__c' \
                        + ', Early_Bird_Deadline__c' \
                        + ', Event_Description__c' \
                        + ', Event_End_Date__c' \
                        + ', Event_External_NAME__c' \
                        + ', Event_Macro_Region__c' \
                        + ', Event_Start_Date__c' \
                        + ', Event_Ticket_Price__c' \
                        + ', Event_Times__c' \
                        + ', EventURL__c' \
                        + ', Geolocation__Latitude__s' \
                        + ', Geolocation__Longitude__s' \
                        + ', Group_Discount__c' \
                        + ', isPublishedOnWebsite__c' \
                        + ', Language__c' \
                        + ', Location_Thumb__c' \
                        + ', Name' \
                        + ', Sold_Out__c' \
                        + ', Speaker_Intro_Text__c' \
                        + ', Sponsor_Intro_Text__c' \
                        + ', Sponsor_Listing_Custom_Title__c' \
                        + ', Standard_Price__c' \
                        + ', Status__c' \
                        + ', Terms_Conditions__c' \
                        + ', Venue_Address__c' \
                        + ', Venue_City__c' \
                        + ', Venue_Country__c' \
                        + ', Venue_Description__c' \
                        + ', Venue_Name__c' \
                        + ', Web_Default_Seat_Left__c' \
                        + ' FROM Events__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                events = response["records"]
                stop = False

                while not stop:
                    for event in events:
                        if not 'Id' in event:
                            continue
                        eventPages = EventPage.objects.filter(salesforce_id=event['Id'])
                        isNew = False
                        if eventPages.count() > 0:
                            if 'Status__c' in event and \
                                    event['Status__c'] == "Failed":
                                eventPages.first().delete()
                                continue
                            else:
                                eventPage = eventPages.first()
                        else:
                            if 'Status__c' in event and \
                                    event['Status__c'] == "Failed":
                                continue
                            else:
                                eventPage = EventPage(salesforce_id=event['Id'])
                                isNew = True

                        if 'SystemModstamp' in event:
                            time = event['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > eventPage.last_sync:

                            eventPage.gen_description = False
                            eventPage.in_sitemap = False
                            if 'isPublishedOnWebsite__c' in event:
                                if event['isPublishedOnWebsite__c']:
                                    eventPage.status = CONTENT_STATUS_PUBLISHED
                                    eventPage.in_sitemap = True
                                else:
                                    eventPage.status = CONTENT_STATUS_DRAFT
                                    eventPage.in_sitemap = False
                            if 'Name' in event:
                                eventPage.title = event['Name']
                            if 'Course__c' in event:
                                eventPage.course = CoursePage.objects \
                                        .filter(salesforce_id=event['Course__c']) \
                                        .first()
                            if 'Language__c' in event:
                                eventPage.lang_code = \
                                       langNameToCode(event['Language__c'])
                            if 'Event_Macro_Region_c' in event:
                                eventPage.macro_region = \
                                       event['Event_Macro_Region_c']
                            if 'Event_Description__c' in event and \
                                    event['Event_Description__c'] != None:
                                eventPage.description = \
                                        event['Event_Description__c']
                            else:
                                eventPage.description = ''
                            if 'Terms_Conditions__c' in event:
                                eventPage.terms_conditions = \
                                        event['Terms_Conditions__c']
                            if 'Event_Start_Date__c' in event and \
                                    event['Event_Start_Date__c']:
                                eventPage.start_date = datetime.datetime.strptime(
                                    event['Event_Start_Date__c'], \
                                            "%Y-%m-%d" )
                            if 'Early_Bird_Deadline__c' in event and \
                                    event['Early_Bird_Deadline__c']:
                                eventPage.early_bird_deadline = \
                                        datetime.datetime.strptime( \
                                        event['Early_Bird_Deadline__c'], \
                                            "%Y-%m-%d" )
                            if 'Event_End_Date__c' in event and \
                                    event['Event_End_Date__c']:
                                eventPage.end_date = datetime.datetime.strptime(
                                    event['Event_End_Date__c'], \
                                            "%Y-%m-%d" )
                            if 'Event_Macro_Region__c' in event:
                                eventPage.macro_region = \
                                        event['Event_Macro_Region__c']
                            if 'Display_Agenda_Days__c' in event:
                                eventPage.display_agenda_days = \
                                        event['Display_Agenda_Days__c']
                            if 'Display_session_times__c' in event:
                                eventPage.display_session_times = \
                                        event['Display_session_times__c']
                            if 'Event_Times__c' in event:
                                eventPage.times = event['Event_Times__c']
                            if 'EventURL__c' in event:
                                if not isNew and \
                                        eventPage.slug != event['EventURL__c']:
                                            oldslug = OldSlug(
                                                    event_page=eventPage,
                                                    slug=eventPage.slug)
                                            oldslug.save()
                                eventPage.slug = event['EventURL__c']
                            if 'Web_Default_Seat_Left__c' in event and \
                                    event['Web_Default_Seat_Left__c']:
                                eventPage.seats_left = max(\
                                        event['Web_Default_Seat_Left__c'], \
                                        0)
                            if 'Attendees_Total__c' in event:
                                eventPage.attendee_number = \
                                        event['Attendees_Total__c']
                            if 'Event_Ticket_Price__c' in event and \
                                    event['Event_Ticket_Price__c'] and \
                                    'CurrencyIsoCode' in event and \
                                    event['CurrencyIsoCode']:
                                eventPage.ticket_price = \
                                        Money(event['Event_Ticket_Price__c'], \
                                        event['CurrencyIsoCode'])
                            if 'Standard_Price__c' in event and \
                                    event['Standard_Price__c'] and \
                                    'CurrencyIsoCode' in event and \
                                    event['CurrencyIsoCode']:
                                eventPage.standard_price = \
                                        Money(event['Standard_Price__c'], \
                                        event['CurrencyIsoCode'])
                            if 'Group_Discount__c' in event:
                                eventPage.nb_group_discount = \
                                        event['Group_Discount__c']
                            if 'Venue_Address__c' in event:
                                eventPage.address = \
                                        event['Venue_Address__c']
                            if 'Venue_City__c' in event:
                                eventPage.city = \
                                        event['Venue_City__c']
                            if 'Venue_Country__c' in event:
                                eventPage.country = \
                                        event['Venue_Country__c']
                            if 'Venue_Description__c' in event:
                                eventPage.venue_description = \
                                        event['Venue_Description__c']
                            if 'Venue_Name__c' in event:
                                eventPage.venue_name = \
                                        event['Venue_Name__c']
                            if 'Geolocation__Latitude__s' in event:
                                eventPage.latitude = \
                                        event['Geolocation__Latitude__s']
                            if 'Geolocation__Longitude__s' in event:
                                eventPage.longitude = \
                                        event['Geolocation__Longitude__s']
                            if 'Location_Thumb__c' in event:
                                eventPage.location_thumb = \
                                        event['Location_Thumb__c']
                            if 'Sold_Out__c' in event:
                                eventPage.sold_out = \
                                        event['Sold_Out__c']
                            if 'Speaker_Intro_Text__c' in event:
                                eventPage.speaker_intro = \
                                        event['Speaker_Intro_Text__c']
                            if 'Sponsor_Intro_Text__c' in event:
                                eventPage.sponsor_title = \
                                        event['Sponsor_Intro_Text__c']
                            if 'Sponsor_Listing_Custom_Title__c' in event:
                                eventPage.sponsor_list_title = \
                                        event['Sponsor_Listing' \
                                        '_Custom_Title__c']
                            eventPage.last_sync = receivedAt
                            eventPage.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        events = response["records"]

                print('events OK')

                # Getting sponsors
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Account__r.Name' \
                        + ', Account__r.Account_Custom_Logo__c' \
                        + ', Account__r.Account_Description__c' \
                        + ', Custom_Description__c' \
                        + ', Custom_Logo__c' \
                        + ', Custom_Name__c' \
                        + ', Name' \
                        + ', Event__c' \
                        + ', Sponsor_Type__c' \
                        + ' FROM Sponsor__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                sponsors = response["records"]
                stop = False

                while not stop:
                    for sponsor in sponsors:
                        if not 'Id' in sponsor:
                            continue
                        sponsors = Sponsor.objects. \
                                filter(salesforce_id=sponsor['Id'])
                        isNew = False
                        if sponsors.count() > 0:
                            dsponsor = sponsors.first()
                        else:
                            dsponsor = \
                                    Sponsor( \
                                    salesforce_id=sponsor['Id'])
                            isNew = True

                        if 'SystemModstamp' in sponsor:
                            time = sponsor['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > dsponsor.last_sync:

                            if 'Event__c' in sponsor:
                                dsponsor.event = EventPage.objects \
                                        .filter(salesforce_id=sponsor['Event__c']) \
                                        .first()

                            if 'Account__r' in sponsor:
                                if 'Name' in sponsor['Account__r']:
                                    dsponsor.account_name = \
                                            sponsor['Account__r']['Name']
                                if 'Account_Custom_Logo__c' in \
                                        sponsor['Account__r']:
                                    dsponsor.account_logo = \
                                            sponsor['Account__r'] \
                                            ['Account_Custom_Logo__c']
                                if 'Account_Description__c' in \
                                        sponsor['Account__r']:
                                    dsponsor.account_description = \
                                            sponsor['Account__r'] \
                                            ['Account_Description__c']

                            if 'Custom_Description__c' in sponsor:
                                dsponsor.custom_description = \
                                        sponsor['Custom_Description__c']

                            if 'Custom_Logo__c' in sponsor:
                                dsponsor.custom_logo = sponsor['Custom_Logo__c']

                            if 'Custom_Name__c' in sponsor:
                                dsponsor.custom_name = sponsor['Custom_Name__c']

                            if 'Name' in sponsor:
                                dsponsor.name = \
                                        sponsor['Name']

                            if 'Sponsor_Type__c' in sponsor:
                                dsponsor.sponsor_type = \
                                        sponsor['Sponsor_Type__c']

                            dsponsor.last_sync = receivedAt
                            dsponsor.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        sponsors = response["records"]

                print('Sponsors OK')


                # Getting sessions
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Course__c' \
                        + ', Event__c' \
                        + ', Content_Reference__c' \
                        + ', Published__c' \
                        + ', Session_Abstract__c' \
                        + ', Session_Code__c' \
                        + ', Session_End_Time__c' \
                        + ', Session_Format__c' \
                        + ', Session_Slot_Number__c' \
                        + ', Session_Start_Time__c' \
                        + ', Session_Take__c' \
                        + ', Session_Theme__c' \
                        + ', Sponsored__c' \
                        + ', Session_Public_Name__c' \
                        + ', SessionImage__c' \
                        + ' FROM Session__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                sessions = response["records"]
                stop = False

                while not stop:
                    for session in sessions:
                        if not 'Id' in session:
                            continue
                        sessions = Session.objects. \
                                filter(salesforce_id=session['Id'])
                        isNew = False
                        if sessions.count() > 0:
                            dsession = sessions.first()
                        else:
                            dsession = \
                                    Session( \
                                    salesforce_id=session['Id'])
                            isNew = True

                        if 'SystemModstamp' in session:
                            time = session['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > dsession.last_sync:

                            if 'Course__c' in session:
                                dsession.course = CoursePage.objects \
                                        .filter(salesforce_id= \
                                        session['Course__c']) \
                                        .first()

                            if 'Event__c' in session:
                                dsession.event = EventPage.objects \
                                        .filter(
                                                salesforce_id=
                                                session['Event__c']) \
                                        .first()

                            if 'Content_Reference__c' in session:
                                dsession.content_reference = \
                                        session['Content_Reference__c']

                            if 'Published__c' in session:
                                dsession.published = session['Published__c']

                            if 'Session_Abstract__c' in session:
                                dsession.abstract = \
                                        session['Session_Abstract__c']

                            if 'Session_Code__c' in session:
                                dsession.code = session['Session_Code__c']

                            if 'Session_End_Time__c' in session and \
                                    session['Session_End_Time__c']:
                                dsession.end_time = \
                                        datetime.datetime.strptime( \
                                        session['Session_End_Time__c'], \
                                        "%Y-%m-%dT%H:%M:%S.%f%z" )

                            if 'Session_Format__c' in session:
                                dsession.session_format = \
                                        session['Session_Format__c']

                            if 'Session_Slot_Number__c' in session:
                                dsession.slot_number = \
                                        session['Session_Slot_Number__c']

                            if 'Session_Start_Time__c' in session and \
                                    session['Session_Start_Time__c']:
                                dsession.start_time = \
                                        datetime.datetime.strptime( \
                                        session['Session_Start_Time__c'], \
                                        "%Y-%m-%dT%H:%M:%S.%f%z" )

                            if 'Session_Take__c' in session:
                                dsession.take = \
                                        session['Session_Take__c']

                            if 'Session_Theme__c' in session:
                                dsession.theme = \
                                        session['Session_Theme__c']

                            if 'Sponsored__c' in session:
                                dsession.sponsored = \
                                        session['Sponsored__c']

                            if 'Session_Public_Name__c' in session:
                                dsession.public_name = \
                                        session['Session_Public_Name__c']

                            if 'SessionImage__c' in session:
                                dsession.image = \
                                        session['SessionImage__c']

                            dsession.last_sync = receivedAt
                            dsession.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        sessions = response["records"]

                print('Sessions OK')

                # Getting speakers
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Contact__r.Name' \
                        + ', Contact__r.Title' \
                        + ', Account__r.Name' \
                        + ', Event__c' \
                        + ', Bio__c' \
                        + ', Custom_Profile_Image__c' \
                        + ', Custom_Name__c' \
                        + ', Anonymous_Account_Name__c' \
                        + ', Anonymous_Contact_Name__c' \
                        + ', Anonymous_Title_Name__c' \
                        + ', Speaker_Country__c' \
                        + ', Speaker_Rating__c' \
                        + ' FROM Speaker__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                speakers = response["records"]
                stop = False

                while not stop:
                    for mSpeaker in speakers:
                        if not 'Id' in mSpeaker:
                            continue
                        dSpeakers = Speaker.objects. \
                                filter(salesforce_id=mSpeaker['Id'])
                        isNew = False
                        if dSpeakers.count() > 0:
                            dSpeaker = dSpeakers.first()
                        else:
                            dSpeaker = Speaker(salesforce_id=mSpeaker['Id'])
                            isNew = True

                        if 'SystemModstamp' in mSpeaker:
                            time = mSpeaker['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > dSpeaker.last_sync:
                            if 'Contact__r' in mSpeaker and \
                                    mSpeaker['Contact__r']:
                                if 'Name' in mSpeaker['Contact__r']:
                                    dSpeaker.contact_name = \
                                        mSpeaker['Contact__r']['Name']
                                if 'Title' in mSpeaker['Contact__r']:
                                    dSpeaker.contact_title = \
                                            mSpeaker['Contact__r']['Title']
                            if 'Account__r' in mSpeaker and \
                                    mSpeaker['Account__r'] and \
                                    'Name' in mSpeaker['Account__r']:
                                        dSpeaker.account_name = \
                                                mSpeaker['Account__r']['Name']
                            if 'Event__c' in mSpeaker:
                                dSpeaker.event = EventPage.objects \
                                        .filter(salesforce_id= \
                                        mSpeaker['Event__c']) \
                                        .first()
                            if 'Bio__c' in mSpeaker:
                                dSpeaker.bio = mSpeaker['Bio__c']
                            if 'Custom_Profile_Image__c' in mSpeaker:
                                dSpeaker.custom_profile_image = \
                                        mSpeaker['Custom_Profile_Image__c']
                            if 'Custom_Name__c' in mSpeaker:
                                dSpeaker.custom_name = \
                                        mSpeaker['Custom_Name__c']
                            if 'Anonymous_Account_Name__c' in mSpeaker:
                                dSpeaker.anonymous_account_name = \
                                        mSpeaker['Anonymous_Account_Name__c']
                            if 'Anonymous_Contact_Name__c' in mSpeaker:
                                dSpeaker.anonymous_contact_name = \
                                        mSpeaker['Anonymous_Contact_Name__c']
                            if 'Anonymous_Title_Name__c' in mSpeaker:
                                dSpeaker.anonymous_title_name = \
                                        mSpeaker['Anonymous_Title_Name__c']
                            if 'Speaker_Country__c' in mSpeaker:
                                dSpeaker.speaker_country = \
                                        mSpeaker['Speaker_Country__c']
                            if 'Speaker_Rating__c' in mSpeaker and \
                                    mSpeaker['Speaker_Rating__c']:
                                dSpeaker.speaker_rating = \
                                        float(mSpeaker['Speaker_Rating__c'])

                            dSpeaker.last_sync = receivedAt
                            dSpeaker.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        speakers = response["records"]

                print('Speakers OK')

                # Getting contents
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Content_Type__c' \
                        + ', Keywords_Filter__c' \
                        + ', ContentReference__c' \
                        + ', Language__c' \
                        + ', Rich_Text__c' \
                        + ', Title__c' \
                        + ' FROM Content__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                contents = response["records"]
                stop = False

                while not stop:
                    for content in contents:
                        if not 'Id' in content:
                            continue
                        pageContents = PageContent.objects. \
                                filter(salesforce_id=content['Id'])
                        isNew = False
                        if pageContents.count() > 0:
                            pageContent = pageContents.first()
                        else:
                            pageContent = PageContent(salesforce_id=content['Id'])
                            isNew = True

                        if 'SystemModstamp' in content:
                            time = content['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > pageContent.last_sync:

                            if 'Title__c' in content:
                                pageContent.title = \
                                        content['Title__c']
                            if 'Rich_Text__c' in content:
                                pageContent.rich_text = content['Rich_Text__c']
                            if 'Content_Type__c' in content:
                                pageContent.content_type = \
                                       content['Content_Type__c']
                            if 'Keywords_Filter__c' in content:
                                pageContent.is_keyword_filter = \
                                        content['Keywords_Filter__c']
                            if 'ContentReference__c' in content:
                                pageContent.reference = \
                                       content['ContentReference__c']
                            if 'Language__c' in content:
                                pageContent.lang_code = \
                                       langNameToCode(content['Language__c'])

                            pageContent.last_sync = receivedAt
                            pageContent.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        contents = response["records"]

                print('contents OK')

                # Getting marketing contents
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', Course__c' \
                        + ', Content__c' \
                        + ', CreatedDate' \
                        + ', Event__c' \
                        + ' FROM Marketing_Content__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                marketingContents = response["records"]
                stop = False

                while not stop:
                    for marketingContent in marketingContents:
                        if not 'Id' in marketingContent:
                            continue
                        marketingContents = MarketingContent.objects. \
                                filter(salesforce_id=marketingContent['Id'])
                        isNew = False
                        if marketingContents.count() > 0:
                            marketContent = marketingContents.first()
                        else:
                            marketContent = \
                                    MarketingContent( \
                                    salesforce_id=marketingContent['Id'])
                            isNew = True

                        if 'SystemModstamp' in marketingContent:
                            time = marketingContent['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > marketContent.last_sync:

                            if 'Course__c' in marketingContent:
                                marketContent.course = CoursePage.objects \
                                        .filter(salesforce_id= \
                                        marketingContent['Course__c']) \
                                        .first()

                            if 'Event__c' in marketingContent:
                                marketContent.event = EventPage.objects \
                                        .filter(salesforce_id=marketingContent['Event__c']) \
                                        .first()

                            if 'Content__c' in marketingContent:
                                marketContent.content = PageContent.objects \
                                        .filter(salesforce_id=marketingContent['Content__c']) \
                                        .first()

                            if 'CreatedOn' in marketingContent:
                                marketContent.creation_date = \
                                        pytz.utc.localize( \
                                        datetime.datetime.strptime( \
                                        marketingContent['CreatedOn'], \
                                        "%Y-%m-%dT%H:%M:%S" ))
                            marketContent.last_sync = receivedAt
                            marketContent.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        marketingContents = response["records"]

                print('Mark contents OK')

                # Getting images
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', SystemModstamp' \
                        + ', LNX_Image_URL__c' \
                        + ', ImageType__c' \
                        + ', MarketingContent__c' \
                        + ' FROM LNXImage__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                mlnxImages = response["records"]
                stop = False

                while not stop:
                    for mlnxImage in mlnxImages:
                        if not 'Id' in mlnxImage:
                            continue
                        lnxImages = LnxImage.objects. \
                                filter(salesforce_id=mlnxImage['Id'])
                        isNew = False
                        if lnxImages.count() > 0:
                            lnxImage = lnxImages.first()
                        else:
                            lnxImage = \
                                    LnxImage( \
                                    salesforce_id=mlnxImage['Id'])
                            isNew = True

                        if 'SystemModstamp' in mlnxImage:
                            time = mlnxImage['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > lnxImage.last_sync:

                            if 'LNX_Image_URL__c' in mlnxImage:
                                lnxImage.url = mlnxImage['LNX_Image_URL__c']

                            if 'ImageType__c' in mlnxImage:
                                lnxImage.image_type = mlnxImage['ImageType__c']


                            if 'MarketingContent__c' in mlnxImage:
                                lnxImage.mark_content = MarketingContent.objects \
                                        .filter(salesforce_id= \
                                                mlnxImage['MarketingContent__c']) \
                                        .first()


                            lnxImage.last_sync = receivedAt
                            lnxImage.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        mlnxImages = response["records"]

                print('LNX Images OK')

                # Getting testimonials
                url = 'https://na45.salesforce.com/services/data/v20.0/query?q=' \
                        + 'SELECT Id' \
                        + ', Authorised__c' \
                        + ', Course__c' \
                        + ', Course__r.Language__c' \
                        + ', Contact_Title__c' \
                        + ', Featured__c' \
                        + ', Ranking__c' \
                        + ', CreatedDate' \
                        + ', SystemModstamp' \
                        + ', Testimonial_Text__c' \
                        + ' FROM Testimonial__c '

                r = requests.get(url, headers=headers)
                r.encoding = 'utf-8'

                receivedAt = datetime.datetime.now(datetime.timezone.utc)

                response = r.json()
                calls += 1
                nextRecordsUrl = ''
                if 'nextRecordsUrl' in response:
                    nextRecordsUrl = response["nextRecordsUrl"]
                testis = response["records"]
                stop = False

                while not stop:
                    for mTesti in testis:
                        if not 'Id' in mTesti:
                            continue
                        dTestis = Testimonial.objects. \
                                filter(salesforce_id=mTesti['Id'])
                        isNew = False
                        if dTestis.count() > 0:
                            if 'Authorised__c' not in mTesti or \
                                    ('Authorised__c' in mTesti and \
                                    mTesti['Authorised__c'] == False) \
                                    or 'Testimonial_Text__c' not in mTesti \
                                    or ('Testimonial_Text__c' in mTesti \
                                    and mTesti['Testimonial_Text__c'] == ""):
                                dTestis.first().delete()
                                continue
                            else:
                                dTesti = dTestis.first()
                        else:
                            if 'Authorised__c' not in mTesti or \
                                    ('Authorised__c' in mTesti and \
                                    mTesti['Authorised__c'] == False) \
                                    or 'Testimonial_Text__c' not in mTesti \
                                    or ('Testimonial_Text__c' in mTesti \
                                    and mTesti['Testimonial_Text__c'] == ""):
                                continue
                            else:
                                dTesti = Testimonial(
                                        salesforce_id=mTesti['Id'])
                                isNew = True

                        if 'SystemModstamp' in mTesti:
                            time = mTesti['SystemModstamp']
                            modon = datetime.datetime.strptime(
                                        time, "%Y-%m-%dT%H:%M:%S.%f%z"
                                        )
                        else:
                            continue
                        if isNew or modon > dTesti.last_sync:
                            if 'Contact_Title__c' in mTesti:
                                dTesti.contact_title = mTesti['Contact_Title__c']
                            if 'Featured__c' in mTesti:
                                dTesti.featured = mTesti['Featured__c']
                            dTesti.testimonial_text = mTesti['Testimonial_Text__c']
                            if 'Course__c' in mTesti:
                                dTesti.course = CoursePage.objects \
                                        .filter(salesforce_id= \
                                        mTesti['Course__c']) \
                                        .first()
                            if 'Ranking__c' in mTesti and \
                                    mTesti['Ranking__c']:
                                dTesti.ranking = int(mTesti['Ranking__c'])
                            dTesti.lang_code = \
                                    langNameToCode(mTesti['Course__r']['Language__c'])
                            if 'CreatedOn' in mTesti:
                                dTesti.creation_date = pytz.utc.localize( \
                                        datetime.datetime.strptime( \
                                        mTesti['CreatedOn'], "%Y-%m-%dT%H:%M:%S" ))

                            dTesti.last_sync = receivedAt
                            dTesti.save()
                    if nextRecordsUrl == '':
                        stop = True
                    else:
                        url = 'https://na45.salesforce.com' + nextRecordsUrl
                        r = requests.get(url, headers=headers)
                        r.encoding = 'utf-8'

                        receivedAt = datetime.datetime.now(datetime.timezone.utc)
                        response = r.json()
                        calls += 1
                        nextRecordsUrl = ''
                        if 'nextRecordsUrl' in response:
                            nextRecordsUrl = response["nextRecordsUrl"]
                        testis = response["records"]
                print('Testimonials OK')

                print('End: ' + str(calls) + ' calls')
        except Exception as e: print(e)

