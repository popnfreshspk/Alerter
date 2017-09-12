import requests
import json

from numpy import random
from Config import slack_endpoint

quotes = [
	"Wubba-lubba-dub-dub!\n",
	"Uncertainty is inherently unsustainable. Eventually, everything either is or isn't. And we've got about four hours to be 'is.'\n",
	"Break the cycle, Morty. Rise above. Focus on science.\n",
	"That's planning for failure Morty... Even dumber than regular planning.\n",
	"Sometimes science is more art than science, Morty. Lot of people don't get that.\n",
	"Get your shit together. Get it all together, and put it in a backpack, all your shit, so it's together. And if you gotta take it somewhere, take it somewhere. You know? Take it to the shit store and sell it. Or put it in a shit museum, I don't care what you do, you just gotta get it together.\nGet your shit together.\n"
]

def slack(name, error_message):
	payload = {
		'username': 'Rick',
		'icon_url': 'https://i.imgur.com/bYspnwo.png',
		'text': quotes[random.randint(len(quotes))],
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
