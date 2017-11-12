from .common_fr24 import REG_BASE, FLT_BASE, AIRPORT_BASE, AIRLINE_BASE, AIRLINE_FLT_BASE, LOGIN_URL, ROOT, FR24
from .common import FlightMixin


class FlightData(FlightMixin):

    fr24=FR24()

    def __init__(self, email=None,password=None):
        super(FlightData, self).__init__()
        if email and password:
            self.login(email,password)

    #Flight related information - primarily from flightradar24
    def get_history_by_flight_number(self,flight_number,page=1,limit=100):
        url = FLT_BASE.format(flight_number,str(self.AUTH_TOKEN),page,limit)
        return self.fr24.get_data(url)

    def get_history_by_tail_number(self,tail_number,page=1,limit=100):
        url = REG_BASE.format(tail_number,str(self.AUTH_TOKEN),page,limit)
        return self.fr24.get_data(url, True)

    def get_countries(self):
        return self.fr24.get_countries_data()

    def get_airports(self,country):
        url = AIRPORT_BASE.format(country.replace(" ","-"))
        return self.fr24.get_airports_data(url)

    def get_info_by_tail_number(self,tail_number):
        url = AIRLINE_BASE.format(tail_number)
        return self.fr24.get_aircraft_data(url)

    def get_airlines(self):
        url = AIRLINE_BASE.format('')
        return self.fr24.get_airlines_data(url)

    def get_fleet(self,airline_key):
        url = AIRLINE_BASE.format(airline_key)
        return self.fr24.get_airline_fleet_data(url)

    def get_flights(self,airline_key):
        url = AIRLINE_FLT_BASE.format(airline_key)
        return self.fr24.get_airline_flight_data(url)

    #Route and range related information from gcmap
    def get_range_map(self,airport,*range,**options):
        pass
        
    def get_path_map(self,*pathsegment,**options):
        pass

    #Pictures from jetphotos and airliners.net
    def get_images_by_tail(self,tail_number):
        pass
        
    def login(self,user,password):
        response = FlightData.session.post(
            url=LOGIN_URL,
            data={
                'email': user,
                'password': password,
                'remember': 'true',
                'type': 'web'
            },
            headers={
                'Origin':'https://www.flightradar24.com',
                'Referer':'https://www.flightradar24.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0'
            }
        )
        response = self.fr24.json_loads_byteified(response.content) if response.status_code==200 else None
        if response:
            token=response['userData']['subscriptionKey']
            self.AUTH_TOKEN=token

    def logout(self):
        self.AUTH_TOKEN=''