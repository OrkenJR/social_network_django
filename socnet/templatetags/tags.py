from django import template

register = template.Library()


@register.filter
def have_parents(things):
    return things.filter(parent__isnull=True)


@register.filter('break')
def break_(loop):
    '''Breaks from a loop.

    The 'break' filter is used within a loop and takes as input a loop variable,
    e.g. 'forloop' in case of a for loop. For example, to display the items
    from list ``items`` up to the first item that is equal to ``end``::

        <ul>
        {% for item in items %}
            {% if item == 'end' %}
                {{ forloop|break }}
            {% endif %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>

    Breaking from nested loops is also supported by passing the appropriate loop
    variable, e.g. ``forloop.parentloop|break``.
    '''
    raise StopLoopException(loop, False)

