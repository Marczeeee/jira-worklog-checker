import datetime

def calc_date_range(numdays = 7):
	base = datetime.datetime.today()
	base = base.replace(hour=0, minute=0, second=0, microsecond=0)
	date_list = [base - datetime.timedelta(days=x) for x in range(1, numdays+1)]
	return date_list

def convert_date_2_str(date):
	return date.strftime(wlog_date_str_format())

def wlog_date_str_format():
	return '%Y-%m-%d'

def wlog_datetime_str_format():
	return '%Y-%m-%dT%H:%M:%S%z'
