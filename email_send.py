import codecs
import logging
import smtplib
import sys
from email.mime.text import MIMEText

logger = logging.getLogger('email-send-handler')

def send_daily_worklog_missing_mail(config, email, name, escalating, date):
	email_template_file = config['Daily Check']['file']
	logger.debug('Napi munkaidő hiány ellenőrző email template betöltése file-ból (%s)', email_template_file)
	with codecs.open(email_template_file,'r','utf-8') as fp:
		msg_content = fp.read()
		msg_content = msg_content.replace('$day', date)
		msg = MIMEText(msg_content, 'plain', 'utf-8')
	subject = config['Daily Check']['subject']
	subject = subject.replace('$day', date)
	subject = subject.replace('$name',name)
	from_addr = config['Daily Check']['from']
	cc_addrs = ''
	escalating_days_tl = int(config['Daily Check']['escalation_days_tl'])
	logger.debug('Team leader eszkaláció napok száma: %s', escalating_days_tl)
	escalating_days_mgr = int(config['Daily Check']['escalation_days_mgr'])
	logger.debug('Manager eszkaláció napok száma: %s', escalating_days_mgr)
	if escalating>=escalating_days_mgr:
		logger.info('Felhasználó (%s) munkaidő hiány (%s) email küldése team leader-nek és manager-nek', name, date)
		team_leader = config['Daily Check']['team_leader']
		manager = config['Daily Check']['manager']
		cc_addrs = [team_leader, manager]
	elif escalating>=escalating_days_tl:
		logger.info('Felhasználó (%s) munkaidő hiány (%s) email küldése team leader-nek', name, date)
		team_leader = config['Daily Check']['team_leader']
		cc_addrs = [team_leader]

	send_email(from_addr, [email], cc_addrs, subject, msg, config)

def send_email(from_addr, to_addrs, cc_addrs, subject, msg, config):
	logger.debug('Email küldése megadott címről (%s) a megadott cím(ek)re (%s), cc-vel (%s) és subject-el (%s)', from_addr, to_addrs, cc_addrs, subject)
	smtp_host = config['SMTP']['smtp_host']
	smtp_user = config['SMTP']['smtp_user']
	smtp_passwd = config['SMTP']['smtp_passwd']

	msg['Subject'] = subject
	msg['From'] = from_addr
	msg['To'] = ', '.join(to_addrs)
	if cc_addrs:
		msg['Cc'] = ', '.join(cc_addrs)

#	try:
	s = smtplib.SMTP(smtp_host)
	smtp_starttls = config['SMTP']['smtp_starttls']
	if smtp_starttls:
		s.starttls()
	if smtp_user:
		s.login(smtp_user, smtp_passwd)

	recipients = to_addrs
	if cc_addrs:
		recipients = recipients + cc_addrs
	s.sendmail(from_addr, recipients, msg.as_string())
	s.quit()
#	except Exception:
#		print('Failed to send email: ', sys.exc_info()[0])
