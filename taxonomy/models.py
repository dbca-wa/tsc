# -*- coding: utf-8 -*-
"""Taxonomic models.

The ``Hbv*`` models maintain a plain copy of WACensus data as published by KMI Geoserver.
They are populated and updated through the TSC API.

Taxon, Crossreferece, and Vernacular are populated from Hbv* through ``taxonomy.utils.make_taxon_names``.
Community is initally populated from TEC through the API, then updated both through the admin and the API.
"""
import logging
from django.contrib.gis.db import models as geo_models
from django.db import models
from django.db.models.signals import pre_save  # , post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from shared.models import LegacySourceMixin, UrlsMixin, RenderMixin

logger = logging.getLogger(__name__)


class HbvSupra(models.Model):
    r"""HBV Suprafamily Group.

    {//supra
      "ogc_fid": 0,
      "supra_code": "ALGA",
      "supra_name": "Alga",
      "updated_on": "2004-12-09Z",
      "md5_rowhash": "ac75154fd5c5b9237d20d833bfe0a506"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to identify the record."),
    )

    supra_code = models.CharField(
        max_length=1000,
        unique=True,
        blank=True, null=True,
        db_index=True,
        verbose_name=_("HBV Suprafamily Group Code"),
        help_text=_("A short code."),
    )

    supra_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("HBV Suprafamily Group Name"),
        help_text=_("The group name."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["supra_code", ]
        verbose_name = "Paraphyletic Group"
        verbose_name_plural = "Paraphyletic Groups"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return self.supra_name


class HbvGroup(models.Model):
    r"""Paraphyletic or informal group of taxa.

    Maps name_id to supra.

    {//group
      "ogc_fid": 0,
      "class_id": "MONOCOT", # FK to supra
      "name_id": 828,
      "updated_by": "HERBIE",
      "updated_on": "2011-04-10Z",
      "rank_name": "Species",
      "name": "Eleocharis pallens",
      "md5_rowhash": "fa190f8247844ef8d2a94f73b961ed69"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to identify the record."),
    )

    class_id = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("HBV Suprafamily Group Code"),
        help_text=_(""),
    )

    name_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    updated_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Updated by"),
        help_text=_("The person or system who updated this record last in WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    rank_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank Name"),
        help_text=_("WACensus Taxonomic Rank Name."),
    )

    name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Name"),
        help_text=_("."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["class_id", "rank_name", "name", ]
        index_together = [
            ["class_id", "rank_name", "name", ]
        ]
        verbose_name = "HBV Suprafamily Group Membership"
        verbose_name_plural = "HBV Suprafamily Group Memberships"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return "[{0}] {1}".format(self.class_id, self.name)


class HbvFamily(models.Model):
    r"""Taxonomic nodes from Families and up from HBVFamilies.

    {
      "ogc_fid": 0,
      "name_id": 23206,
      "kingdom_id": 4,
      "rank_id": 140,
      "rank_name": "Family",
      "family_name": "Phragmopelthecaceae",
      "is_current": "Y",
      "informal": null,
      "comments": null,
      "family_code": "762",
      "linear_sequence": null,
      "order_nid": null,
      "order_name": null,
      "class_nid": null,
      "class_name": null,
      "division_nid": null,
      "division_name": null,
      "kingdom_name": "Fungi",
      "author": "L.Xavier",
      "editor": null,
      "reference": "Phragmopeltecaceae uma ...",
      "supra_code": "LICHEN",
      "added_on": "2004-12-09Z",
      "updated_on": "2016-08-30Z",
      "md5_rowhash": "2b9aaba4c145701f540c40db4fde6071"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, "
                    "used to identify the record."),
    )

    name_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    rank_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Rank ID"),
        help_text=_("WACensus Taxonomic Rank ID."),
    )

    rank_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank Name"),
        help_text=_("WACensus Taxonomic Rank Name."),
    )

    family_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Family Name"),
        help_text=_(""),
    )

    is_current = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is name current?"),
        help_text=_("WACensus currency status."),
    )

    informal = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name approval status"),
        help_text=_("The approval status indicates whether a taxonomic name"
                    " is a phrase name (PN), manuscript name (MS) or published (blank)."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments about the name."),
    )

    family_code = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Family Code"),
        help_text=_("Taxonomic Family Code, deprecated, no not use."),
    )

    linear_sequence = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Linear sequence"),
        help_text=_("Always populated for plant families, may be blank for other names."),
    )

    order_nid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Order NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    order_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Order Name"),
        help_text=_(""),
    )

    class_nid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Class NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    class_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Class"),
        help_text=_(""),
    )

    division_nid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Division NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    division_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Division"),
        help_text=_(""),
    )

    kingdom_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Kingdom ID"),
        help_text=_("WACensus Kingdom ID."),
    )

    kingdom_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Kingdom"),
        help_text=_(""),
    )

    author = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Author"),
        help_text=_("Taxonomic Author"),
    )

    editor = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Editor"),
        help_text=_("The rditor of the journal the name was published in."),
    )

    reference = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Reference"),
        help_text=_("The citation for the reference article this name was published in."),
    )

    supra_code = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("HBV Suprafamily Group Code"),
        help_text=_(""),
    )

    added_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus added on"),
        help_text=_("Date on which this record was added to WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["kingdom_name", "division_name", "class_name", "order_name", "family_name", ]
        index_together = [
            ["kingdom_name", "division_name", "class_name", "order_name", "family_name", ],
        ]
        verbose_name = "HBV Family"
        verbose_name_plural = "HBV Families"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return self.family_name


class HbvGenus(models.Model):
    r"""Taxonomic Genera.

    {//genera
      "ogc_fid": 0,
      "name_id": 44200,
      "kingdom_id": 4,
      "rank_id": 180,
      "rank_name": "Genus",
      "genus": "Xalocoa",
      "is_current": "Y",
      "informal": null,
      "comments": null,
      "family_code": null,
      "family_nid": 23171, # FK Families
      "author": "Kraichak, Lücking & Lumbsch",
      "editor": null,
      "reference": "Austral.Syst.Bot. 26:472 (2014)",
      "genusid": 44200,
      "added_on": "2014-05-18Z",
      "updated_on": "2014-05-18Z",
      "md5_rowhash": "88bd0e2944e7ac09bdc08adafb453a66"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to identify the record."),
    )

    name_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    kingdom_id = models.BigIntegerField(
        # refactor: FK Kingdom
        # default: request.user.default_kingdom
        blank=True, null=True,
        verbose_name=_("Kingdom ID"),
        help_text=_("WACensus Kingdom ID."),
    )

    rank_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Rank ID"),
        help_text=_("WACensus Taxonomic Rank ID."),
    )

    rank_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank Name"),
        help_text=_("WACensus Taxonomic Rank Name."),
    )

    genus = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Genus"),
        help_text=_("The Genus name."),
    )
    is_current = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is name current?"),
        help_text=_("WACensus currency status."),
    )

    informal = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name approval status"),
        help_text=_("The approval status indicates whether a taxonomic name"
                    " is a phrase name (PN), manuscript name (MS) or published (blank)."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments about the name."),
    )

    family_code = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Family Code"),
        help_text=_("Taxonomic Family Code, deprecated, no not use."),
    )

    family_nid = models.BigIntegerField(
        # refactor: FK Family
        blank=True, null=True,
        verbose_name=_("Family NameID"),
        help_text=_("WACensus Family NameID"),
    )
    author = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Author"),
        help_text=_("Taxonomic Author"),
    )

    editor = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Editor"),
        help_text=_("The rditor of the journal the name was published in."),
    )

    reference = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Reference"),
        help_text=_("The citation for the reference article this name was published in."),
    )

    genusid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Genus ID"),
        help_text=_("WACensus Genus ID"),
    )

    added_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus added on"),
        help_text=_("Date on which this record was added to WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["kingdom_id", "family_nid", "genusid", ]
        index_together = [
            ["kingdom_id", "family_nid", "genusid", ],
        ]
        verbose_name = "HBV Genus"
        verbose_name_plural = "HBV Genera"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return self.genus


class HbvSpecies(models.Model):
    r"""Taxonomic species names.

    {
      "ogc_fid": 1,
      "name_id": 11724,
      "kingdom_id": 3,
      "rank_id": 240,
      "rank_name": "Variety",
      "family_code": "162",
      "family_nid": 34857,
      "genus": "Pultenaea", # = HbvTaxon.name1
      "species": "verruculosa", # = HbvTaxon.name2
      "infra_rank": "var.", # HbvTaxon.rank3
      "infra_name": "verruculosa", # HbvTaxon.name3
      "infra_rank2": null, # HbvTaxon.rank4
      "infra_name2": null, # HbvTaxon.name4
      "author": "Turcz.",
      "editor": null,
      "reference": null,
      "comments": null,
      "vernacular": null,
      "all_vernaculars": null,
      "species_name": "Pultenaea verruculosa var. verruculosa", # HbvTaxon.name
      "species_code": "PULVERVER", # the one for lookups
      "is_current": "N",
      "naturalised": null,
      "naturalised_status": "N",
      "naturalised_certainty": null,
      "is_eradicated": null,
      "naturalised_comments": null,
      "informal": null,
      "added_on": "1991-12-31Z",
      "updated_on": "2004-12-09Z",
      "consv_code": null,
      "ranking": null,
      "linear_sequence": null,
      "md5_rowhash": "387d5ee88472d3f6f300f3b677ae475a"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to identify the record."),
    )

    name_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    kingdom_id = models.BigIntegerField(
        # refactor: FK Kingdom
        # default: request.user.default_kingdom
        blank=True, null=True,
        verbose_name=_("Kingdom ID"),
        help_text=_("WACensus Kingdom ID."),
    )

    rank_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Rank ID"),
        help_text=_("WACensus Taxonomic Rank ID."),
    )

    rank_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank Name"),
        help_text=_("WACensus Taxonomic Rank Name."),
    )

    family_code = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Family Code"),
        help_text=_("Taxonomic Family Code, deprecated, no not use."),
    )

    family_nid = models.BigIntegerField(
        # refactor: FK Family
        blank=True, null=True,
        verbose_name=_("Family NameID"),
        help_text=_("WACensus Family NameID"),
    )

    # "genus": "Pultenaea", # = HbvTaxon.name1
    # "species": "verruculosa", # = HbvTaxon.name2
    # "infra_rank": "var.", # HbvTaxon.rank3
    # "infra_name": "verruculosa", # HbvTaxon.name3
    # "infra_rank2": null, # HbvTaxon.rank4
    # "infra_name2": null, # HbvTaxon.name4

    genus = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Genus"),
        help_text=_("Taxon name if taxon is of rank kingdom to subgenus."
                    " Genus if taxon is of rank species or below."),
    )

    species = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Species"),
        help_text=_("Empty if taxon is of rank kingdom to subgenus."
                    " Specific epithet if taxon is of rank species or below."),
    )

    infra_rank = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank after species"),
        help_text=_("Whichever rank comes after the species epithet: "
                    "subsp, var, forma, subforma."),
    )

    infra_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name after species name"),
        help_text=_("Whichever name comes after infra_rank."),
    )

    infra_rank2 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Lowest rank"),
        help_text=_("Whichever rank comes after infra_name: "
                    "var, forma, subforma."),
    )

    infra_name2 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Lowest name"),
        help_text=_("Whichever name comes after infra_rank2."),
    )

    author = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Author"),
        help_text=_("Taxonomic Author"),
    )

    editor = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Editor"),
        help_text=_("The rditor of the journal the name was published in."),
    )

    reference = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Reference"),
        help_text=_("The citation for the reference article this name was published in."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments about the name."),
    )

    vernacular = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Preferred Vernacular Name"),
        help_text=_("Preferred Vernacular Name."),
    )

    all_vernaculars = models.TextField(
        blank=True, null=True,
        verbose_name=_("All Vernacular Names"),
        help_text=_("All Vernacular Names in order of preference"
                    " including preferred vernacular name."),
    )

    species_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Name"),
        help_text=_(
            "Built by WACensus by concatenating all name fields, "
            "excluding author and editor. Phrase names may contain authors."),
    )

    species_code = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Species Code"),
        help_text=_("WACensus species shortcode, used for data entry."),
    )

    is_current = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is name current?"),
        help_text=_("WACensus currency status."),
    )

    naturalised = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Naturalised"),
        help_text=_(""),
    )

    naturalised_status = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Naturalisation status"),
        help_text=_("Naturalisation status."),
    )

    naturalised_certainty = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Naturalisation certainty"),
        help_text=_("Naturalisation certainty."),
    )

    naturalised_comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Naturalisation comments"),
        help_text=_("Naturalisation comments."),
    )

    is_eradicated = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is eradicated?"),
        help_text=_("Whether taxon is eradicated or not."),
    )

    informal = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name approval status"),
        help_text=_("The approval status indicates whether a taxonomic name"
                    " is a phrase name (PN), manuscript name (MS) or published (blank)."),
    )
    added_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus added on"),
        help_text=_("Date on which this record was added to WACensus."),
    )
    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    consv_code = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Conservation Code"),
        help_text=_(""),
    )

    ranking = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Ranking"),
        help_text=_(""),
    )

    linear_sequence = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Linear sequence"),
        help_text=_("Always populated for plant families, may be blank for other names."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["kingdom_id", "genus", "species"]
        index_together = [
            ["kingdom_id", "genus", "species"],
        ]
        verbose_name = "HBV Species"
        verbose_name_plural = "HBV Species"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return "[{0}] {1} {2} ({3})".format(
            self.name_id,
            self.species_name,
            self.author,
            self.species_code
        )


class HbvName(models.Model):
    r"""Taxonomic Names from HBVnames.

    Each Taxon has a unique, never re-used, ``name_id``.

    Data are refreshed (overwritten) from
    `KMI HBVnames <https://kmi.dbca.wa.gov.au/geoserver/dpaw/ows?
    service=WFS&version=2.0.0&request=GetFeature
    &typeName=dpaw:herbie_hbvnames&maxFeatures=50&outputFormat=application%2Fjson>`_

    Example taxon:
    {
      "type": "Feature",
      "id": "herbie_hbvnames.fid-3032fae6_1619d7978c8_-6031",
      "geometry": null,
      "properties": {
        "ogc_fid": 0,
        "name_id": 20887,
        "kingdom_id": 3,
        "rank_id": 180,
        "rank_name": "Genus",
        "name1": "Paraceterach",
        "name2": null,
        "rank3": null,
        "name3": null,
        "rank4": null,
        "name4": null,
        "pub_id": 582,
        "vol_info": "75",
        "pub_year": 1947,
        "is_current": "Y",
        "origin": null,
        "naturalised_status": null,
        "naturalised_certainty": null,
        "is_eradicated": null,
        "naturalised_comments": null,
        "informal": null,
        "form_desc_yr": null,
        "form_desc_mn": null,
        "form_desc_dy": null,
        "comments": null,
        "added_by": "HERBIE",
        "added_on": "2004-12-09Z",
        "updated_by": "SUEC",
        "updated_on": "2010-02-03Z",
        "family_code": "008",
        "family_nid": 22721,
        "name": "Paraceterach",
        "full_name": "Paraceterach\nCopel.",
        "author": "Copel.",
        "reference": "Gen.Fil.\n75\n(1947)",
        "editor": null,
        "vernacular": null,
        "all_vernaculars": null,
        "linear_sequence": null,
        "md5_rowhash": "f3e900990365c28fc9d15fe5e4090aa1"
      }
    }
    """

    name_id = models.BigIntegerField(
        unique=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Name"),
        help_text=_(
            "Built by WACensus by concatenating all name fields, "
            "excluding author and editor. Phrase names may contain authors."),
    )

    full_name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Full Name"),
        help_text=_(
            "Built by WACensus by concatenating all name fields, "
            "including author and editor."),
    )

    vernacular = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Preferred Vernacular Name"),
        help_text=_("Preferred Vernacular Name."),
    )

    all_vernaculars = models.TextField(
        blank=True, null=True,
        verbose_name=_("All Vernacular Names"),
        help_text=_("All Vernacular Names in order of preference"
                    " including preferred vernacular name."),
    )

    kingdom_id = models.BigIntegerField(
        # refactor: FK Kingdom
        # default: request.user.default_kingdom
        blank=True, null=True,
        verbose_name=_("Kingdom ID"),
        help_text=_("WACensus Kingdom ID."),
    )

    family_code = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Family Code"),
        help_text=_("Taxonomic Family Code, deprecated, no not use."),
    )

    family_nid = models.BigIntegerField(
        # refactor: FK Family
        blank=True, null=True,
        verbose_name=_("Family NameID"),
        help_text=_("WACensus Family NameID"),
    )

    rank_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Rank ID"),
        help_text=_("WACensus Taxonomic Rank ID."),
    )

    rank_name = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank Name"),
        help_text=_("WACensus Taxonomic Rank Name."),
    )

    name1 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name 1"),
        help_text=_("Taxon name if taxon is of rank kingdom to subgenus."
                    " Genus if taxon is of rank species or below."),
    )

    name2 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name 2"),
        help_text=_("Empty if taxon is of rank kingdom to subgenus."
                    " Specific epithet if taxon is of rank species or below."),
    )

    rank3 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank 3"),
        help_text=_("Whichever rank comes after the species epithet: "
                    "subsp, var, forma, subforma."),
    )

    name3 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name 3"),
        help_text=_("Whichever name comes after rank 3."),
    )

    rank4 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Rank 4"),
        help_text=_("Whichever rank comes after name 3: "
                    "var, forma, subforma."),
    )

    name4 = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name 4"),
        help_text=_("Whichever name comes after rank 4."),
    )

    author = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Author"),
        help_text=_("Taxonomic Author"),
    )

    editor = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Editor"),
        help_text=_("The rditor of the journal the name was published in."),
    )

    reference = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Reference"),
        help_text=_("The citation for the reference article this name was published in."),
    )

    pub_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Publication ID"),
        help_text=_("WACensus Publication ID"),
    )

    vol_info = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Journal Volume Number"),
        help_text=_("Journal Volume Number."),
    )

    pub_year = models.IntegerField(
        blank=True, null=True,
        verbose_name=_("Publication Year"),
        help_text=_("Publication Year."),
    )

    form_desc_yr = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Described on (year)"),
        help_text=_("Year of first description."),
    )

    form_desc_mn = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Described on (month)"),
        help_text=_("Month of first description."),
    )

    form_desc_dy = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Described on (day)"),
        help_text=_("Day of first description."),
    )

    is_current = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is name current?"),
        help_text=_("WACensus currency status."),
    )

    origin = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Origin"),
        help_text=_("Deprecated. * = introduced into WA."),
    )

    naturalised_status = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Naturalisation status"),
        help_text=_("Naturalisation status."),
    )

    naturalised_certainty = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Naturalisation certainty"),
        help_text=_("Naturalisation certainty."),
    )

    naturalised_comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Naturalisation comments"),
        help_text=_("Naturalisation comments."),
    )

    is_eradicated = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Is eradicated?"),
        help_text=_("Whether taxon is eradicated or not."),
    )

    informal = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("Name approval status"),
        help_text=_("The approval status indicates whether a taxonomic name"
                    " is a phrase name (PN), manuscript name (MS) or "
                    "published (blank)."),
    )

    code = models.CharField(
        max_length=1000,
        unique=True,
        blank=True, null=True,
        verbose_name=_("Taxon code"),
        help_text=_("If available, the DBCA six-letter code used in MAX."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments about the name."),
    )

    added_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Added by"),
        help_text=_("The person or system who added this record to WACensus."),
    )

    added_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus added on"),
        help_text=_("Date on which this record was added to WACensus."),
    )

    updated_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Updated by"),
        help_text=_("The person or system who updated this record "
                    "last in WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    linear_sequence = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Linear sequence"),
        help_text=_("Always populated for plant families,"
                    " may be blank for other names."),
    )

    #    "md5_rowhash": "f3e900990365c28fc9d15fe5e4090aa1"
    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to "
                    "identify the record."),
    )

    class Meta:
        """Class options."""

        ordering = ["kingdom_id", "family_nid", "name_id"]
        index_together = [
            ["kingdom_id", "family_nid", "name_id"],
        ]
        verbose_name = "HBV Name"
        verbose_name_plural = "HBV Names"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return "[{0}] {1} ({2})".format(
            self.name_id,
            self.full_name,
            self.vernacular or "")

    def taxonomic_synonyms(self):
        """TODO Return all taxonomic synonyms."""
        return self.__str__()

    def nomenclatural_synonyms(self):
        """TODO Return all nonenclatural synonyms."""
        return self.__str__()

    def current_names(self):
        """TODO Return all current name(s)."""
        return self.__str__()


class HbvVernacular(models.Model):
    r"""Taxonomic vernacular names.

    {//vernacular
      "ogc_fid": 0,
      "name_id": 828,
      "name": "Eleocharis pallens",
      "vernacular": "Pale Spikerush",
      "language": "ENGLISH",
      "lang_pref": null,
      "preferred": "Y",
      "source": "E.M. Bennett",
      "updated_by": "HERBIE",
      "updated_on": "2004-12-09Z",
      "md5_rowhash": "3694af72bc5e906f2d9919c736ad99fe"
    }
    """

    ogc_fid = models.BigIntegerField(
        unique=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to "
                    "identify the record."),
    )

    name_id = models.BigIntegerField(
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Name"),
        help_text=_(
            ""),
    )

    vernacular = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Vernacular Name"),
        help_text=_(
            ""),
    )

    language = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Language"),
        help_text=_("The language of the vernacular name."),
    )

    lang_pref = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Preferred within given language"),
        help_text=_("Whether the vernacular name is the preferred "
                    "name within the given language."),
    )

    preferred = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Preferred vernacular name"),
        help_text=_("Whether this vernacular name is the preferred one "
                    "out of all vernacular names for the given NameID."),
    )

    source = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("source"),
        help_text=_("The source of the vernacular name."),
    )

    updated_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Updated by"),
        help_text=_("The person or system who updated this record "
                    "last in WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        # ordering = ["kingdom_id", "family_nid", "name_id"]
        verbose_name = "HBV Vernacular Name"
        verbose_name_plural = "HBV Vernacular Names"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return self.vernacular


class HbvXref(models.Model):
    r"""Taxonomic operations on NameIDs.

    {//xrefs
      "ogc_fid": 0,
      "xref_id": 1,
      "old_name_id": 8288,
      "new_name_id": null,
      "xref_type": "EXC",
      "active": "Y",
      "authorised_by": null,
      "authorised_on": "        ",
      "comments": null,
      "added_on": "1990-12-03Z",
      "updated_on": null,
      "md5_rowhash": "8a0bb19a2dad98dbe92dbc0caad58eb9"
    }
    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to "
                    "identify the record in GeoServer."),
    )

    xref_id = models.BigIntegerField(
        unique=True,
        blank=True, null=True,
        verbose_name=_("WACensus xref ID"),
        help_text=_("The WACensus xref ID of the record, used to "
                    "identify the record in WACensus."),
    )

    old_name_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("Old NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    new_name_id = models.BigIntegerField(
        blank=True, null=True,
        verbose_name=_("New NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    xref_type = models.CharField(
        max_length=100,
        choices=(
            ("MIS", "Misapplied name"),
            ("TSY", "Taxonomic synonym"),
            ("NSY", "Nomenclatural synonym"),
            ("EXC", "Excluded name"),
            ("CON", "Concept change"),
            ("FOR", "Formal description"),
            ("OGV", "Orthographic variant"),
            ("ERR", "Name in error"),
            ("ISY", "Informal Synonym"),
            # ISY: non-current name pointing to another non-current name
        ),
        blank=True, null=True,
        verbose_name=_("Type"),
        help_text=_("The taxonomic type of this crossreference."),
    )

    active = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Active"),
        help_text=_("Inactive crossrefrences are considered deleted."),
    )

    authorised_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus authorised by"),
        help_text=_("The person or system who authorised this record "
                    "last in WACensus."),
    )

    authorised_on = models.CharField(
        db_index=True,
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus authorised on"),
        help_text=_("Date on which this record was authorised in WACensus."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments are words to clarify things."),
    )

    added_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus added on"),
        help_text=_("Date on which this record was added to WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["authorised_on", ]
        verbose_name = "HBV Crossreference"
        verbose_name_plural = "HBV Crossreferences"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return "{0} {1} {2} on {3}".format(
            self.old_name_id,
            self.xref_type,
            self.new_name_id,
            self.authorised_on)


class HbvParent(models.Model):
    r"""Taxonomic inheritance: name_id is child of parent_nid.

    {"ogc_fid": 0,
    "name_id": 1,
    "class_id": "WAH",
    "parent_nid": 20872,
    "updated_by": "HERBIE",
    "updated_on": "2004-12-09Z",
    "md5_rowhash": "dea886a27ece6a629387fc3ba34392ef"}

    """

    ogc_fid = models.BigIntegerField(
        blank=True, null=True,
        unique=True,
        db_index=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to "
                    "identify the record in GeoServer."),
    )

    name_id = models.BigIntegerField(
        blank=True, null=True,
        db_index=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    class_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus ClassID"),
        help_text=_(""),
    )

    parent_nid = models.BigIntegerField(
        blank=True, null=True,
        db_index=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    updated_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("Updated by"),
        help_text=_("The person or system who updated this record "
                    "last in WACensus."),
    )

    updated_on = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus updated on"),
        help_text=_("Date on which this record was updated in WACensus."),
    )

    md5_rowhash = models.CharField(
        max_length=500,
        blank=True, null=True,
        verbose_name=_("GeoServer MD5 rowhash"),
        help_text=_("An MD5 hash of the record, used to indicate updates."),
    )

    class Meta:
        """Class options."""

        ordering = ["ogc_fid", ]
        verbose_name = "HBV Parent"
        verbose_name_plural = "HBV Parents"
        # get_latest_by = "added_on"

    def __str__(self):
        """The full name."""
        return "{0} is child of {1}".format(
            self.name_id,
            self.parent_nid)


