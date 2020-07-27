# -*- coding: utf-8 -*-
"""Template tags for taxonomy."""
# import json

# import django
# from django.contrib.admin.util import lookup_field, quote
# from django.conf import settings
# from django.core.urlresolvers import resolve, reverse
# from django.utils.encoding import force_str
from django import template

register = template.Library()


@register.filter
def rangify(value):
    """Return a range around a given number."""
    span = 5
    min_val = max(value - span, 1)
    max_val = max(value + span, span * 2)
    return range(min_val, max_val)


# @register.inclusion_tag('include/taxon_change.html', takes_context=True)
# def admin_taxon_change_link(context, user, btn=True, block=False, label=False):
#     """Render a link to the admin taxon change view."""
#     return {
#         "object": context["object"],
#         "is_staff": True,
#         "btn": btn,
#         "block": block,
#         "label": label
#     }


# -----------------------------------------------------------------------------
# Conservation threats
#
# @register.inclusion_tag('conservation/include/conservationthreat_cards.html', takes_context=False)
# def conservationthreat_cards(user, threats, area=None):
#     """Render a conservation threat in a card."""
#     return {"threats": threats.filter(occurrence_area_code=area) if area else threats}


# # -----------------------------------------------------------------------------
# # Conservation actions
# #
# @register.inclusion_tag('conservation/include/conservationaction_cards.html', takes_context=False)
# def conservationaction_cards(user, actions, area=None):
#     """Render a conservation Action in a card."""
#     return {"actions": actions.filter(occurrence_area_code=area) if area else actions}
