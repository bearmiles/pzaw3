
from django.contrib import admin
from django.urls import path, include
from .views import simple_api, loginn, check_login, logoutt

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/simple/', simple_api, name='simple_api'),
    path('api/v1/loginn/', loginn, name="loginn"),
    path('api/v1/user', check_login, name="check_login"),
    path('api/v1/logoutt', logoutt, name="logoutt")
]
