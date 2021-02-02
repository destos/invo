from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        refresh = serializer.validated_data.pop("refresh", None)
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        if refresh:
            # TODO: , domain= from site session or root domain from settings?
            # TODO: restrict authentication to only site apis that you have access to?
            response.set_cookie("refresh_token", refresh, secure=not settings.DEBUG)
        return response
