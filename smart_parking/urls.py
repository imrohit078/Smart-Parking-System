from django.contrib import admin
from django.urls import path, include
from my_app import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from my_app import views as app_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_app.urls')),
    path('login/', app_views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # path('logout/', app_views.logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('manual-entry/', app_views.manual_entry_view, name='manual_entry'),
    path('update-session/<int:session_id>/', app_views.session_update_view, name='update_session'),
]
