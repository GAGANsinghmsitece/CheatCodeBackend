from rest_framework.exceptions import APIException

from rest_framework.views import exception_handler

class TagDoesNotExist(APIException):
	status_code = 211
	default_detail = "Tag Does Not Exist"

class InvalidQuestion(APIException):
	status_code = 400
	default_detail = "You are trying to submit an invalid question"

class InvalidRequest(APIException):
	status_code = 400
	default_detail = "Bad Request"

class UserDoesNotExist(APIException):
	status_code = 400
	default_detail = "User does not Exist"