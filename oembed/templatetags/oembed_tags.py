import urllib
import html

import django
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import smart_str, force_text
from oembed.core import replace
from oembed.models import StoredOEmbed

register = template.Library()

@register.filter
def unescape(text):
    """Decoding HTML Entities to Text in Python"""
    return force_text(html.unescape(text))


@register.filter
def urlunquote(quoted_url):
    return force_text(urllib.unquote(smart_str(quoted_url)))


@register.filter
def urlunquote_plus(quoted_url):
    return force_text(urllib.unquote_plus(smart_str(quoted_url)))


def oembed(input, args=None):
    if args:
        try:
            width, height = map(int, args.lower().split('x'))
        except ValueError:
            raise template.TemplateSyntaxError("Oembed's optional " \
                "WIDTHxHEIGHT argument requires WIDTH and HEIGHT to be " \
                "positive integers.")
    else:
        width, height = None, None
    return replace(input, max_width=width, max_height=height)
oembed = stringfilter(oembed)

if django.get_version() < "1.4":
    oembed.is_safe = True
    register.filter('oembed', oembed)
else:
    register.filter('oembed', oembed, is_safe=True)


def do_oembed(parser, token):
    """
    A node which parses everything between its two nodes, and replaces any
    links with OEmbed-provided objects, if possible.

    Supports two optional arguments, one which is the maximum width and height,
    the other which specifies whether to use the simple provider, specified
    like so:

                {% oembed 640x480 simple %}
                    http://www.viddler.com/explore/SYSTM/videos/49/
                {% endoembed %}
    """
    width = None
    height = None
    simple = False

    tokens = token.split_contents()
    if len(tokens) > 3:
        raise template.TemplateSyntaxError(
            "Oembed tag takes two (optional) arguments: WIDTHxHEIGHT, where \
             WIDTH and HEIGHT are positive integers, and 'simple', which \
             tries to render the embed object in a basic layout.")
    else:
        width, height, simple = _parse_oembed_tag_tokens(tokens)

    nodelist = parser.parse(('endoembed',))
    parser.delete_first_token()
    return OEmbedNode(nodelist, width, height, simple)

register.tag('oembed', do_oembed)

class OEmbedNode(template.Node):
    def __init__(self, nodelist, width, height, simple):
        self.nodelist = nodelist
        self.width = width
        self.height = height
        self.simple = simple

    def render(self, context):
        kwargs = {}
        if self.width and self.height:
            kwargs['max_width'] = self.width
            kwargs['max_height'] = self.height
        if self.simple:
            kwargs['simple'] = self.simple
        return replace(self.nodelist.render(context), **kwargs)

# This comes in handy, so you don't hit the database so many times
# if you want to access different fields for a same object
_oembed_objects = {}

@register.filter
def get_oembed_property(oembed_url, json_property):
    """ Use it like this:
        {% url_string|get_oembed_property:'thumbnail_url' %}    
    """
    if not oembed_url in _oembed_objects:
        matches = StoredOEmbed.objects.filter(match=oembed_url)
        if matches:
            # Found it, happy path
            oembed = matches[0]
        else:
            # If not found, we will try to fetch it
            _ = replace(oembed_url)
            matches = StoredOEmbed.objects.filter(match=oembed_url)
            if matches:
                # Haven't been parsed before, but now is available
                oembed = matches[0]
            else:
                # Nothing to do, is not an oembed
                oembed = None
        _oembed_objects[oembed_url] = oembed

    if _oembed_objects[oembed_url]:
        return _oembed_objects[oembed_url].get_json(json_property)
    else:
        return ''

def _parse_oembed_tag_tokens(tokens):
    width = None
    height = None
    simple = False

    for t in tokens:
        if t == "oembed":
            continue
        elif t == "simple":
            simple = True
        else:
            try:
                width, height = map(int, t.lower().split('x'))
            except ValueError:
                raise template.TemplateSyntaxError("Oembed's optional " \
                    "WIDTHxHEIGHT argument requires WIDTH and HEIGHT to be " \
                    "positive integers.")

    return width, height, simple
