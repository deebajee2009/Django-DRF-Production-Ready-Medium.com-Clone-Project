"""
Exception handler for Profile app.
"""
from rest_framework import APIException

class CantFollowYourself(APIException):
    """
    Docstring for CantFollowYourself
    """
    status_code = 403
    default_detail = "You can't follow yourself."
    default_code = "forbidden"