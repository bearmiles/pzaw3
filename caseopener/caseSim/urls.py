
from django.contrib import admin
from django.urls import path, include
from .views import simple_api, loginn

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/simple/', simple_api, name='simple_api'),
    path('api/v1/loginn/', loginn, name="loginn"),
]
