"""
.. module:: emailer
   :platform: Unix, Linux
   :synopsis: Sends report data

.. moduleauthor:: Kevin Hsu <k.wk.hsu@gmail.com>

"""
import tempfile
import smtplib
import mimetypes
import json
import pandas
import requests
import json
import numpy as np

from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from Config import email_user, email_password


def send_email(to_email=[], subject=None, file_location=None):

	if isinstance(to_email, list):
		if None in to_email:
			return
		else:
			to_email += []
			email_str = ','.join(to_email)
	else:
		email_str = to_email

	msg = MIMEMultipart()
	msg["From"] = 'noreply' #username
	msg["To"] = ''
	msg["Bcc"] = ''
	msg["Subject"] = subject
	msg.reamble = subject

	if file_location is not None:
		ctype, encoding = mimetypes.guess_type(file_location)
	else:
		ctype = "application/octet-stream"

	maintype, subtype = ctype.split("/", 1)

	if file_location is not None:
		if maintype == "text":
			fp = open(file_location)
			# Note: we should handle calculating the charset
			attachment = MIMEText(fp.read(), _subtype=subtype)
			fp.close()
		elif maintype == "image":
			fp = open(file_location, "rb")
			attachment = MIMEImage(fp.read(), _subtype=subtype)
			fp.close()
		elif maintype == "audio":
			fp = open(file_location, "rb")
			attachment = MIMEAudio(fp.read(), _subtype=subtype)
			fp.close()
		else:
			fp = open(file_location, "rb")
			attachment = MIMEBase(maintype, subtype)
			attachment.set_payload(fp.read())
			fp.close()
			encoders.encode_base64(attachment)

		outname = file_location.split('/')[len(file_location.split('/')) - 1]
		attachment.add_header("Content-Disposition", "attachment", filename=outname)

		msg.attach(attachment)

	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	server.login(email_user,email_password)
	server.sendmail('noreply', to_email, msg.as_string())
	server.quit
