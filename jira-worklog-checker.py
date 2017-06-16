#!/usr/bin/python

import calendar
import configparser
import logging
from datetime import datetime
from datetime import timedelta
from common import calc_date_range
from common import convert_date_2_str
from common import load_excluded_workdays
from common import wlog_date_str_format
from common import wlog_datetime_str_format
from email_send import send_daily_worklog_missing_mail
from jira import query_jira_worklogs
from jira import query_user_details
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(filename='logs/jira-worklog-checker.log', level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger('jira-worklog-checker')
handler = TimedRotatingFileHandler('logs/jira-worklog-checker.log', when='D', interval=1, backupCount=5)
logger.addHandler(handler)

def process_daily_worklog_check(dates, user, worklogs, excluded_workdays, config):
	wlogs_dict = {}
	for date in dates:
		logger.info('Felhasználó (%s) munkanap (%s) feldolgozása', user['name'], date.date())
		if (date.weekday()<5 and str(date.date()) not in excluded_workdays):
                        wlogs_dict[date] = False
                        for worklog in worklogs[0]:
                                wlog_date = worklog['startDate']
                                wlog_day = datetime.strptime(wlog_date, wlog_datetime_str_format())
                                if wlog_day.date()==date.date():
                                        wlogs_dict[date] = True

	logger.debug('Felhasználó (%s) eredmények feldolgozása', user['name'])
	for day,state in wlogs_dict.items():
		if not state:
			logger.info('Felhasználó (%s) problémás nap: %s', user['name'], day.date())
			day_diff = datetime.now().date()-day.date()
			logger.info('Felhasználó (%s) a %s munkanappal elmaradásban van %s napja', user['name'], day.date(), day_diff.days)
			send_daily_worklog_missing_mail(config, user['emailAddress'], user['displayName'], day_diff.days, convert_date_2_str(day))

def process_user(username, date_range, excluded_workdays, config):
	jira_user = config['Jira']['username']
	jira_passwd = config['Jira']['password']
	jira_url = config['Jira']['url']

	logger.debug('Felhasználó (%s) munkaidők feldolgozása', username)
	start_date = dates[dates.__len__()-1]
	worklogs = query_jira_worklogs(jira_url, jira_user, jira_passwd, convert_date_2_str(start_date), convert_date_2_str(dates[0]), username)
	logger.debug('Felhasználó (%s) részletes adatok lekérdezése', username)
	user = query_user_details(jira_url, jira_user, jira_passwd, username)
	logger.debug('Felhasználó (%s) napi munkaidő adatok ellenőrzése', username)
	process_daily_worklog_check(date_range, user, worklogs, excluded_workdays, config)


today = datetime.today()
config = configparser.ConfigParser()
config.read('config.ini')

dates = calc_date_range(int(config['Daily Check']['days_back']))
logger.info('Worklog ellenőrzés napjai: %s', dates)

excluded_workdays = load_excluded_workdays(config)
logger.info('Ellenőrzés alól kivett napok: %s', excluded_workdays)

users = config['Daily Check']['users'].split(',')
for user in users:
	logger.info('Felhasználó feldolgozása: %s', user)
	if today.weekday()<5:
		logger.info('Felhasználó (%s) napi munkaidejének feldolgozása', user)
		process_user(user, dates, excluded_workdays, config)
	else:
		logger.info('Hétvége, nincs munkaidő ellenőrzés')
#	if today.day==1:
#		print('Felhasználó előző havi munkaidejének feldolgozása:', user)		
#		print('----------')
