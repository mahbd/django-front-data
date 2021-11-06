import json

from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client

from front_data.models import FrontData, FAQ, Configuration
from front_data.serializers import FrontDataSerializer, FullFrontDataSerializer, StdFrontDataSerializer, FAQSerializer, \
    ConfigurationSerializer

c = Client()
try:
    import rest_framework


    class SiteDataTest(TestCase):
        def setUp(self) -> None:
            self.admin = User.objects.create_superuser('super', password='1234')
            self.staff1 = User.objects.create_user('staff', password='1234', is_staff=True)
            self.staff2 = User.objects.create_user('staff2', password='1234', is_staff=True)
            self.user = User.objects.create_user('user', password='1234')
            self.staff1.user_permissions.add(Permission.objects.get(codename='add_frontdata'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='change_frontdata'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='delete_frontdata'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='view_frontdata'))
            self.api = '/api/front-data/'
            self.api_std = '/api/front-data-std/'
            self.api_full = '/api/front-data-full/'

            c.force_login(self.admin)
            c.post(self.api_full, {
                "name": "test_about",
                "data": json.dumps([{"link": "fds"}, {"text": "fde"}])
            })
            c.logout()

        def test_create_site_data_superuser(self):
            c.force_login(self.admin)
            data = {
                "name": "test_nav",
                "data": json.dumps([{"link": "fds"}, {"text": "fde"}]),
                "templates": json.dumps([])
            }
            res = c.post(self.api_full, data)
            self.assertEqual(res.status_code, 201, f'Admin must be able to create site data\n{res.content}')
            res = res.json()
            self.assertEqual(res['data'], json.loads(data['data']), 'data must be equal')
            self.assertEqual(res['name'], data['name'], 'name must be equal')
            self.assertEqual(res['user'], self.admin.id, 'user must be equal')
            self.assertEqual(res['templates'], [], 'templates must be equal')

        def test_create_site_data_permitted_staff(self):
            c.force_login(self.staff1)
            data = {
                "name": "test_nav",
                "data": json.dumps([{"link": "fds"}, {"text": "fde"}])
            }
            res = c.post(self.api, data)
            self.assertEqual(res.status_code, 201, f'Admin must be able to create site data\n{res.content}')
            res = res.json()
            self.assertEqual(res['data'], json.loads(data['data']), 'data must be equal')
            self.assertEqual(res['name'], data['name'], 'name must be equal')

        def test_create_site_data_non_permitted_staff(self):
            c.force_login(self.staff2)
            data = {
                "name": "test_nav",
                "data": json.dumps([{"link": "fds"}, {"text": "fde"}])
            }
            res = c.post(self.api, data)
            self.assertEqual(res.status_code, 403, f'Non permitted staff must not be able to create site data')

        def test_create_site_data_regular_user(self):
            c.force_login(self.user)
            data = {
                "name": "test_nav",
                "data": json.dumps([{"link": "fds"}, {"text": "fde"}])
            }
            res = c.post(self.api, data)
            self.assertEqual(res.status_code, 403, f'User must not be able to create site data')

        def test_get_site_data_ann(self):
            c.logout()
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200, 'Everybody should be able to read')
            res = res.json()
            self.assertEqual(len(res), FrontData.objects.all().count(), 'All site data should be returned')
            self.assertDictEqual(res[0], FrontDataSerializer(FrontData.objects.all().first()).data,
                                 'Correct site data should be returned')

        def test_get_site_data_user(self):
            c.force_login(self.user)
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200, 'Everybody should be able to read')
            res = res.json()
            self.assertEqual(len(res), FrontData.objects.all().count(), 'All site data should be returned')
            self.assertDictEqual(res[0], FrontDataSerializer(FrontData.objects.all().first()).data,
                                 'Correct site data should be returned')

        def test_get_site_data_permitted_staff(self):
            c.force_login(self.staff1)
            res = c.get(self.api_std)
            self.assertEqual(res.status_code, 200, 'Everybody should be able to read')
            res = res.json()
            self.assertCountEqual(res, StdFrontDataSerializer(FrontData.objects.all(), many=True).data,
                                  'Correct site data should be returned')

        def test_get_site_data_permitted_admin(self):
            c.force_login(self.admin)
            res = c.get(self.api_full)
            self.assertEqual(res.status_code, 200, 'Everybody should be able to read')
            res = res.json()
            self.assertCountEqual(res, FullFrontDataSerializer(FrontData.objects.all(), many=True).data,
                                  'Correct site data should be returned')


    class FAQTestCase(TestCase):
        def setUp(self) -> None:
            self.admin = User.objects.create_superuser('super', password='1234')
            self.staff1 = User.objects.create_user('staff', password='1234', is_staff=True)
            self.staff2 = User.objects.create_user('staff2', password='1234', is_staff=True)
            self.user = User.objects.create_user('user', password='1234')
            self.staff1.user_permissions.add(Permission.objects.get(codename='add_faq'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='change_faq'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='delete_faq'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='view_faq'))
            self.api = '/api/faqs/'

            c.force_login(self.admin)
            c.post(self.api, {
                "question": "test_about",
                "answer": 'hello world'
            })
            c.logout()

        def test_create_faq_admin(self):
            c.force_login(self.admin)
            data = {'question': 'hello', 'answer': 'nice to meet'}
            res = c.post(self.api, {'question': 'hello', 'answer': 'nice to meet'})
            self.assertEqual(res.status_code, 201)
            res = res.json()
            data = res | data
            self.assertDictEqual(data, res)

        def test_create_faq_staff(self):
            c.force_login(self.staff1)
            res = c.post(self.api, {'question': 'hello', 'answer': 'nice to meet'})
            self.assertEqual(res.status_code, 201)

        def test_create_faq_non_permitted_staff(self):
            c.force_login(self.staff2)
            res = c.post(self.api, {'question': 'hello', 'answer': 'nice to meet'})
            self.assertEqual(res.status_code, 403)

        def test_create_faq_user(self):
            c.force_login(self.user)
            res = c.post(self.api, {'question': 'hello', 'answer': 'nice to meet'})
            self.assertEqual(res.status_code, 403)

        def test_get_faq_user(self):
            c.force_login(self.user)
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200)
            res = res.json()
            self.assertCountEqual(res, FAQSerializer(FAQ.objects.all(), many=True).data)

        def test_get_faq_ann(self):
            c.logout()
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200)
            res = res.json()
            self.assertCountEqual(res, FAQSerializer(FAQ.objects.all(), many=True).data)


    class ConfigurationTestCase(TestCase):
        def setUp(self) -> None:
            self.admin = User.objects.create_superuser('super', password='1234')
            self.staff1 = User.objects.create_user('staff', password='1234', is_staff=True)
            self.staff2 = User.objects.create_user('staff2', password='1234', is_staff=True)
            self.user = User.objects.create_user('user', password='1234')
            self.staff1.user_permissions.add(Permission.objects.get(codename='add_configuration'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='change_configuration'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='delete_configuration'))
            self.staff1.user_permissions.add(Permission.objects.get(codename='view_configuration'))
            self.api = '/api/configurations/'

            c.force_login(self.admin)
            c.post(self.api, {
                "key": "test_about",
                "value": 'hello world'
            })
            c.logout()

        def test_create_configuration_admin(self):
            c.force_login(self.admin)
            res = c.post(self.api, {'key': 'hello', 'value': 'nice to meet'})
            self.assertEqual(res.status_code, 201)
            data = res.json()
            self.assertEqual(data['key'], 'hello')
            self.assertEqual(data['value'], 'nice to meet')

        def test_create_configuration_staff(self):
            c.force_login(self.staff1)
            res = c.post(self.api, {'key': 'hello', 'value': 'nice to meet'})
            self.assertEqual(res.status_code, 201)

        def test_create_configuration_non_permitted_staff(self):
            c.force_login(self.staff2)
            res = c.post(self.api, {'key': 'hello', 'value': 'nice to meet'})
            self.assertEqual(res.status_code, 403)

        def test_create_configuration_user(self):
            c.force_login(self.user)
            res = c.post(self.api, {'key': 'hello', 'value': 'nice to meet'})
            self.assertEqual(res.status_code, 403)

        def test_get_configuration_user(self):
            c.force_login(self.user)
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200)
            res = res.json()
            self.assertCountEqual(res, ConfigurationSerializer(Configuration.objects.all(), many=True).data)

        def test_get_configuration_ann(self):
            c.logout()
            res = c.get(self.api)
            self.assertEqual(res.status_code, 200)
            res = res.json()
            self.assertCountEqual(res, ConfigurationSerializer(Configuration.objects.all(), many=True).data)

        def test_update_configuration_admin(self):
            c.force_login(self.admin)
            res = c.patch(self.api + 'test_about/', {'value': 'hello world 2'}, content_type='application/json')
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data['value'], 'hello world 2')

        def test_update_configuration_staff(self):
            c.force_login(self.staff1)
            res = c.patch(self.api + 'test_about/', {'value': 'hello world 2'}, content_type='application/json')
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data['value'], 'hello world 2')

        def test_update_configuration_non_permitted_staff(self):
            c.force_login(self.staff2)
            res = c.patch(self.api + 'test_about/', {'value': 'hello world 2'})
            self.assertEqual(res.status_code, 403)

        def test_update_configuration_user(self):
            c.force_login(self.user)
            res = c.patch(self.api + 'test_about/', {'value': 'hello world 2'})
            self.assertEqual(res.status_code, 403)

        def test_delete_configuration_admin(self):
            c.force_login(self.admin)
            res = c.delete(self.api + 'test_about/')
            self.assertEqual(res.status_code, 204)

        def test_delete_configuration_staff(self):
            c.force_login(self.staff1)
            res = c.delete(self.api + 'test_about/')
            self.assertEqual(res.status_code, 204)

        def test_delete_configuration_non_permitted_staff(self):
            c.force_login(self.staff2)
            res = c.delete(self.api + 'test_about/')
            self.assertEqual(res.status_code, 403)

        def test_delete_configuration_user(self):
            c.force_login(self.user)
            res = c.delete(self.api + 'test_about/')
            self.assertEqual(res.status_code, 403)


except ModuleNotFoundError:
    pass
