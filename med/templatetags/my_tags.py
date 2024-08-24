from django import template

register = template.Library()


@register.filter(name='media_filter')
def media_filter(path):
    ''' Шаблонный фильтр для изображений (медиа)'''
    if path:
        return f'/media/{path}'
    return '#'
