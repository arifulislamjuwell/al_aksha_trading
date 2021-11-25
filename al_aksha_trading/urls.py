
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views.authenticate import AuthenticationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', AuthenticationView.as_view(), name= "login_url"),
    path('logout/', AuthenticationView.as_view(), name= "logout_url"),
    path('', include('dashboard.urls', namespace= 'dashboard'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)