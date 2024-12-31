import logging
import traceback
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger('django')

class StatusCodeLoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if 200 <= response.status_code < 300:
            logger.info(f"Info: Successful request. Path: {request.path}, Status code: {response.status_code}")
        elif 400 <= response.status_code < 500:
            logger.warning(f"Warning: Client error. Path: {request.path}, Status code: {response.status_code}")
        elif 500 <= response.status_code < 600:
            logger.error(f"Error: Server error. Path: {request.path}, Status code: {response.status_code}")
        return response

    def process_exception(self, request, exception):
        logger.error(f"Exception occurred in path: {request.path}")
        logger.error(traceback.format_exc())
        return HttpResponse(status=500)
