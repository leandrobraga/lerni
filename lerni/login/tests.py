# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User
from lerni.core.models import Teacher


class LoginTest(TestCase):

    def setUp(self):

        user_admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        user_admin.save()

        user_teacher = User.objects.create_user('teacher', 'teacher@gmail.com', 'teacher')
        user_teacher.save()
        teacher = Teacher(user=user_teacher)
        teacher.save()

    def test_get(self):

        pass

    def test_post(self):

        data = dict(username='', password='')
        resp = self.client.post('/login/', data)
        self.assertEqual(200, resp.status_code)
        #self.assertTemplateUsed(resp, 'core/administrator.html')

    def test_login_administrator(self):

        data = dict(username='admin', password='admin')
        resp = self.client.post('/login/', data)
        self.assertRedirects(resp, '/administrator/')

    def test_login_teacher(self):

        data = dict(username='teacher', password='teacher')
        resp = self.client.post('/login/', data)
        #self.assertContains(self.client.session,'administrator')
        self.assertTemplateUsed(resp, 'core/teacher.html')


