"""webapps2023 URL Configuration"""

from django.contrib import admin
from django.urls import include, path
import register.views  as reg_views


urlpatterns = [
    path('', reg_views.login_user),
    path('admin/', admin.site.urls),
    path('payapp/', include('payapp.urls')),
    path('register/', include('register.urls')),
    path('login', reg_views.login_user, name='login'),
    path('logout', reg_views.logout_user, name='logout'),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
