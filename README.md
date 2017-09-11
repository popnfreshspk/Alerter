Alerter
=======
Alerter is a decorator that converts a function into an e-mail notifier about errors. This is meant to be an easy way to implement custom state based alerts.

Alerter uses Fibonacci to determine the next time to send an alert, and keeps processes that enter bad states from flooding your inbox.

Configuration
=============
```python
Config.py
notification_emails = [
	'array_of_emails@email.com'
]

email_user = 'gmailuser'
email_password = 'gmailpassword'

default_directory = 'directory where logs will be saved'
```

Implementation
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




