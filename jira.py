import json
import logging
import requests

logger = logging.getLogger('jira-handler')

def query_jira_worklogs(jira_url, jira_user, jira_passwd, start_date, end_date, work_user):
	url = jira_url+'/rest/jira-worklog-query/1.2.1/find/worklogs'
	params = dict(
        	startDate=start_date,
	        endDate=end_date,
	        user=work_user
	)

	logger.debug('Jira-ból munkaidők lekérdezése %s felhasználónak a megadott időszakra (%s - %s)', work_user, start_date, end_date)
	resp = requests.get(url=url, params=params, auth=(jira_user, jira_passwd))
	return json.loads(resp.text)

def query_user_details(jira_url, jira_user, jira_passwd, username):
	url = jira_url+'/rest/api/2/user'
	params = dict(
		username=username
	)
	logger.debug('Jira-ból felhasználó (%s) részletes adatok lekérdezése', username)
	resp = requests.get(url=url, params=params, auth=(jira_user, jira_passwd))
	return json.loads(resp.text)
