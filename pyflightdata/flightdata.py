from metar import Metar

from .common import FlightMixin
from .common_fr24 import (AIRLINE_BASE, AIRLINE_FLT_BASE, AIRPORT_BASE,
                          AIRPORT_DATA_BASE, FLT_BASE, FR24, LOGIN_URL,
                          REG_BASE, ROOT)


class FlightData(FlightMixin):
    """FlightData class is the entry point to the API. 

    This class abstracts the data sources and provides convenient methods to get the various datapoints as JSON lists.
    At the moment flightradar24 is the only data source.

    It is optional to pass in the email and password to login to the site at the time of creating the API object.
    The login method can be invoked at a later point in the code.

    Args:
        email (str): optional email ID used to login to flightradar24
        password (str): password for the user ID

    Example::

        from pyflightdata import FlightData
        f=FlightData()
        f.login(myemail,mypassword)

    """

    _fr24 = FR24()

    def __init__(self, email=None, password=None):
        super(FlightData, self).__init__()
        if email and password:
            self.login(email, password)

    # Flight related information - primarily from flightradar24
    def get_history_by_flight_number(self, flight_number, page=1, limit=100):
        """Fetch the history of a flight by its number.

        This method can be used to get the history of a flight route by the number.
        It checks the user authentication and returns the data accordingly.

        Args:
            flight_number (str): The flight number, e.g. AI101
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_history_by_flight_number('AI101')
            f.get_history_by_flight_number('AI101',page=1,limit=10)

        """
        url = FLT_BASE.format(flight_number, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_data(url)

    def get_history_by_tail_number(self, tail_number, page=1, limit=100):
        """Fetch the history of a particular aircraft by its tail number.

        This method can be used to get the history of a particular aircraft by its tail number.
        It checks the user authentication and returns the data accordingly.

        Args:
            tail_number (str): The tail number, e.g. VT-ANL
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_history_by_flight_number('VT-ANL')
            f.get_history_by_flight_number('VT-ANL',page=1,limit=10)

        """
        url = REG_BASE.format(tail_number, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_data(url, True)

    def get_countries(self):
        """Returns a list of all countries
        This can be used to get the country name/code as it is known on flightradar24
        """
        return self._fr24.get_countries_data()

    def get_airports(self, country):
        """Returns a list of all the airports
        For a given country this returns a list of dicts, one for each airport, with information like the iata code of the airport etc

        Args:
            country (str): The country for which the airports will be fetched

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            f.get_airports('India')

        """
        url = AIRPORT_BASE.format(country.replace(" ", "-"))
        return self._fr24.get_airports_data(url)

    def get_info_by_tail_number(self, tail_number, page=1, limit=100):
        """Fetch the details of a particular aircraft by its tail number.

        This method can be used to get the details of a particular aircraft by its tail number.
        Details include the serial number, age etc along with links to the images of the aircraft.
        It checks the user authentication and returns the data accordingly.

        Args:
            tail_number (str): The tail number, e.g. VT-ANL
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_info_by_flight_number('VT-ANL')
            f.get_info_by_flight_number('VT-ANL',page=1,limit=10)
        """
        url = REG_BASE.format(tail_number, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_aircraft_data(url)

    def get_airlines(self):
        """Returns a list of all the airlines in the world that are known on flightradar24

        The return value is a list of dicts, one for each airline, with details like the airline code on flightradar24, call sign, codes etc.
        The airline code can be used to get the fleet and the flights from flightradar24

        """
        url = AIRLINE_BASE.format('')
        return self._fr24.get_airlines_data(url)

    def get_fleet(self, airline_key):
        """Get the fleet for a particular airline.

        Given a airline code form the get_airlines() method output, this method returns the fleet for the airline.

        Args:
            airline_key (str): The code for the airline on flightradar24

        Returns:
            A list of dicts, one for each aircraft in the airlines fleet

        Example::
            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_fleet('ai-aic')
        """
        url = AIRLINE_BASE.format(airline_key)
        return self._fr24.get_airline_fleet_data(url)

    def get_flights(self, airline_key):
        """Get the flights for a particular airline.

        Given a airline code form the get_airlines() method output, this method returns the scheduled flights for the airline.

        Args:
            airline_key (str): The code for the airline on flightradar24

        Returns:
            A list of dicts, one for each scheduled flight in the airlines network

        Example::
            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_flights('ai-aic')
        """
        url = AIRLINE_FLT_BASE.format(airline_key)
        return self._fr24.get_airline_flight_data(url)

    def get_airport_weather(self, iata, page=1, limit=100):
        """Retrieve the weather at an airport

        Given the IATA code of an airport, this method returns the weather information.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_weather('HYD')
            f.get_airport_weather('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        weather = self._fr24.get_airport_weather(url)
        mi = weather['sky']['visibility']['mi']
        if (mi is not None) and (mi != "None"):
            mi = float(mi)
            km = mi * 1.6094
            weather['sky']['visibility']['km'] = km
        return weather

    def get_airport_metars(self, iata, page=1, limit=100):
        """Retrieve the metar data at the current time

        Given the IATA code of an airport, this method returns the metar information.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            The metar data for the airport

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_metars('HYD')

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        w = self._fr24.get_airport_weather(url)
        return w['metar']

    def get_airport_metars_hist(self, iata):
        """Retrieve the metar data for past 72 hours. The data will not be parsed to readable format.

        Given the IATA code of an airport, this method returns the metar information for last 72 hours.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD

        Returns:
            The metar data for the airport

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_metars_hist('HYD')

        """
        url = AIRPORT_BASE.format(iata) + "/weather"
        return self._fr24.get_airport_metars_hist(url)

    def get_airport_stats(self, iata, page=1, limit=100):
        """Retrieve the performance statistics at an airport

        Given the IATA code of an airport, this method returns the performance statistics for the airport.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_stats('HYD')
            f.get_airport_stats('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_airport_stats(url)

    def get_airport_details(self, iata, page=1, limit=100):
        """Retrieve the details of an airport

        Given the IATA code of an airport, this method returns the detailed information like lat lon, full name, URL, codes etc.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_details('HYD')
            f.get_airport_details('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        details = self._fr24.get_airport_details(url)
        weather = self._fr24.get_airport_weather(url)
        # weather has more correct and standard elevation details in feet and meters
        details['position']['elevation'] = weather['elevation']
        return details

    def get_airport_reviews(self, iata, page=1, limit=100):
        """Retrieve the passenger reviews of an airport

        Given the IATA code of an airport, this method returns the passenger reviews of an airport.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_reviews('HYD')
            f.get_airport_reviews('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_airport_reviews(url)

    def get_airport_arrivals(self, iata, page=1, limit=100):
        """Retrieve the arrivals at an airport

        Given the IATA code of an airport, this method returns the arrivals information.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_arrivals('HYD')
            f.get_airport_arrivals('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_airport_arrivals(url)

    def get_airport_departures(self, iata, page=1, limit=100):
        """Retrieve the departures at an airport

        Given the IATA code of an airport, this method returns the departures information.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_departures('HYD')
            f.get_airport_departures('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_airport_departures(url)

    def get_airport_onground(self, iata, page=1, limit=100):
        """Retrieve the aircraft on ground at an airport

        Given the IATA code of an airport, this method returns the aircraft on the ground at the airport.

        Args:
            iata (str): The IATA code for an airport, e.g. HYD
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A list of dicts with the data; one dict for each row of data from flightradar24

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_airport_onground('HYD')
            f.get_airport_onground('HYD',page=1,limit=10)

        """
        url = AIRPORT_DATA_BASE.format(iata, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_airport_onground(url)

    def get_images_by_tail_number(self, tail_number, page=1, limit=100):
        """Fetch the images of a particular aircraft by its tail number.

        This method can be used to get the images of the aircraft. The images are in 3 sizes and you can use what suits your need.

        Args:
            tail_number (str): The tail number, e.g. VT-ANL
            page (int): Optional page number; for users who are on a plan with flightradar24 they can pass in higher page numbers to get more data
            limit (int): Optional limit on number of records returned

        Returns:
            A dict with the images of the aircraft in various sizes

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            #optional login
            f.login(myemail,mypassword)
            f.get_images_by_flight_number('VT-ANL')
            f.get_images_by_flight_number('VT-ANL',page=1,limit=10)
        """
        url = REG_BASE.format(tail_number, str(self.AUTH_TOKEN), page, limit)
        return self._fr24.get_aircraft_image_data(url)

    def login(self, email, password):
        """Login to the flightradar24 session

        The API currently uses flightradar24 as the primary data source. The site provides different levels of data based on user plans.
        For users who have signed up for a plan, this method allows to login with the credentials from flightradar24. The API obtains
        a token that will be passed on all the requests; this obtains the data as per the plan limits.

        Args:
            email (str): The email ID which is used to login to flightradar24
            password (str): The password for the user ID

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            f.login(myemail,mypassword)

        """
        response = FlightData.session.post(
            url=LOGIN_URL,
            data={
                'email': email,
                'password': password,
                'remember': 'true',
                'type': 'web'
            },
            headers={
                'Origin': 'https://www.flightradar24.com',
                'Referer': 'https://www.flightradar24.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
            }
        )
        response = self._fr24.json_loads_byteified(
            response.content) if response.status_code == 200 else None
        if response:
            token = response['userData']['subscriptionKey']
            self.AUTH_TOKEN = token

    def logout(self):
        """Logout from the flightradar24 session.

        This will reset the user token that was retrieved earlier; the API will return data visible to unauthenticated users
        """
        self.AUTH_TOKEN = ''

    def is_authenticated(self):
        """Simple method to check if the user is authenticated to flightradar24"""
        return not self.AUTH_TOKEN == ''

    def decode_metar(self, metar):
        """
        Simple method that decodes a given metar string.

        Args:
            metar (str): The metar data

        Returns:
            The metar data in readable format

        Example::

            from pyflightdata import FlightData
            f=FlightData()
            f.decode_metar('WSSS 181030Z 04009KT 010V080 9999 FEW018TCU BKN300 29/22 Q1007 NOSIG')
        """
        m = Metar.Metar(metar)
        return m.string()
