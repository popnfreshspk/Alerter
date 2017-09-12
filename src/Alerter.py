"""
.. module:: Alerter
   :platform: Unix, Linux
   :synopsis: Module for creating alerts

.. moduleauthor:: Kevin Hsu <k.wk.hsu@gmail.com>

"""
import pandas

from datetime import datetime

from Emailer import send_email
from Webhooks import webhook_dispatcher
from .Config import notification_emails, default_directory 

def log(message='', status='OK'):
	now = str(datetime.now().replace(microsecond=0))
	with open(default_directory + 'status.log', 'a') as f:
		f.write('[%s] - %s\n' % (now, status + ' ' + message))


def init_state(filename):
	"""
		Helper function for using pandas DataFrame for storing alert state.
		
			:param filename str: location of statefile
			
			:returns pandas.DataFrame:
	"""
	try:
		return pandas.read_csv(filename)
	except:
		state = pandas.DataFrame(
			[['', 2, 2, 3]], 
			columns=[
				'status',
				'count',
				'last_message',
				'next_message'
			]
		)
		state.to_csv(filename, index=None)
		return state	  


def set_state(status, failure, state_file):
	"""
		Sets a statefile for a specific alert. Uses Fibonacci to determine
		whether or not to deliver the next alert message.		
		
			:param pandas.DataFrame status: stores the current state of an alert
			:param bool failure: whether or not a failure event has ocurred
			:param string state_file: path for saving state_file
	
			:returns bool: 
	"""
	send_alert = False
	
	if failure == False:
		status['status'] = 'OK'
		status['count'] = 2
		status['last_message'] = 2
		status['next_message'] = 3
		status.to_csv(state_file, index=None)	
	else:
		status['count'] += 1	
		status['status'] = 'ERROR'
		if status['count'].max() >= status['next_message'].max():
			fibonacci_next_placeholder = status['next_message'].max()
			send_alert = True
			status['next_message'] = fibonacci_next_placeholder + status['last_message'].max()
			status['last_message'] = fibonacci_next_placeholder
		status.to_csv(state_file, index=None)
	
	return send_alert


def alerter(name='', path=''):
	"""
		Decorator that wraps a boolean function with alert functionality. 
		Alerters will send alerts based on input function's truth state and 
		use Fibonacci to delay follow up messages.
		
			:param string path: location for alert's statefile
			:param string alert: name of alert

			:returns function: 
	"""
	def alert_decorator(status_function):
		state_file = path + name + '.csv'
		error_message = ''
		def output_function():
			status = init_state(state_file)
			
			# status_function is a function that should return true/false
			exception_status = False
			try:
				failure, error_message = status_function()
			except Exception as e:
				failure = True
				exception_status = 'EXCEPTION'
				error_message = e.message
				
			send_alert = set_state(status, failure, state_file)
			
			if failure:
				log(message=name + ' ' + error_message, status=exception_status if exception_status else 'ERROR')
				if send_alert:
					send_email(
						to_email = notification_emails,
						subject='[Warning] %s - %s' % (name, error_message),
						file_location = state_file
					)
					webhook_dispatcher(name, error_message)
			else:
				log(message=name, status='OK')
		return output_function
	
	return alert_decorator
