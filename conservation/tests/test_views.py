# -*- coding: utf-8 -*-
"""Conservation view test suite testing URLs, templates, and views.

* [REQ 40] Include the following dashboard pages:
  * Dashboard of all plans: document list view and templates
  * Dashboard of all annual reports for all plans: document list view, filter plan type
  From within a dashboard, the user to open an entity and view the details.
  Test that document card contains detail link.
  Dashboard to show when details were last edited.
  Test that document card contains date last modified.


See also:
https://model-mommy.readthedocs.io/en/latest/
https://github.com/sigma-geosistemas/mommy_spatial_generators
"""
from __future__ import unicode_literals

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry  # Point, Polygon   # noqa
from django.core.files.uploadedfile import SimpleUploadedFile  # noqa
from django.test import TestCase
from django.urls import reverse  # noqa
from model_mommy import mommy  # noqa
from mommy_spatial_generators import MOMMY_SPATIAL_FIELDS  # noqa
from taxonomy.models import Taxon, Community
from wastd.observations.models import Area
from conservation import models as cons_models


class ConservationThreatViewTests(TestCase):
    """View tests for ConservationThreat."""

    def setUp(self):
        """Set up."""
        self.taxon0 = mommy.make(
            Taxon,
            name_id=1000,
            name="name0",
            _fill_optional=['rank', 'eoo'])
        self.taxon0.save()
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()
        self.doc = cons_models.Document.objects.create(
            title="test doc",
            document_type=cons_models.Document.TYPE_RECOVERY_PLAN,
            # attachment=self.fatt1
            # TODO add dates
        )
        self.consthreatcat = cons_models.ConservationThreatCategory.objects.create(
            code="weeds",
            label="Weeds",
            description="invasive weeds"
        )
        self.object = cons_models.ConservationThreat.objects.create(
            category=self.consthreatcat,
            cause="burn some stuff",
            document=self.doc
        )
        self.object.taxa.add(self.taxon0)
        self.object.communities.add(self.com0)
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_conservation_threat_absolute_admin_url(self):
        """Test ConservationThreat absolute admin url."""
        response = self.client.get(self.object.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_conservation_threat_admin_changelist(self):
        """Test ConservationThreat absolute admin url."""
        url = reverse("admin:conservation_conservationthreat_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        """Test ConservationAction get absolute url loads."""
        response = self.client.get(self.object.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_list_url_loads(self):
        """Test conservationaction-list loads."""
        response = self.client.get(self.object.list_url())
        self.assertEqual(response.status_code, 200)

        # test filter by one and many admin_areas

    def test_create_url_loads(self):
        """Test conservationaction-create loads."""
        response = self.client.get(self.object.create_url())
        self.assertEqual(response.status_code, 200)

    def test_update_url_loads(self):
        """Test conservationaction-update url loads."""
        response = self.client.get(self.object.update_url)
        self.assertEqual(response.status_code, 200)


class ConservationActionCategoryViewTests(TestCase):
    """View tests for ConservationActionCategory."""

    def setUp(self):
        """Set up."""
        self.object = cons_models.ConservationActionCategory.objects.create(
            code="burn", label="Burn", description="Burn everything")
        self.consaction = cons_models.ConservationAction.objects.create(
            category=self.object,
            instructions="burn some stuff"
        )
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_conservation_action_category_absolute_admin_url(self):
        """Test ConservationActionCategory absolute admin url."""
        response = self.client.get(self.object.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_admin_list_action(self):
        """Test admin change list for ConservationAction."""
        url = reverse("admin:conservation_conservationaction_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ConservationActionViewTests(TestCase):
    """View tests for ConservationAction."""

    def setUp(self):
        """Set up."""
        self.taxon0 = mommy.make(
            Taxon,
            name_id=1000,
            name="name0",
            _fill_optional=['rank', 'eoo'])
        self.taxon0.save()
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()
        self.consactioncat = cons_models.ConservationActionCategory.objects.create(
            code="burn", label="Burn", description="Burn everything")
        self.object = cons_models.ConservationAction.objects.create(
            category=self.consactioncat, instructions="burn some stuff")
        self.object.taxa.add(self.taxon0)
        self.object.communities.add(self.com0)
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_conservation_action_absolute_admin_url(self):
        """Test ConservationAction absolute admin url."""
        response = self.client.get(self.object.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        """Test ConservationAction get absolute url loads."""
        response = self.client.get(self.object.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_list_url_loads(self):
        """Test conservationaction-list loads."""
        response = self.client.get(self.object.list_url())
        self.assertEqual(response.status_code, 200)

        # test filter by one and many admin_areas

    def test_create_url_loads(self):
        """Test conservationaction-create loads."""
        response = self.client.get(self.object.create_url())
        self.assertEqual(response.status_code, 200)

    def test_update_url_loads(self):
        """Test conservationaction-update url loads."""
        response = self.client.get(self.object.update_url)
        self.assertEqual(response.status_code, 200)


class ConservationActivityViewTests(TestCase):
    """View tests for ConservationActivity."""

    def setUp(self):
        """Set up."""
        self.consactioncat = cons_models.ConservationActionCategory.objects.create(
            code="burn", label="Burn", description="Burn everything")
        self.consaction = cons_models.ConservationAction.objects.create(
            category=self.consactioncat,
            instructions="burn some stuff"
        )
        self.object = cons_models.ConservationActivity.objects.create(
            conservation_action=self.consaction,
        )
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_conservation_activity_absolute_admin_url(self):
        """Test ConservationActivity absolute admin url."""
        response = self.client.get(self.object.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        """Test ConservationAction get absolute url."""
        response = self.client.get(self.object.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_list_url_loads(self):
        """Test conservationactivity-list."""
        response = self.client.get(self.object.list_url())
        self.assertEqual(response.status_code, 200)

    def test_create_url_loads(self):
        """Test conservationactivity-create."""
        response = self.client.get(self.object.create_url(self.consaction))
        self.assertEqual(response.status_code, 200)

    def test_update_url_loads(self):
        """Test conservationactivity-update."""
        response = self.client.get(self.object.update_url)
        self.assertEqual(response.status_code, 200)

    def test_conservation_activity_str(self):
        """Test ConservationActivity str."""
        label = "[{0}][{1}] {2}".format(
            self.object.conservation_action.category,
            self.object.completion_date.strftime("%d/%m/%Y")
            if self.object.completion_date else "in progress",
            self.object.implementation_notes)
        self.assertEqual(label, self.object.__str__())


class ConservationListViewTests(TestCase):
    """ConservationList view tests."""

    def setUp(self):
        """Setup: create a new list."""
        self.cl = cons_models.ConservationList.objects.create(
            code='test',
            label='test list',
            approval_level=cons_models.ConservationList.APPROVAL_IMMEDIATE)
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_conservationlist_absolute_admin_url(self):
        """Test ConservationList absolute admin url."""
        response = self.client.get(self.cl.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_conservationlist_string(self):
        """Test string."""
        pass


class ConservationCategoryViewTests(TestCase):
    """ConservationCategory unit tests."""

    def setUp(self):
        """Set up."""
        pass

    def test_absolute_admin_url(self):
        """Test absolute_admin_url loads."""
        pass


class ConservationCriterionViewTests(TestCase):
    """ConservationCriterion unit tests."""

    def setUp(self):
        """Set up."""
        pass

    def test_absolute_admin_url(self):
        """Test absolute_admin_url loads."""
        pass


class TaxonConservationListingViewTests(TestCase):
    """TaxonConservationListing view tests."""

    def setUp(self):
        """Set up."""
        self.taxon, created = Taxon.objects.update_or_create(
            name_id=0,
            defaults=dict(name="Eukarya",
                          rank=Taxon.RANK_DOMAIN,
                          current=True,
                          parent=None))

        self.gaz = cons_models.TaxonConservationListing.objects.create(
            taxon=self.taxon,
            scope=cons_models.TaxonConservationListing.SCOPE_WESTERN_AUSTRALIA,
        )
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_list_url_loads(self):
        """Test conservationactivity-list."""
        response = self.client.get(self.gaz.list_url())
        self.assertEqual(response.status_code, 200)

    def test_absolute_admin_url(self):
        """Test absolute_admin_url loads."""
        response = self.client.get(self.gaz.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_absolute_admin_add_url(self):
        """Test absolute_admin_add_url loads."""
        response = self.client.get(self.gaz.absolute_admin_add_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        """Test TaxonConservationListing create view."""
        url = reverse("conservation:taxonconservationlisting-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CommunityConservationListingViewTests(TestCase):
    """CommunityConservationListing view tests."""

    def setUp(self):
        """Set up."""
        self.taxon, created = Taxon.objects.update_or_create(
            name_id=0,
            defaults=dict(name="Eukarya",
                          rank=Taxon.RANK_DOMAIN,
                          current=True,
                          parent=None))
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()
        self.gaz = cons_models.CommunityConservationListing.objects.create(
            community=self.com0,
            scope=cons_models.CommunityConservationListing.SCOPE_WESTERN_AUSTRALIA,
        )
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()
        self.client.force_login(self.user)

    def test_list_url_loads(self):
        """Test conservationactivity-list."""
        response = self.client.get(self.gaz.list_url())
        self.assertEqual(response.status_code, 200)

    def test_absolute_admin_url(self):
        """Test absolute_admin_url loads."""
        response = self.client.get(self.gaz.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_absolute_admin_add_url(self):
        """Test absolute_admin_add_url loads."""
        response = self.client.get(self.gaz.absolute_admin_add_url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        """Test CommunityConservationListing create view."""
        url = reverse("conservation:communityconservationlisting-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_community_detail_url_loads(self):
        """Test Community detail_url."""
        response = self.client.get(self.com0.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conservation/cards/conservationlisting.html')


class DocumentViewTests(TestCase):
    """View tests for Document."""

    def setUp(self):
        """Set up."""
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.user.save()

        self.taxon0 = mommy.make(
            Taxon,
            name_id=1000,
            name="name0",
            _fill_optional=['rank', 'eoo'])
        self.taxon0.save()
        self.com0 = mommy.make(
            Community,
            code="code0",
            name="name0",
            _fill_optional=['eoo'])
        self.com0.save()
        self.object = cons_models.Document.objects.create(
            title="test doc",
            document_type=cons_models.Document.TYPE_RECOVERY_PLAN,
            # attachment=self.fatt1
            # TODO add dates

            effective_from=timezone.now(),
            effective_to=timezone.now() + relativedelta(months=+6),
            effective_from_commonwealth=timezone.now(),
            effective_to_commonwealth=timezone.now() + relativedelta(months=+6),
            review_due=timezone.now() + relativedelta(months=+6),
            last_reviewed_on=timezone.now() + relativedelta(days=-10),
        )
        self.consthreatcat = cons_models.ConservationThreatCategory.objects.create(
            code="weeds",
            label="Weeds",
            description="invasive weeds"
        )
        self.threat = cons_models.ConservationThreat.objects.create(
            category=self.consthreatcat,
            cause="burn some stuff",
            document=self.object
        )
        self.object.taxa.add(self.taxon0)
        self.object.communities.add(self.com0)

        # TODO add attachment
        # self.fatt1 = cons_models.FileAttachment.objects.create(
        #     attachment=SimpleUploadedFile('testfile.txt', b'These are the file contents.'),
        #     title="test",
        #     author=self.user,
        #     confidential=True,
        #     current=True
        # )
        # self.fatt1.save()
        # Error: fatt1 has no content_type

        # TODO add actions

        self.client.force_login(self.user)

    def test_absolute_admin_url(self):
        """Test Document absolute admin url."""
        response = self.client.get(self.object.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url(self):
        """Test ConservationAction get absolute url."""
        response = self.client.get(self.object.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_community_detail_url_loads(self):
        """Test Community detail_url."""
        response = self.client.get(self.com0.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conservation/cards/document.html')

    def test_list_url_loads(self):
        """Test conservationaction-list."""
        response = self.client.get(self.object.list_url())
        self.assertEqual(response.status_code, 200)

        # test filter by one and many admin_areas

    def test_create_url_loads(self):
        """Test conservationaction-create."""
        response = self.client.get(self.object.create_url())
        self.assertEqual(response.status_code, 200)

    def test_update_url_loads(self):
        """Test conservationaction-update."""
        response = self.client.get(self.object.update_url)
        self.assertEqual(response.status_code, 200)


class ConservationFixtureTests(TestCase):
    """View tests for Conservation models with test data from fixtures."""

    fixtures = [
        "taxonomy/fixtures/test_groups.json",
        "taxonomy/fixtures/test_users.json",
        "taxonomy/fixtures/test_supra.json",
        "taxonomy/fixtures/test_conservationlist.json",
        "taxonomy/fixtures/test_communities.json",
        "taxonomy/fixtures/test_conservationthreat.json",
        "taxonomy/fixtures/test_conservationaction.json",
        "taxonomy/fixtures/test_conservationactivity.json",
        "taxonomy/fixtures/test_document.json",
        "taxonomy/fixtures/test_woylie.json",
    ]

    def test_get_absolute_url_taxon(self):
        """Test Taxon with ConservationThreats and Conservation listings get absolute url loads."""
        t = cons_models.ConservationThreat.objects.last().taxa.first()
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        t = cons_models.TaxonConservationListing.objects.last().taxon
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        u = get_user_model().objects.filter(is_superuser=True).first()
        self.client.force_login(u)
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        # TODO verify that staff can see the conservation listing absolute admin url

    def test_list_url_taxon(self):
        """Test Taxon list url with filter settings."""
        t = cons_models.Document.objects.last().taxa.first()
        response = self.client.get(t.list_url() + "?name_id={0}".format(t.name_id))
        self.assertEqual(response.status_code, 200)
        # TODO assert document title in response
        # TODO assert document include template used

        t = cons_models.TaxonConservationListing.objects.last().taxon
        response = self.client.get(t.list_url() + "?name_id={0}".format(t.name_id))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        a, created = Area.objects.get_or_create(
            name="WA",
            geom='{"type": "Polygon", "coordinates": [[[110, -38], [110,-15],[125,-15],[125,-38],[110, -38]]]}')
        response = self.client.get(t.list_url() + "?admin_areas={0}".format(a.pk))
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url_threat(self):
        """Test ConservationThreat get absolute url loads."""
        t = cons_models.ConservationThreat.objects.last()
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url_action(self):
        """Test ConservationAction get absolute url loads."""
        t = cons_models.ConservationAction.objects.last()
        response = self.client.get(t.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_admin_list_threat(self):
        """Test admin change list for ConservationThreat."""
        url = reverse("admin:conservation_conservationthreat_changelist")
        u = get_user_model().objects.filter(is_superuser=True).first()
        self.client.force_login(u)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_list_action(self):
        """Test admin change list for ConservationAction."""
        url = reverse("admin:conservation_conservationaction_changelist")
        u = get_user_model().objects.filter(is_superuser=True).first()
        self.client.force_login(u)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_loads_threat(self):
        """Test conservationthreat-list loads."""
        url = cons_models.ConservationThreat.objects.last().list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_conservationactivity_list_url_loads_action(self):
        """Test conservationaction-list loads."""
        url = cons_models.ConservationActivity.objects.last().conservation_action.list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        a, created = Area.objects.get_or_create(
            name="WA",
            geom='{"type": "Polygon", "coordinates": [[[110, -38], [110,-15],[125,-15],[125,-38],[110, -38]]]}')
        response = self.client.get(url + "?admin_areas={0}".format(a.pk))
        self.assertEqual(response.status_code, 200)

    def test_absolute_admin_url_document(self):
        """Test Document absolute admin url."""
        url = cons_models.Document.objects.last().absolute_admin_url
        u = get_user_model().objects.filter(is_superuser=True).first()
        self.client.force_login(u)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url_document(self):
        """Test Document and Taxon with Document get absolute url."""
        url = cons_models.Document.objects.last().get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = cons_models.Document.objects.last().taxa.first().get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_url_loads_document(self):
        """Test conservationaction-list."""
        url = cons_models.Document.objects.last().list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
