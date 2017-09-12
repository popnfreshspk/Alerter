![alt text](http://i.imgur.com/J5WWmGH.png) Alerter ![alt text](http://i.imgur.com/iaFq7mW.png)
=======
Alerter is a decorator that converts a function into an e-mail notifier about errors. This is meant to be an easy way to implement custom state based alerts.

Alerter uses Fibonacci to determine the next time to send an alert, and keeps processes that enter bad states from flooding your inbox.

![alt text](http://i.imgur.com/RU7rjf9.png)

![alt text](http://i.imgur.com/J5WWmGH.png) Setup
=====
#### Getting started
Update `Config.py.example` with your configuration parameters. Rename this file `Config.py` and move it into the `src` directory.


#### Configuration
```python
Config.py
notification_emails = [
	'array_of_emails@email.com'
]

email_user = 'gmailuser'
email_password = 'gmailpassword'

default_directory = 'directory where logs will be saved'

slack_endpoint = 'post endpoint for slack webhook'
```

![alt text](http://i.imgur.com/J5WWmGH.png) Implementation
==============
The function that alerter decorates must return a tuple (bool, string):
	bool - whether or not an alert should be sent.
	string - the message to be sent along with the alert.

```python
from Alerter import alerter

@alerter(name='passing_alert', path='~/')
def passing_alert():
	return (False, '')

@alerter(name='failing_alert', path='~/')
def failing_alert():
	return (True, 'This alert is sent because a failure criteria is met.')

# this alert will send an exception indicating the alert itself has failed.
@alerter(name='exception_alert', path='~/')
def exception_alert():
	return 1/0
```

![alt text](http://i.imgur.com/J5WWmGH.png) Webhooks
========
Will work out of the box with Slack. Go to: https://api.slack.com/incoming-webhooks to configure.
