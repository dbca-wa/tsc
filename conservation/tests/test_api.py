from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase
import json
from rest_framework.test import APIClient
import uuid

from taxonomy.models import Community, Taxon
from conservation.models import (
    FileAttachment,
    ConservationList,
    ConservationCategory,
    CommunityConservationListing,
    ConservationCriterion,
    Document,
    TaxonConservationListing,
)

# Test updating taxon-conservationlisting with none, one, many cat and crit
# Test updating community-conservationlisting


User = get_user_model()


class ObservationGroupSerializerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # TODO: test user/group permissions properly
        self.user = User.objects.create_superuser('testuser', 'testuser@test.com', 'pass')
        self.client.login(username='testuser', password='pass')
        self.community = Community.objects.create(code='Test community')
        self.taxon = Taxon.objects.create(name_id=0, name='Test taxon')
        self.clist = ConservationList.objects.create(code='test-list', label='Test conservation list')
        self.ccategory = ConservationCategory.objects.create(
            conservation_list=self.clist, code='test-category', label='Test conservation category')
        self.ccriterion = ConservationCriterion.objects.create(
            conservation_list=self.clist, code='test-criterion')
        self.taxon_listing = TaxonConservationListing.objects.create(taxon=self.taxon)
        self.document = Document.objects.create(title='Test document')
        f = SimpleUploadedFile('file.txt', b'file_content')
        self.fileattachment = FileAttachment.objects.create(
            attachment=f,
            content_type=ContentType.objects.get_for_model(Document),
            object_id=self.document.pk
        )
        self.ccl = CommunityConservationListing.objects.create(community=self.community)

    def test_get_list_endpoints(self):
        for i in [
            'conservationlist',
            'conservationcategory',
            'conservationcriterion',
            'taxonconservationlisting',
            'communityconservationlisting',
        ]:
            url = reverse('api:{}-list'.format(i))
            resp = self.client.get(url, {'format': 'json'})
            self.assertEqual(resp.status_code, 200)

    def test_get_detail_endpoints(self):
        url = reverse('api:conservationlist-detail', kwargs={'pk': self.clist.pk})
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        url = reverse('api:conservationcategory-detail', kwargs={'pk': self.ccategory.pk})
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        url = reverse('api:conservationcriterion-detail', kwargs={'pk': self.ccriterion.pk})
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        url = reverse('api:taxonconservationlisting-detail', kwargs={'pk': self.taxon_listing.pk})
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        url = reverse('api:communityconservationlisting-detail', kwargs={'pk': self.ccl.pk})
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)

    def test_post_taxonconservationlisting(self):
        """Test the TaxonConservationListing POST endpoint behaves correctly
        """
        url = reverse('api:taxonconservationlisting-list')
        data = {
            'source': 0,
            'source_id': uuid.uuid4(),
            'taxon': self.taxon.name_id,
            'comments': 'Test comment',
            'category': [self.ccategory.pk],
            'criteria': [self.ccriterion.pk]
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        # Category or criteria can also be a single PK.
        data['source_id'] = uuid.uuid4()
        data['category'] = self.ccategory.pk
        data['criteria'] = self.ccriterion.pk
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        # Test with no categories or criteria.
        data['source_id'] = uuid.uuid4()
        data.pop('category')
        data.pop('criteria')
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)

    def test_post_communityconservationlisting(self):
        """Test the CommunityConservationListing POST endpoint behaves correctly
        """
        url = reverse('api:communityconservationlisting-list')
        data = {
            'source': 0,
            'source_id': uuid.uuid4(),
            'community': self.community.code,
            'comments': 'Test comment',
            'category': [self.ccategory.pk],
            'criteria': [self.ccriterion.pk]
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        # Category or criteria can also be a single PK.
        data['source_id'] = uuid.uuid4()
        data['category'] = self.ccategory.pk
        data['criteria'] = self.ccriterion.pk
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
        # Test with no categories or criteria.
        data['source_id'] = uuid.uuid4()
        data.pop('category')
        data.pop('criteria')
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 201)
