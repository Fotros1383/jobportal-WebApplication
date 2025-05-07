from django.http import HttpResponseRedirect

class RedirectOnAuthFailureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if token_expired flag was set during authentication
        if hasattr(request, 'token_expired') and request.token_expired:
            if not request.path.startswith('/api/login'):  # Prevent redirect loops
                response = HttpResponseRedirect('/api/login/')
                response.delete_cookie('user_token')
                return response
        
        return response