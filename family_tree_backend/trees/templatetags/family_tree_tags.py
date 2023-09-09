from django import template
from trees.models import Family_Member

register = template.Library()

@register.simple_tag
def render_family_tree(person):
    """Renders an entire tree"""
    result = f"{person.first_name} {person.last_name}"

    children = person.children.all()
    if children:
        result += '<ul>'
        for child in children:
            result += f'<li>render_family_tree(child)</li>'
        result += '</ul>'
    return (result)
