from .models import CustomUser

class UpdateLastActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Update the last active time
            request.user.update_last_active()

        response = self.get_response(request)
        return response