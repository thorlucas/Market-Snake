import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import marketsnake.alerts.alert as alert
import configparser

class Email(object):
	def __init__(self, configFile):
		config = configparser.ConfigParser(interpolation=None)
		config.read(configFile)
		mailOpts = config['MAIL']

		# TODO: Catch errors
		self.server = smtplib.SMTP_SSL(host=mailOpts['SMTP_HOST'], port=mailOpts['SMTP_PORT'])
		self.server.ehlo()

		self.mailAddress = mailOpts['MAIL_ADDRESS']

		self.server.login(self.mailAddress, mailOpts['MAIL_PASSWORD'])

	def sendEmail(self, to, subject, body):
		msg = MIMEMultipart()
		msg['From'] = self.mailAddress
		msg['To'] = to
		msg['Subject'] = subject
		msg.attach(MIMEText(body, 'plain'))

		self.server.send_message(msg)


class EmailAlert(alert.AbstractAlert):
	def __init__(self, email, to, subject):
		super().__init__(alert.Callback(email.sendEmail, {'to' : to, 'subject' : subject}))

	def __call__(self, body):
		self.callback({'body' : body})