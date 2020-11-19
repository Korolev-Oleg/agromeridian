from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

# registration
urlpatterns = [
    url(r"^token_validation/", views.validate_registration_token, name='token-validation'),
    path('registration/', views.get_registration_form, name='registration'),
]

# Cabinet
urlpatterns += [
    path('login_redirect/', views.login_redirect, name='login-redirect'),
    path('', RedirectView.as_view(url='/login_redirect/')),
    path('cabinet/', views.UserPassesView.as_view(), name='cabinet'),
]

# Passes
urlpatterns += [
    url('^cabinet/passes/new/$', views.renew_passes_form, name='passes-new'),
    url(r'^cabinet/passes/(?P<pk>\d+)/renew/$', views.renew_passes_form, name='passes-renew'),
]

# Zip
urlpatterns += [
    url(r'^getzip/(?P<pk>\d+)$', views.get_zip, name='get-zip')
]
