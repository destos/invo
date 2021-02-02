"""ariadne_django_jwt middleware module"""
from rest_framework_simplejwt.authentication import JWTAuthentication


__all__ = ["JWTMiddleware"]


class JWTMiddleware:
    """Middleware to be used in conjunction with ariadne grapqh_* methods"""

    def resolve(self, next, root, info, **kwargs):
        """Performs the middleware relevant operations"""
        request = info.context.get("request", None)

        auth_result = JWTAuthentication().authenticate(request)
        if auth_result is not None:
            user, token = auth_result
            info.context["user"] = user
            info.context["token"] = token
            setattr(request, "user", user)

        return next(root, info, **kwargs)
