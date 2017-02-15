from dal import autocomplete

from django.http import HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView, View, TemplateView

import stripe

import requests
import requests.auth

import xmltodict, json

import forms

from decimal import Decimal

from djstripe.models import Customer

from models import RSMUserProfile as profile

def get_api_token():
    key=settings.PRODUCT_CLIENT_KEY
    secret=settings.PRODUCT_CLIENT_SECRET
    client_auth = requests.auth.HTTPBasicAuth(key, secret)
    post_data = {"grant_type": "client_credentials"}
    response = requests.post("https://api.business.govt.nz/services/token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    return token_json["access_token"]

def get_licence_detail_xml(licence_id):
    xml_string = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dow="http://rsm.govt.nz/smart/download"><soapenv:Header/><soapenv:Body><dow:LicenceDetailsRequest licenceId="%s"/></soapenv:Body></soapenv:Envelope>' % str(licence_id)
    return xml_string

def search_licence_xml(licensee,
                       transmitLocation,
                       receiveLocation,       
                       applicationNumber,
                       callSign,
                       channel,
                       clientId,
                       dateType,
                       fromDate,
                       fromFrequency,
                       licenceId,
                       licenceNumber,
                       licenceStatus,
                       licenceType,
                       locationId,
                       managementRightId,
                       systemIdentifier,
                       toDate,
                       toFrequency,
                       certifiedBy,
                       includeAssociatedLicences,
                       # gridRefDefault,
                       # engineerDecisionIAgree
                       ):
    fields = ''
    if licensee:
        fields += ' licensee="%s"' % str(applicationNumber)
    if transmitLocation:
        fields += ' transmitLocation="%s"' % str(transmitLocation)
    if receiveLocation:
        fields += ' receiveLocation="%s"' % str(receiveLocation)
    if applicationNumber:
        fields += ' applicationNumber="%s"' % str(applicationNumber)
    if callSign:
        fields += ' callSign=""%s"' % str(callSign)
    if channel:
        fields += ' channel="%s"' % str(channel)
    if clientId:
        fields += ' clientId="%s"' % str(clientId)
    if dateType:
        fields += ' dateType="%s"' % str(dateType)
    if fromDate:
        fields += ' fromDate="%s"' % str(fromDate)
    if fromFrequency:
        fields += ' fromFrequency="%s"' % str(fromFrequency)
    if licenceId:
        fields += ' licenceId="%s"' % str(licenceId)
    if licenceNumber:
        fields += ' licenceNumber="%s"' % str(licenceNumber)
    if licenceStatus:
        fields += ' licenceStatus="%s"' % str(licenceStatus)
    if licenceType:
        fields += ' licenceType="%s"' % str(licenceType)
    if locationId:
        fields += ' locationId="%s"' % str(locationId)
    if managementRightId:
        fields += ' managementRightId="%s"' % str(managementRightId)
    if systemIdentifier:
        fields += ' systemIdentifier="%s"' % str(systemIdentifier)
    if toDate:
        fields += ' toDate="%s"' % str(toDate)
    if toFrequency:
        fields += ' toFrequency="%s"' % str(toFrequency)
    if certifiedBy:
        fields += ' certifiedBy="%s"' % str(certifiedBy)
    if includeAssociatedLicences:
        fields += ' includeAssociatedLicences="%s"' % str(includeAssociatedLicences)
    # if gridRefDefault:
    #     fields += ' gridRefDefault="%s"' % str(gridRefDefault)
    # if engineerDecisionIAgree:
    #     fields += ' engineerDecisionIAgree="%s"' % str(engineerDecisionIAgree)

    xml_string = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dow="http://rsm.govt.nz/smart/download"><soapenv:Header/><soapenv:Body><dow:SearchCriteria %s></dow:SearchCriteria></soapenv:Body></soapenv:Envelope>' % fields
    print(xml_string)
    return xml_string

def send_api_request(url, token, action, xml):
    if action == "search":
        action_string = b'"searchLicences"'
    elif action == "get":
        action_string = b'"getLicenceDetails"'
    else:
        print("Action provided is not available!!")
    
    headers = {'Authorization':'Bearer ' + token,'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': action_string}
    response_xml = requests.post(url, data=xml, headers=headers)
    return response_xml

class SearchLicence(FormView):
    ''''''
    template_name = 'search_licence.html'
    form_class = forms.SearchLicenceForm

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super(SearchLicence, self).get_context_data(**kwargs)

        if user.is_authenticated():
            customer, created = Customer.get_or_create(subscriber=user.id)

            user_profile = profile.objects.get(customer=customer)

            context['are_id'] = user_profile.are_id

        return context

    def post(self, request):
        licensee = self.request.POST.get('Licensee')
        transmitLocation = self.request.POST.get('transmitLocation')
        receiveLocation = self.request.POST.get('receiveLocation')
        applicationNumber = self.request.POST.get('applicationNumber')
        callSign = self.request.POST.get('callSign')
        channel = self.request.POST.get('channel')
        clientId = self.request.POST.get('clientId')
        dateType = self.request.POST.get('dateType')
        fromDate = self.request.POST.get('fromDate')
        fromFrequency = self.request.POST.get('fromFrequency')
        licenceId = self.request.POST.get('licenceId')
        licenceNumber = self.request.POST.get('licenceNumber')
        licenceStatus = self.request.POST.get('licenceStatus')
        licenceType = self.request.POST.get('licenceType')
        locationId = self.request.POST.get('locationId')
        managementRightId = self.request.POST.get('managementRightId')
        systemIdentifier = self.request.POST.get('systemIdentifier')
        toDate = self.request.POST.get('toDate')
        toFrequency = self.request.POST.get('toFrequency')
        certifiedBy = self.request.POST.get('certifiedBy')
        includeAssociatedLicences = self.request.POST.get('includeAssociatedLicences')
        # gridRefDefault = "LAT_LONG_NZGD2000_D2000"
        # engineerDecisionIAgree = self.request.POST.get('engineerDecisionIAgree')

        token = get_api_token()

        xml = search_licence_xml(licensee,
                                 transmitLocation,
                                 receiveLocation,
                                 applicationNumber,
                                 callSign,
                                 channel,
                                 clientId,
                                 dateType,
                                 fromDate,
                                 fromFrequency,
                                 licenceId,
                                 licenceNumber,
                                 licenceStatus,
                                 licenceType,
                                 locationId,
                                 managementRightId,
                                 systemIdentifier,
                                 toDate,
                                 toFrequency,
                                 certifiedBy,
                                 includeAssociatedLicences,
                                 # gridRefDefault,
                                 # engineerDecisionIAgree
                                 )

        action = "search"

        xml_response = send_api_request(settings.DL_PRODUCT_URL, token, action, xml).text.replace("'", '"')
        dict_response = xmltodict.parse(xml_response)

        json_list = []
        for dict_obj in dict_response['env:Envelope']['env:Body']['dow:SearchResult']['summary']:
            json_list.append(dict_obj)

        return JsonResponse({'data': json_list})

class LicenceDetail(TemplateView):
    ''''''
    template_name = 'licence_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(LicenceDetail, self).get_context_data(**kwargs)

        licence_id = self.request.GET.get('licenceId')
        token = get_api_token()
        xml = get_licence_detail_xml(licence_id)

        action = "get"

        xml_response = send_api_request(settings.DL_PRODUCT_URL, token, action, xml).text
        header_part = xml_response[:40].replace("'", '"')
        body_part = xml_response[40:].replace("'", "")
        xml_response = header_part+body_part
        dict_response = xmltodict.parse(xml_response)

        licence = dict_response['env:Envelope']['env:Body']['dow:Licence']

        ctx['data'] = json.dumps(licence)
        ctx['GMAPI'] = settings.GOOGLE_MAPS_API

        extra_info = []

        for point in licence['configurations']:
            if point['location'].get('geoReference'):
                for geoReference in point['location']['geoReference']:
                    if geoReference['@type'] == 'LAT/LONG (NZGD2000)':
                        lat = geoReference['@northing']
                        lng = geoReference['@easting']

                if point['@type'] == "TRN":
                    extra_info.append({
                        'location':
                            {
                                'lat': float(lat), 
                                'lng': float(lng)
                            }, 
                        'tooltip': 
                            {
                                'type': point['@type'], 
                                'district': point['location']['@district'],
                                'height': point['location']['@height'],
                                'id': point['location']['@id'],
                                'name': point['location']['@name'],
                            }
                    })
                elif point['@type'] == "REC":
                    extra_info.append({
                        'location':
                            {
                                'lat': float(lat), 
                                'lng': float(lng)
                            }, 
                        'tooltip': 
                            {
                                'type': point['@type'], 
                                'district': point['location']['@district'],
                                'height': point['location']['@height'] if '@height' in point['location'].keys() else "UNKOWN",
                                'id': point['location']['@id'],
                                'name': point['location']['@name'],
                                'mpis': point['@mpis'],
                                'mpisUom': point['@mpisUom'],
                            }
                    })
                else:
                    extra_info.append({'error': "the configuration type is neither transfer or recieve!!"})

        ctx['extra_info'] = json.dumps(extra_info)
        return ctx

class LocationAutocomplete(autocomplete.Select2QuerySetView):
    '''do not require any additional methods'''

def get_location(request):
    query_string = request.GET.get('q')

    url = "https://api.business.govt.nz/services/v1/radio-spectrum-management/reference-data/searchLocation?locName=%s" % query_string 
    token = get_api_token()
    headers = {'Authorization':'Bearer ' + token,'Accept': 'application/json'}

    response = requests.get(url,headers=headers)
    # print("response is %s" % response.text)
    results = []
    
    print('below are locations: ')
    j = json.loads(response.text)
    unique_check = set()
    for location in j['searchLocationResponse']['locations']:
        check_string = str(location['id']) + str(location['name'])
        if check_string not in unique_check:
            unique_check.add(check_string)
            results.append({'id': location['id'], 'text': str(location['name']) + "ID: " + str(location['id'])})

    results.sort(key=lambda x: x['text'], reverse=True)

    return JsonResponse({'results': results})

#######################################################
##################   Stripe  Views   ##################
#######################################################
class SuccessView(TemplateView):
    template_name = 'thank_you.html'

class TopupFormView(TemplateView):
    template_name = 'topup_form.html'

    def get_context_data(self, **kwargs):
        context = super(TopupView, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context

class TopupView(FormView):
    template_name = 'topup.html'
    form_class = forms.TopupAmountForm
    success_url = '/thank_you/'

    def form_valid(self, form):
        ''''''
        user = self.request.user

        customer, created = Customer.get_or_create(subscriber=user)

        amount = Decimal(form.amount)
        customer.charge(amount)

        user_profile = profile.objects.get(customer=customer)
        user_profile.credit += amount
        user_profile.save()

        return super(TopupView, self).form_valid(form)

def charge_guest(request):
    '''server side reciever to charge customer'''
    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Token is created using Stripe.js or Checkout!
    # Get the payment token submitted by the form:
    token = request.POST['stripeToken']

    # Charge the Customer instead of the card:
    charge = stripe.Charge.create(
      amount=2500,
      currency="nzd",
      description="Charge for %s" % user_email,
      source=token,
    )

    if charge.status == "succeeded":
        pass
        # TO DO 
        # send throught the upload licence request.


