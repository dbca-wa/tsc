# -*- coding: utf-8 -*-
""".

Taxonomy view tests
^^^^^^^^^^^^^^^^^^^

View tests call every page and verify that

* each URL works,
* each page loads,
* each page uses the correct templates,
* each page shows all expected data and features.

"""
from __future__ import unicode_literals

from django.conf import settings
from django.utils import timezone  # noqa
# from django.http import Http404
from django.contrib.auth import get_user_model  # noqa
from django.contrib.gis.geos import GEOSGeometry  # Point, Polygon  # noqa
from django.test import TestCase  # noqa
from django.urls import reverse  # noqa
from model_mommy import mommy  # noqa
from mommy_spatial_generators import MOMMY_SPATIAL_FIELDS  # noqa

from conservation import models as cons_models
from taxonomy.models import Community, Taxon, Crossreference, Vernacular
from wastd.observations.models import Area
# from django.contrib.contenttypes.models import ContentType

MOMMY_CUSTOM_FIELDS_GEN = MOMMY_SPATIAL_FIELDS


from taxonomy.models import Community, Taxon  # noqa


class CommunityViewTests(TestCase):
    """Community tests."""

    fixtures = ['taxonomy/fixtures/test_taxonomy.json', ]

    def setUp(self):
        """Shared objects."""
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()

        self.com1 = mommy.make(
            Community,
            code="code1",
            name="name1",
            _fill_optional=['eoo'])
        self.com1.save()

        self.taxon0 = mommy.make(
            Taxon,
            name_id=1000,
            name="name0",
            _fill_optional=['rank', 'eoo'])
        self.taxon0.save()

        self.consthreatcat = cons_models.ConservationThreatCategory.objects.create(
            code="weeds", label="Weeds", description="invasive weeds")
        self.consthreat = cons_models.ConservationThreat.objects.create(
            category=self.consthreatcat, cause="burn some stuff")
        self.consthreat.taxa.add(self.taxon0)
        self.consthreat.communities.add(self.com0)

        self.consactioncat = cons_models.ConservationActionCategory.objects.create(
            code="burn", label="Burn", description="Burn everything")
        self.consaction = cons_models.ConservationAction.objects.create(
            category=self.consactioncat, instructions="burn some stuff")
        self.consaction.taxa.add(self.taxon0)
        self.consaction.communities.add(self.com0)

        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_com_creation(self):
        """Test creating a Community."""
        self.assertTrue(isinstance(self.com0, Community))

    def test_com_absolute_admin_url_loads(self):
        """Test Community absolute_admin_url."""
        response = self.client.get(self.com0.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_com_list_url_loads(self):
        """Test community-list."""
        response = self.client.get(self.com0.list_url())
        self.assertEqual(response.status_code, 200)

        wa_poly = '{"type":"Polygon","coordinates":[[[110,-35],[110,-10],[135,-10],[135,-35],[110,-35]]]}'

        a, created = Area.objects.get_or_create(name="WA", geom=wa_poly)
        response = self.client.get(self.com0.list_url() + "?admin_areas={0}".format(a.pk))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.com0.list_url() + "?eoo=" + wa_poly)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.com0.list_url() + "?aoo=" + wa_poly)
        self.assertEqual(response.status_code, 200)

        # cat1 = cons_models.ConservationCategory.objects.first()
        # cat2 = cons_models.ConservationCategory.objects.last()

        # response = self.client.get(self.com0.list_url() + "?categories=" + cat1.pk)
        # self.assertEqual(response.status_code, 200)

        # response = self.client.get(self.com0.list_url() + "?categories=" + cat1.pk + "&categories=" + cat2.pk)
        # self.assertEqual(response.status_code, 200)

    def test_com_detail_url_loads(self):
        """Test Community detail_url."""
        response = self.client.get(self.com0.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    # def test_com_update_url_loads(self):
    #     """Test Community update_url."""
    #     response = self.client.get(self.com0.update_url)
    #     self.assertEqual(response.status_code, 200)


class TaxonViewTests(TestCase):
    """Taxon view tests."""

    fixtures = ['taxonomy/fixtures/test_taxonomy.json', ]

    def setUp(self):
        """Shared objects."""
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()

        self.com1 = mommy.make(
            Community,
            code="code1",
            name="name1",
            _fill_optional=['eoo'])
        self.com1.save()

        self.taxon0 = mommy.make(
            Taxon,
            name_id=1000,
            name="name0",
            publication_status=0,
            _fill_optional=['rank', 'eoo', ])
        self.taxon0.save()
        self.ver0 = mommy.make(Vernacular, taxon=self.taxon0, name="vern0", language=Vernacular.LANGUAGE_ENGLISH)
        self.taxon0.save()

        self.taxon1 = mommy.make(
            Taxon,
            name_id=1001,
            name="name1",
            current=True,
            publication_status=1,
            parent=self.taxon0,
            author="ze author",
            vernacular_name="some vernacular name",
            vernacular_names="some vernacular name",
            _fill_optional=['rank', 'eoo'])
        self.taxon1.save()
        self.ver1a = mommy.make(Vernacular, taxon=self.taxon1, name="vern1a",
                                language=Vernacular.LANGUAGE_ENGLISH, preferred=True)
        self.ver1b = mommy.make(Vernacular, taxon=self.taxon1, name="vern1b",
                                language=Vernacular.LANGUAGE_ENGLISH)
        self.taxon1.save()

        self.taxon2 = mommy.make(
            Taxon,
            name_id=1002,
            name="name2",
            publication_status=2,
            _fill_optional=['rank', 'eoo'])
        self.taxon2.save()

        self.xref01 = Crossreference.objects.create(
            predecessor=self.taxon1,
            successor=self.taxon0,
            reason=Crossreference.REASON_TSY
        )

        self.xref12 = Crossreference.objects.create(
            predecessor=self.taxon0,
            successor=self.taxon2,
            reason=Crossreference.REASON_TSY
        )

        # add vernaculars

        self.consthreatcat = cons_models.ConservationThreatCategory.objects.create(
            code="weeds", label="Weeds", description="invasive weeds")
        self.consthreat = cons_models.ConservationThreat.objects.create(
            category=self.consthreatcat, cause="weeds are invading")
        self.consthreat.taxa.add(self.taxon0)
        self.consthreat.taxa.add(self.taxon1)
        self.consthreat.taxa.add(self.taxon2)
        self.consthreat.communities.add(self.com0)
        self.consthreat.communities.add(self.com1)

        self.consactioncat = cons_models.ConservationActionCategory.objects.create(
            code="burn", label="Burn", description="Burn everything")
        self.consaction = cons_models.ConservationAction.objects.create(
            category=self.consactioncat, instructions="burn some stuff")
        self.consaction.taxa.add(self.taxon0)
        self.consaction.communities.add(self.com0)

        # TODO add cons threats with area code

        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()

        self.doc = mommy.make(cons_models.Document)
        self.doc.taxa.add(self.taxon0)
        self.doc.save()

        self.client.force_login(self.user)

    def test_taxon_creation(self):
        """Test creating a Taxon."""
        self.assertTrue(isinstance(Taxon.objects.last(), Taxon))

    def test_taxon_absolute_admin_url_loads(self):
        """Test Taxon absolute_admin_url."""
        response = self.client.get(Taxon.objects.last().absolute_admin_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.taxon0.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_taxon_list_url_loads(self):
        """Test taxon-list."""
        list_url = Taxon.list_url()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)

        wa_poly = '{"type":"Polygon","coordinates":[[[110,-35],[110,-10],[135,-10],[135,-35],[110,-35]]]}'
        a, created = Area.objects.get_or_create(name="WA", geom=wa_poly)

        for filter_args in [
            "?paraphyletic_groups={0}&is_terminal_taxon=true".format(settings.ANIMALS_PK),
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=threatened&conservation_level=priority".format(settings.ANIMALS_PK),  # noqa
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=priority".format(settings.ANIMALS_PK),
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=threatened".format(settings.ANIMALS_PK),
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=threatened&conservation_level=priority".format(settings.PLANTS_PK),  # noqa
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=threatened".format(settings.PLANTS_PK),
            "?paraphyletic_groups={0}&is_terminal_taxon=true&conservation_level=priority".format(settings.PLANTS_PK),
            "?is_terminal_taxon=true",
            "?admin_areas=a.pk",
            '?eoo={"type"%3A"Polygon"%2C"coordinates"%3A[[[111.357422%2C-30.190717]%2C[111.357422%2C-24.974106]%2C[122.519531%2C-24.974106]%2C[122.519531%2C-30.190717]%2C[111.357422%2C-30.190717]]]}',  # noqa
            '?aoo={"type"%3A"Polygon"%2C"coordinates"%3A[[[111.357422%2C-30.190717]%2C[111.357422%2C-24.974106]%2C[122.519531%2C-24.974106]%2C[122.519531%2C-30.190717]%2C[111.357422%2C-30.190717]]]}',  # noqa
            # "?categories=5&categories=2&categories=3", # needs cons cat
            # TODO add other filters
        ]:
            response = self.client.get(list_url + filter_args)
            self.assertEqual(response.status_code, 200)

    def test_taxon_list_url_with_nameid(self):
        """Test taxon-list with name_id.

        * taxon-list with valid name_id should load.
        * taxon-list with invalid name_id should still load but show warning.
        """
        response = self.client.get("{0}?name_id={1}".format(
            Taxon.list_url(),
            Taxon.objects.last().name_id)
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("{0}?name_id=-5000000".format(self.taxon0.list_url()))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This Name ID does not exist.")

    def test_taxon_detail_url_loads(self):
        """Test Taxon detail_url."""
        response = self.client.get(self.taxon0.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.taxon1.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        # TODO test crossreference urls
        url = reverse('taxonomy:taxon-detail', kwargs={'name_id': -50000000})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # def test_taxon_update_url_loads(self):
    #     """Test Taxon update_url."""
    #     self.client.force_login(self.user)
    #     response = self.client.get(self.taxon0.update_url)
    #     self.assertEqual(response.status_code, 200)

    def test_taxon_detail_url_shows_all_vernaculars(self):
        """Test Taxon detail_url shows preferred and vernacular names (if different to preferred)."""
        # taxon0: additional vernacular names
        response = self.client.get(self.taxon0.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'taxonomy/include/vernaculars.html')
        # print("Taxon 0 vn: {0}, vnames: {1}".format(self.taxon0.vernacular_name, self.taxon0.vernacular_names))
        self.assertEqual(self.taxon0.vernacular_name, self.taxon0.vernacular_names)
        self.assertContains(response, self.taxon0.vernacular_name)

        # taxon 1: only perferred vernacular names
        response = self.client.get(self.taxon1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'taxonomy/include/vernaculars.html')
        # print("Taxon 1 vn: {0}, vnames: {1}".format(self.taxon0.vernacular_name, self.taxon0.vernacular_names))
        self.assertNotEqual(self.taxon1.vernacular_name, self.taxon1.vernacular_names)
        self.assertContains(response, self.taxon1.vernacular_name)
        self.assertContains(response, self.taxon1.vernacular_names)


class TaxonBulkViewTests(TestCase):
    """Taxon view tests."""

    fixtures = [
        'taxonomy/fixtures/test_taxonomy.json',
        'taxonomy/fixtures/test_wacensus.json',
    ]

    def test_taxon_list_url_loads(self):
        """Test taxon-list with filters."""
        t = Taxon.objects.last()
        response = self.client.get(t.list_url())
        self.assertEqual(response.status_code, 200)

        wa_poly = '{"type":"Polygon","coordinates":[[[110,-35],[110,-10],[135,-10],[135,-35],[110,-35]]]}'

        a, created = Area.objects.get_or_create(name="WA", geom=wa_poly)
        response = self.client.get(t.list_url() + "?admin_areas={0}".format(a.pk))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(t.list_url() + "?eoo=" + wa_poly)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(t.list_url() + "?aoo=" + wa_poly)
        self.assertEqual(response.status_code, 200)

        # Requires conservation list and categories
        # cat1 = cons_models.ConservationCategory.objects.first()
        # cat2 = cons_models.ConservationCategory.objects.last()

        # response = self.client.get(t.list_url() + "?categories=" + cat1.pk)
        # self.assertEqual(response.status_code, 200)

        # response = self.client.get(t.list_url() + "?categories=" + cat1.pk + "&categories=" + cat2.pk)
        # self.assertEqual(response.status_code, 200)

    def test_taxon_detail_url_loads(self):
        """Test Taxon detail_url."""
        t = Taxon.objects.last()
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_update_taxon_view(self):
        """Test the update_taxon view."""
        url = reverse("taxonomy:task-update-taxon")
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()

        # works and redirects to home view
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
