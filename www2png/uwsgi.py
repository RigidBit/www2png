"""
Main entry point when being run in uWSGI mode.
"""

from web import app as application

if __name__ == "__main__":
	application.run()
