import os

import pypandoc
from django import template
from django.conf import settings
from django.template.defaultfilters import register, stringfilter
from django_fsm_log.models import StateLog
from rest_framework.authtoken.models import Token

from wastd.observations.models import OBSERVATION_ICONS, Encounter

register = template.Library()


@register.simple_tag
def google_maps_apikey(*args, **kwargs):
    """Return the settings key GOOGLE_MAPS_API_KEY."""
    return settings.GOOGLE_MAPS_API_KEY


@register.simple_tag
def apitoken(user, **kwargs):
    return Token.objects.get_or_create(user=user)[0].key


@register.inclusion_tag('tx_logs.html', takes_context=False)
def tx_logs(obj):
    """Render the FSM transition logs for an object to HTML."""
    return {'logs': [log for log in StateLog.objects.for_(obj)]}


@register.filter
@stringfilter
def mm_as_cm(mm_value):
    """Turn a given mm value into a cm value."""
    if mm_value == 'None':
        return None
    return float(mm_value) / 10


@register.filter
@stringfilter
def mm_as_m(mm_value):
    """Turn a given mm value into a m value."""
    if mm_value == 'None':
        return None
    return float(mm_value) / 1000


@register.filter
@stringfilter
def tb_status_icon(status_value):
    """Turn a given status value into a complete twitter-boootstrap v4 CSS class.

    Uses ``Encounter.STATUS_LABELS`` to resolve values for:

    * new = red
    * proofread = orange
    * curated = blue
    * published = green
    """
    return Encounter.STATUS_LABELS[status_value]


@register.filter
@stringfilter
def fa_observation_icon(observation_value):
    """Turn a given accuracy value into a complete fontawesome icon class.

    Uses ``wastd.observations.OBSERVATION_ICONS`` to resolve values for:

    * present: confirmed yes
    * absent: confirmed no
    * na: did not measure
    """
    return OBSERVATION_ICONS[observation_value]


@register.filter
def filename(value):
    return os.path.basename(value)


@register.filter
@stringfilter
def tex(string_value):
    """Convert a text or HTML string to tex."""
    return pypandoc.convert_text(string_value, 'tex', format='html')
