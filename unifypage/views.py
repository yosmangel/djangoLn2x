from __future__ import unicode_literals
from future.builtins import str, int
from django.http import HttpResponseRedirect

from mezzanine.pages import views
from unifypage.models import Row

from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template.response import TemplateResponse

from mezzanine.pages.models import Page, PageMoveException
from mezzanine.utils.urls import home_slug


from calendar import month_name

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.apps import apps

from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.blog.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate
from mezzanine.core.models import Displayable
from mezzanine.utils.sites import has_site_permission
from mezzanine.accounts.views import login as accountslogin

from django.core.mail import send_mail

from .forms import ContactForm, LogInCaptchaForm

from el_pagination.decorators import page_template

from .models import MultilangKeyword


@page_template('unifypage/row.html', key='row_entries_page')
def unifypage(request, slug, template=u"pages/unifypage.html", extra_context=None):
    if hasattr(request, "page") and hasattr(request.page, "unifypage"):
        if request.method == 'POST':
            if slug == 'about-us/contact':
                send_mail(
                    request.POST.get("name") + ' (' + request.POST.get("email")\
                            + ') completed the contact form. Subject: '\
                            + request.POST.get("subject"),
                    request.POST.get("message"),
                    'info@ln2x.com',
                    ['lallen@liquidnexxus.com',],
                    fail_silently=False,
                )
                if request.POST.get("send_email") == 'on':
                    send_mail(
                        'Your email to the ln2x team on the subject: '\
                                + request.POST.get("subject"),
                        request.POST.get("message"),
                        'info@ln2x.com',
                        [request.POST.get("email"),],
                        fail_silently=False,
                        )
            form = ContactForm(request.POST)
        else:
            form = ContactForm()
        context = {
            'row_entry_list': request.page.unifypage.toRows.all,
            'is_user_admin': has_site_permission(request.user),
            'form': form,
            'keywords': request.page.unifypage.multilang_keywords.all(),
        }
    else:
        context = {}
    context.update(extra_context or {})
    return page(request, slug, template, context)

def page(request, slug, template=u"pages/page.html", extra_context=None):
    """
    Select a template for a page and render it. The request
    object should have a ``page`` attribute that's added via
    ``mezzanine.pages.middleware.PageMiddleware``. The page is loaded
    earlier via middleware to perform various other functions.
    The urlpattern that maps to this view is a catch-all pattern, in
    which case the page attribute won't exist, so raise a 404 then.

    For template selection, a list of possible templates is built up
    based on the current page. This list is order from most granular
    match, starting with a custom template for the exact page, then
    adding templates based on the page's parent page, that could be
    used for sections of a site (eg all children of the parent).
    Finally at the broadest level, a template for the page's content
    type (it's model class) is checked for, and then if none of these
    templates match, the default pages/page.html is used.
    """

    from mezzanine.pages.middleware import PageMiddleware
    if not PageMiddleware.installed():
        raise ImproperlyConfigured("mezzanine.pages.middleware.PageMiddleware "
                                   "(or a subclass of it) is missing from " +
                                   "settings.MIDDLEWARE_CLASSES or " +
                                   "settings.MIDDLEWARE")

    if not hasattr(request, "page") or request.page.slug != slug:
        raise Http404

    # Check for a template name matching the page's slug. If the homepage
    # is configured as a page instance, the template "pages/index.html" is
    # used, since the slug "/" won't match a template name.
    template_name = str(slug) if slug != home_slug() else "index"
    templates = [u"pages/%s.html" % template_name]
    method_template = request.page.get_content_model().get_template_name()
    if method_template:
        templates.insert(0, method_template)
    if request.page.content_model is not None:
        templates.append(u"pages/%s/%s.html" % (template_name,
            request.page.content_model))
    for parent in request.page.get_ascendants(for_user=request.user):
        parent_template_name = str(parent.slug)
        # Check for a template matching the page's content model.
        if request.page.content_model is not None:
            templates.append(u"pages/%s/%s.html" % (parent_template_name,
                request.page.content_model))
    # Check for a template matching the page's content model.
    if request.page.content_model is not None:
        templates.append(u"pages/%s.html" % request.page.content_model)
    templates.append(template)
    if request.is_ajax() or (template != "pages/unifypage.html" and template != "pages/page.html"):
        templates = template
    return TemplateResponse(request, templates, extra_context or {})

