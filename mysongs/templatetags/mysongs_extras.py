from django import template

register = template.Library()


@register.filter()
def uppercase(value):
    return value.upper()

@register.filter()
def duplicate(albumnamee, duplicate_list):
    is_duplicate = False
    for value in duplicate_list:
        if value['album_name'] == albumnamee.album_name:
            is_duplicate = True
            break
    if is_duplicate:
        return albumnamee.album_name + "("+str(albumnamee.album_year)+")"
    else:
        return albumnamee.album_name