# django-mptt tree models ----------------------------------------------------#


class Taxon(RenderMixin, UrlsMixin, MPTTModel, geo_models.Model):
    """A taxonomic name at any taxonomic rank.

    A taxonomy is a directed graph with exactly one root node (Domain) and
    child nodes at every known rank. Each node has exactly one parent node,
    and can thus infer its taxonomic parentage.

    Each rank can build its correct name based on different rules for each rank.
    Ranks are stored as SmallIntegerField, so that lookups against ranks are fast.

    Status contains the taxon name"s life cycle:

    * A phrase name is created for possibly unknown specimens.
    * A manuscript name is <insert definition>.
    * A formally published name is current.
    * Taxonomic events (xref types) can render a name non-current.
    * Taxonomic events can involve more than one name.

    A legally gazetted name is published every year for names with conservation status.
    The conservation listing (gazettal) process can lag behind the publication
    process by up to a year at the current rate of gazettal (annual).

    Get Parents: https://stackoverflow.com/a/6565577/2813717
    """

    RANK_THING = 0
    RANK_DOMAIN = 5
    RANK_COMMUNITY = 7
    RANK_KINGDOM = 10
    RANK_SUBKINGDOM = 20
    RANK_DIVISION = 30
    RANK_SUBDIVISION = 40
    RANK_CLASS = 50
    RANK_SUBCLASS = 60
    RANK_ORDER = 70
    RANK_SUBORDER = 80
    RANK_FAMILY = 90
    RANK_SUBFAMILY = 100
    RANK_TRIBE = 110
    RANK_SUBTRIBE = 120
    RANK_GENUS = 130
    RANK_SUBGENUS = 140
    RANK_SECTION = 150
    RANK_SUBSECTION = 160
    RANK_SERIES = 170
    RANK_SUBSERIES = 180
    RANK_SPECIES = 190
    RANK_SUBSPECIES = 200
    RANK_VARIETY = 210
    RANK_SUBVARIETY = 220
    RANK_FORMA = 230
    RANK_SUBFORMA = 240

    RANKS = (
        # (RANK_THING, "Thing"),
        # (RANK_COMMUNITY, "Community"),
        (RANK_DOMAIN, "Domain"),
        (RANK_KINGDOM, "Kingdom"),
        (RANK_SUBKINGDOM, "Subkingdom"),
        (RANK_DIVISION, "Division"),
        (RANK_SUBDIVISION, "Subdivision"),
        (RANK_CLASS, "Class"),
        (RANK_SUBCLASS, "Subclass"),
        (RANK_ORDER, "Order"),
        (RANK_SUBORDER, "Suborder"),
        (RANK_FAMILY, "Family"),
        (RANK_SUBFAMILY, "Subfamily"),
        (RANK_TRIBE, "Tribe"),
        (RANK_SUBTRIBE, "Subtribe"),
        (RANK_GENUS, "Genus"),
        (RANK_SUBGENUS, "Subgenus"),
        (RANK_SECTION, "Section"),
        (RANK_SUBSECTION, "Subsection"),
        (RANK_SERIES, "Series"),
        (RANK_SUBSERIES, "Subseries"),
        (RANK_SPECIES, "Species"),
        (RANK_SUBSPECIES, "Subspecies"),
        (RANK_VARIETY, "Variety"),
        (RANK_SUBVARIETY, "Subvariety"),
        (RANK_FORMA, "Forma"),
        (RANK_SUBFORMA, "Subforma")
    )

    RANK_ABBREVIATIONS = {
        RANK_SUBSPECIES: "subsp.",
        RANK_VARIETY: "var.",
        RANK_SUBVARIETY: "subvar.",
        RANK_FORMA: "forma",
        RANK_SUBFORMA: "subf.",
    }

    PUBLICATION_STATUS_PHRASE_NAME = 0
    PUBLICATION_STATUS_MANUSCRIPT_NAME = 1
    PUBLICATION_STATUS_PUBLISHED_NAME = 2

    PUBLICATION_STATUS = (
        (PUBLICATION_STATUS_PHRASE_NAME, "Phrase Name"),
        (PUBLICATION_STATUS_MANUSCRIPT_NAME, "Manuscript Name"),
        (PUBLICATION_STATUS_PUBLISHED_NAME, "Published Name"),
    )

    name_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        verbose_name=_("NameID"),
        help_text=_("WACensus NameID, assigned by WACensus."),
    )

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="children",
        db_index=True,
        verbose_name=_("Parent Taxon"),
        help_text=_("The lowest known parent taxon."),
    )

    paraphyletic_groups = models.ManyToManyField(
        HbvSupra,
        blank=True,
        verbose_name=_("Groups"),
        help_text=_("All paraphyletic groups this taxon belongs to."),
    )

    supra_group = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("HBV Suprafamily Group"),
        help_text=_("A possibly paraphyletic supragroup for convenient subsetting."),
    )

    rank = models.PositiveSmallIntegerField(
        choices=RANKS,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Taxonomic Rank"),
        help_text=_("The taxonomic rank of the taxon."),
    )

    name = models.CharField(
        max_length=1000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Taxon Name"),
        help_text=_("The taxon name.")
    )

    canonical_name = models.CharField(
        max_length=2000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Canonical Name"),
        help_text=_("The canonical name.")
    )

    taxonomic_name = models.CharField(
        max_length=2000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Taxonomic Name"),
        help_text=_("The taxonomic name.")
    )

    vernacular_name = models.CharField(
        max_length=2000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Preferred English Vernacular Name"),
        help_text=_("The preferred english vernacular name.")
    )

    field_code = models.CharField(
        max_length=2000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Field collection code"),
        help_text=_("The agreed acronym, often used on paper datasheets.")
    )

    vernacular_names = models.TextField(
        db_index=True,
        blank=True, null=True,
        verbose_name=_("All Vernacular Names"),
        help_text=_("A list of all vernacular names.")
    )

    author = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Author"),
        help_text=_("Taxonomic Author"),
    )

    publication_status = models.PositiveSmallIntegerField(
        db_index=True,
        choices=PUBLICATION_STATUS,
        default=PUBLICATION_STATUS_PUBLISHED_NAME,
        verbose_name=_("Publication Status"),
        help_text=_("On what level the name is published."),
    )

    current = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Is current"),
        help_text=_("Whether the name is current."),
    )

    eoo = geo_models.PolygonField(
        srid=4326,
        blank=True, null=True,
        verbose_name=_("Extent of Occurrence"),
        help_text=_("The extent of occurrence as polygon in WGS84, if available."))

    # Approval Status FSM: [phrase name, ms name, current name, non-current name]
    # status = FSMField(default=STATUS_NEW, choices=STATUS_CHOICES, verbose_name=_("QA Status"))

    class MPTTMeta:
        """MPTT Class options."""

        order_insertion_by = ["name_id"]
        ordering = ['-rank', 'current']
        index_together = [
            ['rank', 'current'],
        ]

    class Meta:
        """Class options."""

        verbose_name = "Taxon"
        verbose_name_plural = "Taxa"

    def __str__(self):
        """The full name: [NameID] (RANK) TAXONOMIC NAME."""
        return "[{0}][{1}] ({2}) {3}".format(
            self.name_id,
            self.field_code if self.field_code else "",
            self.get_rank_display(),
            self.name if not self.taxonomic_name else self.taxonomic_name)

    # -------------------------------------------------------------------------
    # URLs
    def get_absolute_url(self):
        """Detail url."""
        return reverse('taxonomy:taxon-detail', kwargs={"name_id": self.name_id})

    @property
    def update_url(self):
        """Admin update url."""
        self.absolute_admin_url

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def build_canonical_name(self):
        """Build the canonical name.

        * Anything above species: [NameID] NAME
        * Species: [NameID] RANK GENUS NAME
        * Subspecies and lower: [NameID] RANK GENUS SPECIES RANK NAME
        """
        if self.rank == Taxon.RANK_SPECIES:
            genus = self.get_ancestors().filter(rank=Taxon.RANK_GENUS).first()
            return "{0} {1}".format("GENUS" if not genus else genus.name, self.name)

        elif self.rank > Taxon.RANK_SPECIES:
            genus = self.get_ancestors().filter(rank=Taxon.RANK_GENUS).first()
            species = self.get_ancestors().filter(rank=Taxon.RANK_SPECIES).first()
            return "{0} {1} {2} {3}".format(
                "GENUS" if not genus else genus.name,
                "SPECIES" if not species else species.name,
                Taxon.RANK_ABBREVIATIONS[self.rank],
                self.name)
        else:
            return self.name

    @property
    def build_taxonomic_name(self):
        """Build the taxonomic name."""
        if self.author:
            return "{0} ({1})".format(
                self.build_canonical_name,
                self.author.replace("(", "").replace(")", "").strip()
            )
        else:
            return self.build_canonical_name

    @property
    def build_vernacular_name(self):
        """Return the preferred english, or the first available vernacular name."""
        vv = self.vernacular_set.all()
        if vv.filter(language=Vernacular.LANGUAGE_ENGLISH, preferred=True):
            n = vv.filter(language=Vernacular.LANGUAGE_ENGLISH, preferred=True).first().name
        elif vv.filter(language=Vernacular.LANGUAGE_ENGLISH):
            n = vv.filter(language=Vernacular.LANGUAGE_ENGLISH).first().name
        elif vv:
            n = vv.first().name
        else:
            n = ""
        return n

    @property
    def build_vernacular_names(self):
        """Return a comma-separated list of all vernacular names."""
        return ", ".join([x.name for x in self.vernacular_set.all() if x.name])

    @property
    def gazettals(self):
        """Return a dict of TaxonConservationListing labels and admin URLs."""
        from conservation import models as cons_models
        return cons_models.TaxonConservationListing.objects.filter(taxon__pk=self.pk)

    @property
    def active_gazettals(self):
        """Return a dict of active TaxonConservationListing labels and admin URLs."""
        from conservation import models as cons_models
        return cons_models.TaxonConservationListing.active.filter(taxon__pk=self.pk)

    @property
    def active_conservation_listing_state(self):
        """Return the first active conservation listing in state scope or None."""
        from conservation import models as cons_models
        return cons_models.TaxonConservationListing.active_state.filter(taxon__pk=self.pk).first()

    @property
    def active_conservation_listing_national(self):
        """Return the first active conservation listing in national scope or None."""
        from conservation import models as cons_models
        return cons_models.TaxonConservationListing.active_national.filter(taxon__pk=self.pk).first()

    # @property
    # def documents(self):
    #     """Return a dict of Documents and admin urls."""
    #     return [{'obj': x,
    #              'url': x.absolute_admin_url}
    #             for x in self.document_set.all()]

    @property
    def is_currently_listed(self):
        """Whether this Taxon has a current conservation listing."""
        from conservation import models as cons_models
        return cons_models.TaxonConservationListing.active.filter(taxon__pk=self.pk).exists()

    # Properties used in API -------------------------------------------------#
    @property
    def conservation_code_state(self):
        """A shorthand conservation code for the current state listing.

        Values: T, 1,2,3,4,5
        T: any listing with conservation category CR, EN, VU
        1..5: Priority listings of levels P1 through P5

        From the current state listing, get the conservation code
        ConservationListing.conservation_code is a property returning
        the highest code (X,T,1..5) of all categories.
        """
        cl = self.active_conservation_listing_state
        if cl:
            # TODO return cl.category.first().conservation_shortcode
            return cl.category.__str__()

        else:
            return None

    @property
    def conservation_list_state(self):
        """The conservation list name for the current state listing.

        From the current state listing, get the name.
        """
        cl = self.active_conservation_listing_state
        if cl:
            return cl.category.first().conservation_list.code
        else:
            return None

    @property
    def conservation_category_state(self):
        """The primary conservation category for the current state listing.

        The categories are ordered by their rank.
        The Threatened categories (CR, EN, VU) are above the
        international agreements (MI, MA, CT).
        The first available category is returned as the primary one.

        TODO test that MI/MA/CT are returned only if no CR/EN/VU present.
        """
        cl = self.active_conservation_listing_state
        if cl:
            return cl.category.first().code
        else:
            return None

    @property
    def conservation_categories_state(self):
        """All conservation categories for the current state listing.

        The categories are stored in category_cache.
        """
        cl = self.active_conservation_listing_state
        if cl:
            return cl.category_cache
        else:
            return None

    @property
    def conservation_criteria_state(self):
        """The list of conservation criteria for the current state listing.

        The criteria are stored in criteria_cache.
        """
        cl = self.active_conservation_listing_state
        if cl:
            return cl.criteria_cache
        else:
            return None

    @property
    def conservation_category_national(self):
        """The primary conservation category for the current national listing.

        The categories are ordered by their rank.
        The Threatened categories (CR, EN, VU) are above the
        international agreements (MI, MA, CT).
        The first available category is returned as the primary one.

        TODO test that MI/MA/CT are returned only if no CR/EN/VU present.
        """
        cl = self.active_conservation_listing_national
        if cl:
            return cl.category.first().code
        else:
            return None


