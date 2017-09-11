import requests
import json

from Config import slack_endpoint

def slack(name, error_message):
	payload = {
		'username': 'Rick',
		'icon_url': 'https://i.imgur.com/bYspnwo.png',
		'attachments': [{
			'title': name,
			'color': '#AF0000',
			'text': error_message
		}]
	}

	requests.post(slack_endpoint, data=json.dumps(payload))

def webhook_dispatcher(name, error_message):
	if slack_endpoint:
		slack(name, error_message)	
