from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView


class HomePageTests(SimpleTestCase):

    def setUp(self):
        # Set the response variable for the homepage url so as
        # to be used in all of the following tests.
        url = reverse('home')
        self.response = self.client.get(url)

    def test_homepage_url_exists(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 400)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, '_base.html')
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_correct_content(self):
        self.assertContains(self.response, 'Home page')

    def test_homepage_incorrect_content(self):
        self.assertNotContains(self.response, 'Wibble')

    def test_homepage_url_resolves_homepageview(self):
        # Tests that the url is handled by the desired view.
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
