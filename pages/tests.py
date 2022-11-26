from django.test import SimpleTestCase
from django.urls import reverse, resolve

from .views import HomePageView, AboutPageView


class HomePageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(reverse('home'))

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 400)

    def test_homepage_correct_content(self):
        self.assertContains(self.response, 'Home Page')

    def test_homepage_incorrect_content(self):
        self.assertNotContains(self.response, 'Wibble')

    def test_homepage_url_resolves_homepageview(self):
        # Test that the url is handled by the desired view.
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)


class AboutPageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 400)

    def test_aboutpage_correct_content(self):
        self.assertContains(self.response, 'About Page')

    def test_aboutpage_incorrect_content(self):
        self.assertNotContains(self.response, 'Home Page')

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve('/about/')
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)
