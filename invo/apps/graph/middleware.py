"""ariadne_django_jwt middleware module"""
from rest_framework_simplejwt.authentication import JWTAuthentication

__all__ = ["JWTMiddleware"]


class JWTMiddleware:
    """Middleware to be used in conjunction with ariadne grapqh_* methods"""

    def resolve(self, next, root, info, **kwargs):
        """Performs the middleware relevant operations"""
        request = info.context.get("request", None)

        # This probably should be done elsewhere
        auth_result = JWTAuthentication().authenticate(request)
        if auth_result is not None:
            user, token = auth_result
            info.context["user"] = user
            info.context["token"] = token
            setattr(request, "user", user)

        return next(root, info, **kwargs)


# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         import ipdb; ipdb.set_trace()

#         response = self.get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         return response
