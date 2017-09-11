import pandas

from datetime import datetime
from Emailer import send_email
from Config import notification_emails 

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
			[['', 0, 0, 1]], 
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
		status['count'] = 0
		status['last_message'] = 1
		status['next_message'] = 1
		status.to_csv(state_file, index=None)	
	else:
		status['count'] += 1
		
		status['status'] = 'ERROR'
		if status['count'].max() == status['next_message'].max():
			fibonacci_next_placeholder = status['next_message'].max()
			print fibonacci_next_placeholder
			send_alert = True
			status['next_message'] = fibonacci_next_placeholder + status['last_message'].max()
			status['last_message'] = fibonacci_next_placeholder
		status.to_csv(state_file, index=None)
	
	return send_alert
	
def log(message='', status='OK'):
	now = str(datetime.now().replace(microsecond=0))
	with open('status.log', 'a') as f:
		f.write('[%s] - %s\n' % (now, status + ' ' + message))

def alerter(path='', alert=''):
	"""
		Decorator that wraps a boolean function with alert functionality. 
		Alerters will send alerts based on input function's truth state and 
		use Fibonacci to delay follow up messages.
		
			:param string path: location for alert's statefile
			:param string alert: name of alert
	"""
	def alert_decorator(status_function):
		state_file = path + alert + '.csv'
		error_message = ''
		def output_function():
			status = init_state(state_file)
			
			# status_function is a function that should return true/false
			try:
				failure = status_function()
			except Exception as e:
				failure = True
				error_message = e.message
			
			send_alert = set_state(status, failure, state_file)
			
			if failure:
				log(message=alert + ' ' + error_message, status='ERROR')
				if send_alert:
					send_email(
						to_email = notification_emails,
						subject='[ERROR] %s' % alert
						file_location = state_file
					)
			else:
				log(message=alert, status='OK')
		return output_function
	
	return alert_decorator
