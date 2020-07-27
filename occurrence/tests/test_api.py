from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Polygon, Point
from django.urls import reverse
from io import BytesIO
import json
# from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
# from unittest import skip
import uuid

from occurrence.models import (
    AreaEncounter, ObservationGroup, HabitatComposition, CountMethod, CountAccuracy,
    EncounterType, SecondarySigns, SampleType, TaxonAreaEncounter, Landform, RockType,
    SoilType,
)
from taxonomy.models import Community, Taxon

User = get_user_model()


class AreaEncounterSerializerTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'testuser@test.com', 'pass')
        self.user.is_staff = True
        self.user.is_superuser = True  # TODO: test user/group permissions properly
        self.user.save()
        self.client.login(username='testuser', password='pass')
        # token = Token.objects.get(user__username='testuser')
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.ae = AreaEncounter.objects.create(
            source_id=uuid.uuid4(),
            description='Test polygon AreaEncounter',
            geom=Polygon(((115.0, -32.0), (115.0, -33.0), (116.0, -33.0), (116.0, -32.0), (115.0, -32.0)))
        )
        self.ae_point = AreaEncounter.objects.create(
            source_id=uuid.uuid4(),
            description='Test point AreaEncounter',
            point=Point((115.0, -32.0))
        )
        self.og = ObservationGroup.objects.create(encounter=self.ae)
        self.hc = HabitatComposition.objects.create(encounter=self.ae)
        self.taxon = Taxon.objects.create(name_id=0, name='Test taxon')
        self.taxon_ae = TaxonAreaEncounter.objects.create(
            source_id=uuid.uuid4(),
            description='Test taxon area encounter',
            geom=self.ae.geom,
            taxon=self.taxon
        )
        self.enc_type = EncounterType.objects.create(code='enctype', label='Encounter type')

    def test_occ_areas_get(self):
        for i in [
            'occurrence_area_polys', 'occurrence_area_points', 'occurrence_taxonarea_polys',
            'occurrence_taxonarea_points', 'occurrence_communityarea_polys', 'occurrence_communityarea_points',
        ]:
            url = reverse('api:{}-list'.format(i))
            resp = self.client.get(url, {'format': 'json'})
            self.assertEqual(resp.status_code, 200)

    def test_occ_areas_post(self):
        url = reverse('api:occurrence_area_polys-list') + '?format=json'
        resp = self.client.post(
            url,
            {
                'source': 0,
                'source_id': str(uuid.uuid4()),
                'code': 'code',
                'label': 'Label',
                'name': 'Name',
                'geom': 'POLYGON ((115 -32, 115 -33, 116 -33, 116 -32, 115 -32))',
            },
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        url = reverse('api:occurrence_area_polys-detail', kwargs={'pk': data['id']})
        # Also check the detail view for the new object.
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['geometry']['type'], 'Polygon')

    def test_occ_points_post(self):
        url = reverse('api:occurrence_area_points-list')
        resp = self.client.post(
            url,
            {
                'source': 0,
                'source_id': str(uuid.uuid4()),
                'code': 'code',
                'label': 'Label',
                'name': 'Name',
                'point': 'POINT (115 -32)',
            },
        )
        self.assertEqual(resp.status_code, 201)

    def test_occ_taxonareas_post(self):
        url = reverse('api:occurrence_taxonarea_polys-list') + '?format=json'
        # Test the validation of required request params.
        # This dict is missing taxon, encountered_by and encounter_type.
        taxon_data = {
            'source': 0,
            'source_id': str(uuid.uuid4()),
            'code': 'code',
            'label': 'Label',
            'name': 'Name',
            'geom': 'POLYGON ((115 -32, 115 -33, 116 -33, 116 -32, 115 -32))',
        }
        resp = self.client.post(url, taxon_data)
        # POST will fail.
        self.assertEqual(resp.status_code, 400)
        # Update the dict with required data and re-try.
        taxon_data['taxon'] = self.taxon.name_id
        taxon_data['encountered_by'] = self.user.pk
        taxon_data['encounter_type'] = self.enc_type.pk
        # POST will now succeed.
        resp = self.client.post(url, taxon_data)
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        url = reverse('api:occurrence_taxonarea_polys-detail', kwargs={'pk': data['id']})
        # Also check the detail view for the new object.
        resp = self.client.get(url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(data['geometry']['type'], 'Polygon')

    def test_occ_taxonpoints_post(self):
        url = reverse('api:occurrence_taxonarea_points-list')
        resp = self.client.post(
            url,
            {
                'source': 0,
                'source_id': str(uuid.uuid4()),
                'code': 'code',
                'label': 'Label',
                'name': 'Name',
                'taxon': self.taxon.name_id,
                'encountered_by': self.user.pk,
                'encounter_type': self.enc_type.pk,
                'point': 'POINT (115 -32)',
            },
        )
        self.assertEqual(resp.status_code, 201)

    def test_occ_communityareas_post(self):
        Community.objects.create(code='comm1', name='Test community')
        url = reverse('api:occurrence_communityarea_polys-list')
        resp = self.client.post(
            url,
            {
                'source': 0,
                'source_id': str(uuid.uuid4()),
                'code': 'code',
                'label': 'Label',
                'name': 'Name',
                'community': 'comm1',
                'encountered_by': self.user.pk,
                'encounter_type': self.enc_type.pk,
                'geom': 'POLYGON ((115 -32, 115 -33, 116 -33, 116 -32, 115 -32))',
            },
        )
        self.assertEqual(resp.status_code, 201)

    def test_occ_communitypoints_post(self):
        Community.objects.create(code='comm1', name='Test community')
        url = reverse('api:occurrence_communityarea_points-list')
        resp = self.client.post(
            url,
            {
                'source': 0,
                'source_id': str(uuid.uuid4()),
                'code': 'code',
                'label': 'Label',
                'name': 'Name',
                'community': 'comm1',
                'encountered_by': self.user.pk,
                'encounter_type': self.enc_type.pk,
                'point': 'POINT (115 -32)',
            },
        )
        self.assertEqual(resp.status_code, 201)


class ObservationGroupSerializerTests(AreaEncounterSerializerTests):

    def setUp(self):
        super(ObservationGroupSerializerTests, self).setUp()
        self.url = reverse('api:occurrence_observation_group-list')

    def test_occ_observation_get(self):
        """Test the occurrence_observation_group API endpoint, unfiltered
        """
        resp = self.client.get(self.url, {'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        # Response should return two objects.
        self.assertEqual(data['count'], 2)

    def test_occ_observation_get_filtered(self):
        """Test the occurrence_observation_group API endpoint, filtered
        """
        resp = self.client.get(self.url, {'format': 'json', 'obstype': 'HabitatComposition'})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        # Response should return one HabitatComposition object (no ObservationGroup objects).
        self.assertEqual(data['count'], 1)
        self.assertFalse('ObservationGroup' in [i['obstype'] for i in data['results']])

    def test_occ_observation_post(self):
        """Test the occurrent_observation_group POST endpoint handles lookups and null fields
        """
        SampleType.objects.create(code='frozen-carcass', label='Frozen carcass')
        resp = self.client.post(
            self.url,
            {
                'obstype': 'PhysicalSample',
                'source': self.ae.source,
                'source_id': self.ae.source_id,
                'sample_type': 'frozen-carcass',
                'sample_label': '[WA Museum]abc123',
                'sample_destination': None,
                'permit_type': None,
            }
        )
        self.assertEqual(resp.status_code, 201)
        # Also test invalid source & source_id.
        resp = self.client.post(
            self.url,
            {
                'obstype': 'PhysicalSample',
                'source': self.ae.source,
                'source_id': 'invalid',
                'sample_type': 'frozen-carcass',
                'sample_label': '[WA Museum]abc123',
                'sample_destination': None,
                'permit_type': None,
            }
        )
        self.assertEqual(resp.status_code, 400)

    def test_occ_observation_obstype_post(self):
        """Test the occurrence_observation_group API POST endpoint for object types not requiring special cases
        """
        models = [
            'HabitatComposition', 'HabitatCondition', 'AreaAssessment', 'FireHistory', 'VegetationClassification']
        for model in models:
            resp = self.client.post(
                self.url,
                {
                    'obstype': model,
                    'source': self.ae.source,
                    'source_id': self.ae.source_id,
                }
            )
            self.assertEqual(resp.status_code, 201)

    def test_occ_observation_post_plantcount(self):
        """Test the PlantCount POST endpoint behaves correctly
        """
        resp = self.client.get(self.url, {'format': 'json', 'obstype': 'PlantCount'})
        data = json.loads(resp.content)
        self.assertEqual(data['count'], 0)
        # The PlantCount API endpoint requires count_method and count_accuracy as valid slug values.
        count_method = CountMethod.objects.create(code='estimate', label='Estimate')
        count_accuracy = CountAccuracy.objects.create(code='estimate', label='Estimate')
        resp = self.client.post(self.url, {
            'obstype': 'PlantCount',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
            'count_method': count_method.code,
            'count_accuracy': count_accuracy.code,
        })
        self.assertEqual(resp.status_code, 201)
        # Confirm that a PlantCount object was created.
        resp = self.client.get(self.url, {'format': 'json', 'obstype': 'PlantCount'})
        data = json.loads(resp.content)
        self.assertEqual(data['count'], 1)

    def test_occ_observation_post_animalobservation(self):
        """Test the AnimalObservation POST endpoint behaves correctly
        """
        # If secondary_signs values are passed into the endpoint, they need to be parseable as valid slugs.
        SecondarySigns.objects.create(code='fur', label='Fur')
        resp = self.client.post(self.url, data={
            'obstype': 'AnimalObservation',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
            'secondary_signs': ['fur'],
        })
        self.assertEqual(resp.status_code, 201)
        SecondarySigns.objects.create(code='eggs', label='Eggs')
        # Parse >1 secondary_signs value.
        resp = self.client.post(self.url, data={
            'obstype': 'AnimalObservation',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
            'secondary_signs': ['fur', 'eggs'],
        })
        self.assertEqual(resp.status_code, 201)
        # Confirm that secondary_signs is optional.
        resp = self.client.post(self.url, {
            'obstype': 'AnimalObservation',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
        })
        self.assertEqual(resp.status_code, 201)

    def test_occ_observation_post_animalobservation_secondarysigns(self):
        """Test the AnimalObservation POST endpoint tolerates strings for secondary signs."""
        SecondarySigns.objects.create(code='fur', label='Fur')
        SecondarySigns.objects.create(code='eggs', label='Eggs')

        # AnimalEncounter.secondary_signs stress test with a list as string
        resp = self.client.post(self.url, data={
            'obstype': 'AnimalObservation',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
            'secondary_signs': ['fur', 'eggs'],
        })
        self.assertEqual(resp.status_code, 201)

        # AnimalEncounter.secondary_signs stress test with a single string
        resp = self.client.post(self.url, data={
            'obstype': 'AnimalObservation',
            'source': self.ae.source,
            'source_id': self.ae.source_id,
            'secondary_signs': ['fur'],
        })
        self.assertEqual(resp.status_code, 201)


    def test_occ_observation_post_fileattachment(self):
        """Test the FileAttachment POST endpoint behaves correctly
        """
        testfile = BytesIO(b'some test binary data')
        testfile.name = 'test.txt'
        resp = self.client.post(
            self.url,
            {
                'obstype': 'FileAttachment',
                'source': self.ae.source,
                'source_id': self.ae.source_id,
                'attachment': testfile,
            },
            format='multipart',
        )
        self.assertEqual(resp.status_code, 201)

    def test_bulk_create(self):
        url = reverse('api:occurrence_observation_group-bulk-create')

        # PhysicalSample object type.
        resp = self.client.post(
            url + '?format=json&obstype=PhysicalSample',
            data=[
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'sample_label': 'foo'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'sample_label': 'bar'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'sample_label': 'baz'}
            ]
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data['created_count'], 3)

        # AnimalObservation.
        SecondarySigns.objects.create(code='tracks', label='Tracks')
        resp = self.client.post(
            url + '?format=json&obstype=AnimalObservation',
            data=[
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'no_adult_female': 1, 'secondary_signs': ['tracks']},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'no_adult_male': 2, 'secondary_signs': ['tracks']},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'no_adult_unknown': 3, 'secondary_signs': ['tracks']}
            ]
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data['created_count'], 3)

        # VegetationClassification.
        Landform.objects.create(code='cave', label='Cave')
        Landform.objects.create(code='plain', label='Plain')
        Landform.objects.create(code='depression', label='Depression')
        resp = self.client.post(
            url + '?format=json&obstype=VegetationClassification',
            data=[
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'landform': 'cave'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'landform': 'plain'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'landform': 'depression'}
            ]
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data['created_count'], 3)

        # HabitatComposition.
        RockType.objects.create(code='banded-iron', label='Banded Iron')
        SoilType.objects.create(code='clay', label='Clay')
        resp = self.client.post(
            url + '?format=json&obstype=HabitatComposition',
            data=[
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'landform': 'cave'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'rock_type': 'banded-iron'},
                {'source': self.ae.source, 'source_id': str(self.ae.source_id), 'soil_type': 'clay'}
            ]
        )
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.content)
        self.assertEqual(data['created_count'], 3)
