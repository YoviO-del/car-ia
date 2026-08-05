import logging
from scraping import apify_client

# Configure the Apify client logger
apify_client_logger = logging.getLogger('apify_client')
apify_client_logger.setLevel(logging.DEBUG)
apify_client_logger.addHandler(logging.StreamHandler())


# attempt - Number of retry attempts for the request.
# status_code - HTTP status code of the response. Only present on records about a request's outcome.
# url - URL of the API endpoint being called.
# client_method - Method name of the client that initiated the request.
# resource_id - Identifier of the resource being accessed.