@receiver(pre_save, sender=Taxon)
def taxon_pre_save(sender, instance, *args, **kwargs):
    """Taxon: Build names (expensive lookups).

    TODO: cache conservation listing lookups.
    """
    try:
        instance.canonical_name = instance.build_canonical_name
        instance.taxonomic_name = instance.build_taxonomic_name
    except:
        logger.info("[taxon_pre_save] New Taxon, re-save to build canonical/taxonomic name.")
    instance.vernacular_name = instance.build_vernacular_name
    instance.vernacular_names = instance.build_vernacular_names


class Vernacular(models.Model):
    """Vernacular Name."""

    LANGUAGE_ENGLISH = 0
    LANGUAGE_INDIGENOUS = 1
    LANGUAGES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_INDIGENOUS, "Indigenous"),
    )

    ogc_fid = models.BigIntegerField(
        unique=True,
        verbose_name=_("GeoServer OGC FeatureID"),
        help_text=_("The OCG Feature ID of the record, used to "
                    "identify the record."),
    )

    taxon = models.ForeignKey(
        Taxon,
        on_delete=models.CASCADE,
        verbose_name=_("Taxon"),
        help_text=_("The taxon this vernacular name applies to.")
    )

    name = models.CharField(
        max_length=1000,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Vernacular Name"),
        help_text=_("The vernacular name.")
    )

    language = models.PositiveSmallIntegerField(
        choices=LANGUAGES,
        db_index=True,
        blank=True, null=True,
        verbose_name=_("Language"),
        help_text=_("The language of the vernacular name."),
    )

    preferred = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Is preferred"),
        help_text=_("Whether the vernacular name is the "
                    "preferred name in the given language."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Vernacular Name"
        verbose_name_plural = "Vernacular Names"

    def __str__(self):
        """The vernacular name: [NameID] (RANK) TAXONOMIC NAME."""
        return "[{0}] {1}".format(
            self.taxon.name_id,
            self.name)


class Crossreference(models.Model):
    """Taxonomic crossreference."""

    REASON_MIS = 0
    REASON_TSY = 1
    REASON_NSY = 2
    REASON_EXC = 3
    REASON_CON = 4
    REASON_FOR = 5
    REASON_OGV = 6
    REASON_ERR = 7
    REASON_ISY = 8
    REASONS = (
        (REASON_MIS, "Misapplied name"),
        (REASON_TSY, "Taxonomic synonym"),
        (REASON_NSY, "Nomenclatural synonym"),
        (REASON_EXC, "Excluded name"),
        (REASON_CON, "Concept change"),
        (REASON_FOR, "Formal description"),
        (REASON_OGV, "Orthographic variant"),
        (REASON_ERR, "Name in error"),
        (REASON_ISY, "Informal Synonym"),
        # ISY: non-current name pointing to another non-current name
    )

    xref_id = models.BigIntegerField(
        unique=True,
        blank=True, null=True,
        verbose_name=_("WACensus xref ID"),
        help_text=_("The WACensus xref ID of the record."),
    )

    predecessor = models.ForeignKey(
        Taxon,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_("Predecessor Taxon"),
        related_name="precedes",
        help_text=_("The old taxon.")
    )

    successor = models.ForeignKey(
        Taxon,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name=_("Successor Taxon"),
        related_name="supercedes",
        help_text=_("The new taxon.")
    )

    reason = models.PositiveSmallIntegerField(
        choices=REASONS,
        default=REASON_ERR,
        db_index=True,
        verbose_name=_("Reason"),
        help_text=_("The reason for the taxonomic change."),
    )

    authorised_by = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_("WACensus authorised by"),
        help_text=_("The person or system who authorised this record "
                    "last in WACensus."),
    )

    authorised_on = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_("WACensus authorised on"),
        help_text=_("Date on which this record was authorised in WACensus."),
    )

    effective_to = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_("WACensus deactivated on"),
        help_text=_("Xref considered deleted after this date if set."),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Comments are words to clarify things."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Crossreference"
        verbose_name_plural = "Crossreferences"

    def __str__(self):
        """The name."""
        return "[{0} > {1}] {2}".format(
            "x" if not self.predecessor else self.predecessor.name_id,
            "x" if not self.successor else self.successor.name_id,
            self.get_reason_display())

    @property
    def involved_taxon_ids(self):
        """Return a list of all involved taxa."""
        pre = [x.pk for x in self.predecessor.get_ancestors()] if self.predecessor else []
        suc = [x.pk for x in self.successor.get_ancestors()] if self.successor else []
        return list(set(pre + suc))


