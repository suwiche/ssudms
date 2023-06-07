from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', include('backend.urls')),
    path('', include('landingpage.urls')),
    path('dashboard/', include('frontend.urls')),
    url(r'^oidc/', include('keycloak_oidc.urls')),
]
