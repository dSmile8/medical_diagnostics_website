from django import template

register = template.Library()


@register.filter(name='media_filter')
def media_filter(path):
    """
    Template filter for media images.
    """

    if path:
        return f'/media/{path}'
    return '#'
