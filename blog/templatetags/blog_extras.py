from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from blog.models import Post
import logging


register = template.Library()
logger = logging.getLogger(__name__)
user_model = get_user_model()


# Author Details (Name / Email Link) and Date of Post
@register.filter
def author_details(author, current_user):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}" class="txt-cb">', author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)


# Simple tags to build Bootstrap rows
@register.simple_tag
def row(extra_classes=''):
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    return format_html("</div>")


# Columns
@register.simple_tag
def col(extra_classes=''):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")


# Fetch the five most recent blogposts
# Exclude current post being viewed
@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    # Log call for 'recent posts' - template fragment caching
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
    return {"title": "Recent Posts", "posts": posts}


@register.simple_tag
def h2(page_name=""):
    return format_html('<div class="card-body text-center mt-4 p-5"><h2 class="card-title display-2">{}</h2></div>', page_name)
