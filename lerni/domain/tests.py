# coding: utf-8

from django.test import TestCase


class DomainIndexTest(TestCase):

    def setUp(self):

        self.resp = self.client.get('/domain/')

    def test_get_domain(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template(self):

        self.assertTemplateUsed(self.resp, 'domain/index.html')

    def test_template_has_link_for_topic(self):

        self.assertContains(self.resp, 'a data-rel="tooltip" title="" class="well span3 top-block" href="/domain/topic/"', 1)

    def test_template_has_link_for_theoretical_exercices(self):

        self.assertContains(self.resp, 'a data-rel="tooltip" title="" class="well span3 top-block" href="/domain/theoretical/"', 1)

    def test_template_has_link_for_pratical_exercices(self):

        self.assertContains(self.resp, 'a data-rel="tooltip" title="" class="well span3 top-block" href="/domain/pratical/"', 1)


class TopicIndexTest(TestCase):

    def setUp(self):

        self.resp = self.client.get('/domain/topic/')

    def test_get_topic(self):

        self.assertEqual(200, self.resp.status_code)

    def test_template(self):

        self.assertTemplateUsed(self.resp, 'domain/topic.html')

    def test_template_has_button_for_add_topic(self):

        self.assertContains(self.resp, '<button class="btn btn-small btn-success btn-setting" onClick="parent.location=\'/domain/topic/add/\'"')

    #def test_template_has_button_for_view_topic(self):

    #    self.assertContains(self.resp, '<a onClick="#" class="btn btn-success" href="#"')


class TopicAddGetTest(TestCase):

    def setUp(self):

        self.resp = self.client.get('/domain/topic/add/')

    def test_get_add_topic(self):

        self.assertEqual(200, self.resp.status_code)
