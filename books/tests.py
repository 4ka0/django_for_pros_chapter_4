from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from .models import Book, Review


class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="review_user",
            email="review_user@email.com",
            password="testpass123",
        )

        cls.special_permission = Permission.objects.get(
            codename="special_status",
        )

        cls.book1 = Book.objects.create(
            title="Harry Potter",
            author="JK Rowling",
            price="25.00",
        )

        cls.book2 = Book.objects.create(
            title="Dirty Harry",
            author="Bobby Davro",
            price="30.00",
        )

        cls.book3 = Book.objects.create(
            title="The Two Towers",
            author="J. R. R. Tolkien",
            price="45.00",
        )

        cls.review = Review.objects.create(
            book=cls.book1,
            author=cls.user,
            text="An excellent review!"
        )

    def test_book1_object_creation(self):
        self.assertEqual(f"{self.book1.title}", "Harry Potter")
        self.assertEqual(f"{self.book1.author}", "JK Rowling")
        self.assertEqual(f"{self.book1.price}", "25.00")

    def test_book_page_list_view_when_logged_in(self):
        self.client.login(email="review_user@email.com", password="testpass123")
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "_base.html")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_page_list_view_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=/books/" % (reverse("account_login"))
        )
        response = self.client.get(
            "%s?next=/books/" % (reverse("account_login"))
        )
        self.assertContains(response, "Log In")

    def test_book_detail_view_with_permissions(self):
        self.client.login(email="review_user@email.com", password="testpass123")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book1.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "An excellent review!")
        self.assertTemplateUsed(response, "_base.html")
        self.assertTemplateUsed(response, "books/book_detail.html")

    def test_book_search(self):
        url = "{url}?{filter}={value}".format(
            url=reverse("search_results"),
            filter="q",
            value="Harry"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 400)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "Dirty Harry")
        self.assertNotContains(response, "The Two Towers")
        self.assertTemplateUsed(response, "_base.html")
        self.assertTemplateUsed(response, "books/search_results.html")
