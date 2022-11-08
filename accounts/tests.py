from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testuser123',
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, 'testuser')
        self.assertEqual(get_user_model().objects.all()[0].email, 'testuser@email.com')

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@email.com',
            password='testsuperuser123'
        )
        self.assertEqual(user.username, 'testsuperuser')
        self.assertEqual(user.email, 'testsuperuser@email.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, 'testsuperuser')
        self.assertEqual(get_user_model().objects.all()[0].email, 'testsuperuser@email.com')


class SignupPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_page_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 302)
        self.assertNotEqual(self.response.status_code, 400)

    def test_signup_page_template(self):
        self.assertTemplateUsed(self.response, "_base.html")
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertTemplateNotUsed(self.response, "home.html")
        self.assertTemplateNotUsed(self.response, "account/login.html")

    def test_signup_page_content(self):
        self.assertContains(self.response, "Sign up")
        self.assertContains(self.response, "E-mail")
        self.assertContains(self.response, "Password")
        self.assertNotContains(self.response, "Home page")
        self.assertNotContains(self.response, "About page")


class LoginPageTests(TestCase):

    def setUp(self):
        url = reverse("account_login")
        self.response = self.client.get(url)

    def test_login_page_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 302)
        self.assertNotEqual(self.response.status_code, 400)

    def test_login_page_template(self):
        self.assertTemplateUsed(self.response, "_base.html")
        self.assertTemplateUsed(self.response, "account/login.html")
        self.assertTemplateNotUsed(self.response, "home.html")
        self.assertTemplateNotUsed(self.response, "account/logout.html")

    def test_login_page_content(self):
        self.assertContains(self.response, "Log in")
        self.assertContains(self.response, "E-mail")
        self.assertContains(self.response, "Password")
        self.assertContains(self.response, '<form method="post">')
        self.assertContains(self.response, '<button class="btn btn-success" type="submit">Log in</button>')
        self.assertNotContains(self.response, "Home page")
        self.assertNotContains(self.response, "About page")


class LogoutPageTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@email.com',
            password='testuser123',
        )
        self.client.force_login(self.user)
        url = reverse("account_logout")
        self.response = self.client.get(url)

    def test_logout_page_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertNotEqual(self.response.status_code, 302)
        self.assertNotEqual(self.response.status_code, 400)

    def test_logout_page_template(self):
        self.assertTemplateUsed(self.response, "_base.html")
        self.assertTemplateUsed(self.response, "account/logout.html")
        self.assertTemplateNotUsed(self.response, "home.html")
        self.assertTemplateNotUsed(self.response, "account/login.html")

    def test_logout_page_content(self):
        self.assertContains(self.response, "Log out")
        self.assertContains(self.response, "Are you sure you want to log out?")
        self.assertContains(self.response, '<button class="btn btn-danger" type="submit">Log out</button>')
        self.assertNotContains(self.response, "Log in")
        self.assertNotContains(self.response, "Home page")
        self.assertNotContains(self.response, "About page")
