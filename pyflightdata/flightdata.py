from .common_fr24 import REG_BASE, FLT_BASE, AIRPORT_BASE, AIRLINE_BASE, AIRLINE_FLT_BASE,get_data, get_countries_data
from .common_fr24 import get_airports_data, get_aircraft_data, get_airlines_data, get_airline_fleet_data, get_airline_flight_data

# most of these are resundant from common.py
# doing it this way so that we can tweak for different sites later


def get_history_by_flight_number(flight_number):
    url = FLT_BASE.format(flight_number)
    return get_data(url)


def get_history_by_tail_number(tail_number):
    url = REG_BASE.format(tail_number)
    return get_data(url, True)


def get_countries():
    return get_countries_data()


def get_airports(country):
    url = AIRPORT_BASE.format(country)
    return get_airports_data(url)


def get_info_by_tail_number(tail_number):
    url = AIRLINE_BASE.format(tail_number)
    return get_aircraft_data(url)


def get_airlines():
    url = AIRLINE_BASE.format('')
    return get_airlines_data(url)


def get_fleet(airline_key):
    url = AIRLINE_BASE.format(airline_key)
    return get_airline_fleet_data(url)


def get_flights(airline_key):
    url = AIRLINE_FLT_BASE.format(airline_key)
    return get_airline_flight_data(url)
