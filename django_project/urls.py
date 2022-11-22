from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from allauth.account import views as allauth_views


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # User authentication
    path('accounts/', include('allauth.urls')),
    # allauth's PasswordChangeView redirects to the same form upon success.
    # This is a known issue. Below, the url for PasswordChangeView is overridden to specify
    # the desired redirect url. This solution taken from the issue page:
    # https://github.com/pennersr/django-allauth/issues/468#issuecomment-643840017
    path(
        'account/password/change/',
        login_required(
            allauth_views.PasswordChangeView.as_view(success_url=reverse_lazy('home'))
        ),
        name='account_change_password'
    ),
    # Local apps
    path('', include('pages.urls')),
    path('books/', include('books.urls')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