def login(request, template="accounts/account_login.html",
        form_class=LogInCaptchaForm, extra_context=None):
    """
    Login form with captcha
    """
    return accountslogin(request, template, form_class, extra_context)

# Blog

User = get_user_model()

def blog_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="blog/blog_post_list.html",
                   page_template="blog/blog_post_list_elems.html",
                   extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/blog_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    blog_posts = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        blog_posts = blog_posts.filter(keywords__keyword=tag)
    if year is not None:
        blog_posts = blog_posts.filter(publish_date__year=year)
        if month is not None:
            blog_posts = blog_posts.filter(publish_date__month=month)
            try:
                month = _(month_name[int(month)])
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        blog_posts = blog_posts.filter(categories=category)
        templates.append(u"blog/blog_post_list_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        blog_posts = blog_posts.filter(user=author)
        templates.append(u"blog/blog_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    blog_posts = blog_posts.select_related("user").prefetch_related(*prefetch)
    blog_posts = paginate(blog_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {
            "blog_posts": blog_posts,
            "year": year,
            "month": month,
            "tag": tag,
            "category": category,
            "author": author,
            "masonry_page_template": page_template,
            }
    context.update(extra_context or {})
    templates.append(template)
    if request.is_ajax():
        templates = page_template
    return unifypage(request, 'blog', templates, extra_context=context)


def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    blog_posts = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {
            "blog_post": blog_post,
            "editable_obj": blog_post,
            "related_posts": related_posts,
            "keywords": blog_post.multilang_keywords.all(),
            }
    context.update(extra_context or {})
    templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)


def blog_post_feed(request, format, **kwargs):
    """
    Blog posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()

def search(request, keyword='', template="unifypage/search_results.html",
        extra_context=None):
    no_result = False
    query = request.GET.get("q", "")
    if query:
        keyword = query
    multikey = MultilangKeyword.objects.filter(word=keyword).first()
    if not multikey:
        multikey = MultilangKeyword.objects.filter(word_en=keyword).first()
        if not multikey:
            multikey = MultilangKeyword.objects.filter(word_fr=keyword).first()
            if not multikey:
                multikey = MultilangKeyword.objects.filter(word_es=keyword).first()
                if not multikey:
                    no_result = True
    if no_result:
        context = {
                'no_result': True,
                'keyword': keyword,
                'all_keywords': MultilangKeyword.objects.all(),
                }
    else:
        course_pages = multikey.course_pages.all()
        event_pages = set(multikey.event_pages.all())
        for course_page in course_pages:
            event_pages.update(course_page.events.are_published())
        context = {
                'keyword': multikey.word,
                'pages': multikey.pages.all(),
                'course_pages': course_pages,
                'event_pages': event_pages,
                'blog_posts': multikey.blog_posts.all(),
                }
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)

def mezz_search(request, template="search_results.html", extra_context=None):
    """
    Display search results. Takes an optional "contenttype" GET parameter
    in the form "app-name.ModelName" to limit search results to a single model.
    """
    query = request.GET.get("q", "")
    page = request.GET.get("page", 1)
    per_page = settings.SEARCH_PER_PAGE
    max_paging_links = settings.MAX_PAGING_LINKS
    try:
        parts = request.GET.get("type", "").split(".", 1)
        search_model = apps.get_model(*parts)
        search_model.objects.search  # Attribute check
    except (ValueError, TypeError, LookupError, AttributeError):
        search_model = Displayable
        search_type = _("Everything")
    else:
        search_type = search_model._meta.verbose_name_plural.capitalize()
    results = search_model.objects.search(query, for_user=request.user)
    paginated = paginate(results, page, per_page, max_paging_links)
    context = {"query": query, "results": paginated,
               "search_type": search_type}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


