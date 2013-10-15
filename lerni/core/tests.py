# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from lerni.core.models import Teacher
from lerni.core.forms import TeacherAddForm


class TestCoreIndex(TestCase):

    def setUp(self):

        self.resp = self.client.get('/')

    def test_get(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template(self):

        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_html(self):

        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 3)
        self.assertContains(self.resp, 'type="text"', 1)
        self.assertContains(self.resp, 'type="password"', 1)
        self.assertContains(self.resp, 'type="submit"')


class AdministratorScreenTest(TestCase):

    def setUp(self):

        user_admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        user_admin.save()
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get('/administrator/')

    def test_template_administrator(self):

        self.assertTemplateUsed(self.resp, "core/administrator.html")

    def test_administrator_html(self):

        self.assertContains(self.resp, '<a class="ajax-link" href="/chooseUser/"')
        self.assertContains(self.resp, '<i class="icon-user"')


class ChooseUserScreenWithAdministratorTest(TestCase):

    def setUp(self):

        user_admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        user_admin.save()
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get('/chooseUser/')

    def test_get_choose_user(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template_choose_user(self):

        self.assertTemplateUsed(self.resp, "core/chooseUser.html")

    def test_html(self):

        self.assertContains(self.resp, '<a data-rel="tooltip" title="" class="well span3 top-block"', 2)
        self.assertContains(self.resp, '<a data-rel="tooltip" title="" class="well span3 top-block" href="/managerTeacher/"')
        self.assertContains(self.resp, '<a data-rel="tooltip" title="" class="well span3 top-block" href="/managerStudent/"')


class ManagerTeacherWithAdministratorTest(TestCase):

    def setUp(self):

        user_admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        user_admin.save()
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get('/managerTeacher/')

    def test_get_manager_teacher(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template_manager_teacher(self):

        self.assertTemplateUsed(self.resp, "core/managerTeacher.html")


class AddTeacherWithAdministratorTest(TestCase):

    def setUp(self):

        user_admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        user_admin.save()
        self.client.login(username='admin', password='admin')
        self.resp = self.client.get('/managerTeacher/add/')

    def test_get_add_teacher(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template_add_teacher(self):

        self.assertTemplateUsed(self.resp, "core/addTeacher.html")

    def test_has_form(self):

        form = self.resp.context['form']
        self.assertIsInstance(form, TeacherAddForm)

    def test_form_has_field(self):

        form = self.resp.context['form']
        self.assertItemsEqual(['username', 'first_name', 'last_name', 'email', 'password', 'check_password'], form.fields)


class AddTeacherWithAdministratorUsingPostTest(TestCase):

    def setUp(self):

        data = {'username': 'ellen', 'first_name': 'Ellen', 'last_name': 'Quirino', 'email': 'elen@gmail.com',
        'password': '123456', 'check_password': '123456'}

        self.resp = self.client.post('/managerTeacher/add/', data)

    def test_post_add_teacher(self):

        self.assertEqual(200, self.resp.status_code)

    def test_save(self):

        self.assertTrue(Teacher.objects.exists())

