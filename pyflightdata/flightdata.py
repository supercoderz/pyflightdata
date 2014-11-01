from .common import REG_BASE, FLT_BASE, get_data


def get_by_flight_number(flight_number):
	url = FLT_BASE+flight_number
	return get_data(url)
	
def get_by_tail_number(tail_number):
	url = REG_BASE+tail_number
	return get_data(url)
