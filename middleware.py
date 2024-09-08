import datetime
from accounts.models import User


class UpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code that is executed in each request before the view is called
        response = self.get_response(request)

        # Update the field if the requested API matches the desired endpoint
        if request.path_info == '/journals/':

            uid = request.user.id
            # Update the field in your database model using Django ORM
            User.objects.filter(id=uid).update(last_login=datetime.datetime.now())

        # Code that is executed in each request after the view is called
        return response
