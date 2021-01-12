import json
import base64
import requests
from teams.models import DataSource


def get_auth_string(user):
    auth_string = user.agency.api_username + ":" + user.agency.api_password
    return base64.b64encode(auth_string.encode('utf-8'))


def get_headers(auth):
    return {'authorization': "Basic " + auth.decode('utf-8'), 'Content-Type': 'application/json'}


def send_api_request(method, url, user, request_body):
    auth = get_auth_string(user)
    headers = get_headers(auth)
    if method == 'POST':
        return requests.post(url, headers=headers, data=json.dumps(request_body)).json()
    elif method == 'GET':
        return requests.get(url, headers=headers, data=json.dumps(request_body)).json()
    elif method == 'DELETE':
        return requests.delete(url, headers=headers, data=json.dumps(request_body)).json()


def map_travellers(travellers):
    travellers = ['ADT'] * travellers['adult'] + ['CHD'] * travellers['child'] + ['INF'] * travellers['infant'] + \
                 ['STU'] * travellers['student'] + ['YTH'] * travellers['youth']
    return travellers


def get_data_source_from_provider(provider):
    if provider == '1A':
        return 'amadeus'
    else:
        return 'travelport'


def get_search_credentials(user):
    credentials = []
    data_sources = DataSource.objects.all().filter(agency=user.agency)
    for source in data_sources:
        if source.active:
            credentials.append({"pcc": source.pcc, "provider": source.provider, "data_source": source.name})

    return credentials


def add_common_parameters(trip, user):
    trip['travellers'] = map_travellers(trip['travellers'])
    trip.update({"alliance": trip.get('alliance', ''),
                 "refundable": trip.get('refundable', False),
                 "permitted_carriers": trip.get('permitted_carriers', []),
                 "time_value": 1,
                 "credentials": get_search_credentials(user),
                 "exclude_carriers": user.common_parameters.exclude_carriers,
                 "search_brands": user.common_parameters.amadeus_branded_fares,
                 "mix_structures": True,
                 "prohibit_unbundled_fares": trip.get('prohibit_unbundled_fares', False),
                 "currency": trip['currency'],
                 "source": 'app.tripninja.io',
                 "user_email": user.email,
                 "markup": user.common_parameters.markup,
                 "markup_by_itinerary": user.common_parameters.markup_by_itinerary,
                 'num_results': 250})
    return trip

def get_user_queue(user):
    return user.agency.datasource.first().queue