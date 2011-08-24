from django import template
from django.template.defaultfilters import stringfilter
from oembed.core import replace
from oembed.models import StoredOEmbed

register = template.Library()

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
oembed.is_safe = True
oembed = stringfilter(oembed)

register.filter('oembed', oembed)

def do_oembed(parser, token):
    """
    A node which parses everything between its two nodes, and replaces any
    links with OEmbed-provided objects, if possible.

    Supports one optional argument, which is the maximum width and height,
    specified like so:

        {% oembed 640x480 %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}
    """
    args = token.contents.split()
    if len(args) > 2:
        raise template.TemplateSyntaxError("Oembed tag takes only one (option" \
            "al) argument: WIDTHxHEIGHT, where WIDTH and HEIGHT are positive " \
            "integers.")
    if len(args) == 2:
        try:
            width, height = map(int, args[1].lower().split('x'))
        except ValueError:
            raise template.TemplateSyntaxError("Oembed's optional " \
                "WIDTHxHEIGHT argument requires WIDTH and HEIGHT to be " \
                "positive integers.")
    else:
        width, height = None, None
    nodelist = parser.parse(('endoembed',))
    parser.delete_first_token()
    return OEmbedNode(nodelist, width, height)

register.tag('oembed', do_oembed)

class OEmbedNode(template.Node):
    def __init__(self, nodelist, width, height):
        self.nodelist = nodelist
        self.width = width
        self.height = height

    def render(self, context):
        kwargs = {}
        if self.width and self.height:
            kwargs['max_width'] = self.width
            kwargs['max_height'] = self.height
        return replace(self.nodelist.render(context), **kwargs)


@register.filter
def get_oembed_thumbnail_url(oembed_url):
    # could refactor into get_oembed_<property_name>
    matches = StoredOEmbed.objects.filter(match=oembed_url).exclude(json='')
    # exclude blank json for backward compatibility without flushing table
    if not matches:
        _ = replace(oembed_url)
        matches = StoredOEmbed.objects.filter(
            match=oembed_url).exclude(json='')
    try:
        return matches[0].get_json('thumbnail_url')
    except IndexError:
        # oh dear, something is seriously wrong here
        if settings.DEBUG:
            raise RuntimeError(
                "StoredOEmbeds aren't gettings stored correctly!?")
        else:
            return '#oembed-failure' # fail silently-ish
