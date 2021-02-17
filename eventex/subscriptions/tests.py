from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscribe'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscription_form.html')

    def test_html(self):
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Amauri Rossetti', cpf='12345678901', email='amauri@gmail.com', phone='11999998888')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEqual(self.resp.status_code, 302)