class Community(RenderMixin, UrlsMixin, LegacySourceMixin, geo_models.Model):
    """Ecological Community."""

    code = models.CharField(
        max_length=1000,
        db_index=True,
        unique=True,
        blank=True, null=True,
        verbose_name=_("Community code"),
        help_text=_("A short community codename."),
    )

    name = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Community name"),
        help_text=_("A full community name."),
    )

    description = models.TextField(
        blank=True, null=True,
        verbose_name=_("Community description"),
        help_text=_("An optional description."),
    )

    eoo = geo_models.PolygonField(
        srid=4326,
        blank=True, null=True,
        verbose_name=_("Extent of Occurrence"),
        help_text=_("The extent of occurrence as polygon in WGS84, if available."))

    # add cache fields here

    class Meta:
        """Class options."""

        verbose_name = "Community"
        verbose_name_plural = "Communities"
        ordering = ["code", ]

    def __str__(self):
        """The name."""
        return self.code

    # -------------------------------------------------------------------------
    # URLs
    @property
    def update_url(self):
        """Admin update url."""
        return self.absolute_admin_url

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def gazettals(self):
        """Return a dict of TaxonConservationListing labels and admin URLs."""
        from conservation import models as cons_models
        return cons_models.CommunityConservationListing.objects.filter(community__pk=self.pk)

    @property
    def active_gazettals(self):
        """Return a dict of active TaxonConservationListing labels and admin URLs."""
        from conservation import models as cons_models
        return cons_models.CommunityConservationListing.active.filter(community__pk=self.pk)
