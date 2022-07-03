from rest_framework.exceptions import APIException

from rest_framework.views import exception_handler

class TagDoesNotExist(APIException):
	status_code = 211
	default_code = 20000
	default_detail = "Tag Does Not Exist"