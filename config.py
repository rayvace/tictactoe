#################
# Configuration #
#################

LISTEN_ADDRESS = '0.0.0.0'      		# Address where the application listens
LISTEN_PORT = 8080              		# Port where the application listens
DEBUG = True                    		# Print debut information
THREADED = True                 		# Use multiple threads to perform the Github API calls
MAX_RETRIES = 5                 		# Number of retries for failed requests
DELAY = 1                       		# The default delay (in seconds) to wait before retrying failed requests
BACKOFF = 2                     		# The backoff factor to wait between retries
#NOTE: THROWAWAY KEY
SECRET_KEY = 'SpevaphevazebEVAb4ubrUBu' # Flask app secret key (to decrypt cookies, better shared across all instances)