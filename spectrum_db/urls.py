from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^search/$', 
        views.SearchLicence.as_view(), 
        name='search_licence'),
    url(r'^licence_detail/$', 
        views.LicenceDetail.as_view(), 
        name='licence_detail'),
    url(r'^location_autocomplete/$',
		views.LocationAutocomplete.as_view(),
		name='location_autocomplete'),
    url(r'^get_location/$',
		views.get_location,
		name='get_location'),
    url(r'^topup_form/$', 
        views.TopupFormView.as_view(), 
        name='top_up_form'),
    url(r'^topup/$', 
        views.TopupView.as_view(), 
        name='top_up'),
    url(r'^charge_guest/$',
        views.charge_guest,
        name='charge_guest'),
    url(r'^thank_you/$', 
        views.SuccessView.as_view(), 
        name='thank_you'),
]
