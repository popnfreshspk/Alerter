import sys

from src import alerter
from src import Config

default_directory = Config.default_directory

@alerter(name='passing_alert', path=default_directory)
def passing_alert():
	return (False, '')


@alerter(name='failing_alert', path=default_directory)
def failing_alert():
	return (True, 'Failing alert')


@alerter(name='exception_alert', path=default_directory)
def exception_alert():
	return 1/0


if __name__ == '__main__':
	passing_alert()
	failing_alert()
	exception_alert()

