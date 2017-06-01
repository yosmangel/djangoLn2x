from django import template
from django.utils.safestring import mark_safe

from ln2xevents.models import PageContent, Testimonial, MarketingContent, EventPage

from bs4 import BeautifulSoup, Tag

register = template.Library()

@register.filter(name="page_content")
def page_content(content):
    soup = BeautifulSoup(content, "lxml")
    if soup.ul:
        for ul in soup.find_all('ul'):
            if ul.parent.name != 'li':
                ul.name = 'div'
                ul['class'] = "grid-boxes"
                gutter = soup.new_tag('div')
                gutter['class']="gutter-sizer"
                ul.insert(0, gutter)
    if soup.li:
        for li in soup.find_all('li'):
            if li.parent.name != 'ul':
                li.name = 'div'
                li['class'] = "tag-box tag-box-v1 box-shadow shadow-effect-2"
                #parent = Tag(name='div')
                li['class'] = 'grid-boxes-in grid-item tag-box tag-box-v1 box-shadow shadow-effect-2'
               #parent.contents.append(li)
               #li.replace_with(parent)
    if soup.body:
        return ''.join(str(child) for child in soup.body)
    else:
        return soup.prettify()

@register.simple_tag()
def in_past_message(lang_code='en'):
    """
    Returns the text to put when the event is in the past
    """
    message = ''
    content = PageContent.objects.all().filter(reference='PastEventMessage').filter(lang_code=lang_code).first()
    message = content.title
    return mark_safe(message)

@register.filter(name="next_ib")
def next_ib(imgbreak):
    try:
        return next(imgbreak).image
    except StopIteration:
        pass
    except TypeError:
        pass

@register.simple_tag()
def testimonials_blocks(positions_string='1', lang='en', course=None, job_title=None):
    """
    Generate blocks with testimonials in order of preference for the given
    language and course
    The postion_string can be in csv format or 'rangeX' for the position 1 to X
    or 'rangeX-Y' for the position X to Y
    """
    blocks = ''
    if 'range' in positions_string:
        positions_string = positions_string.replace('range', '')
        if '-' in positions_string:
            ranges = positions_string.split('-')
            maxi = int(ranges[1])
            positions = range(int(ranges[0]), int(ranges[1]))
        else:
            maxi = int(positions_string)
            positions = range(int(positions_string))
    else:
        positions = positions_string.split(',')
        positions = [ int(pos) for pos in positions]
        maxi = max(positions)

    base_testis = list(Testimonial.objects \
            .filter(ranking__gte=1, ranking__lte=5, lang_code=lang) \
            .order_by('ranking', 'creation_date'))
    testis = base_testis
    if course:
        testis = [testi for testi in testis if testi.course == course]
    if len(testis) < 3:
        testis += [testi for testi in base_testis if testi not in testis]

    for num in positions:

        if len(testis) > int(num):
            testi = testis[int(num)]
        else:
            break

        blocks += '<div class="testimonials-info rounded-bottom">'
        blocks += '<div class="testimonials-desc">'
        blocks += '<p><i>' + testi.testimonial_text + '</i></p>'
        blocks += '<small>' + testi.contact_title + '</small>'
        blocks += '</div>'
        blocks += '<script type="application/ld+json">'
        blocks += '{'
        blocks += '  "@context": "http://schema.org/",'
        blocks += '  "@type": "Review",'
        blocks += '  "itemReviewed": {'
        blocks += '    "@type": "Organization",'
        blocks += '    "image": "https://s3.eu-central-1.amazonaws.com/ln2ximages/liquid-nexxus-logo.png",'
        blocks += '    "name": "LiquidNexxus"'
        blocks += '  },'
        blocks += '  "reviewRating": {'
        blocks += '    "@type": "Rating",'
        blocks += '    "ratingValue": "4"'
        blocks += '  },'
        blocks += '  "author": {'
        blocks += '    "@type": "Person",'
        blocks += '    "name": "' + testi.contact_title + '"'
        blocks += '  },'
        blocks += '  "reviewBody": "' + testi.testimonial_text + '",'
        blocks += '  "publisher": {'
        blocks += '    "@type": "Organization",'
        blocks += '    "name": "LiquidNexxus"'
        blocks += '  }'
        blocks += '}'
        blocks += '</script>'
        blocks += '</div>'
    return blocks

@register.simple_tag()
def keywords_content(lang_code='en'):
    content = PageContent.objects.filter(
            lang_code=lang_code, reference='keywordsLabel'
            ).first()
    return MarketingContent(content=content)


@register.simple_tag()
def all_next_sessions(lang='en'):
    """
    returns the nexts sessions in the given language
    """
    results = EventPage.objects.are_not_past().filter(lang_code=lang)
    if not results:
        results = EventPage.objects.are_not_past()
    return sorted(list(results), key = lambda event: event.start_date)

