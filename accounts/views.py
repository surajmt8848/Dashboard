from django.db.models import Q
from rest_framework import exceptions, viewsets, status
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Role, User, Permission
from .authentication import generate_access_token, JWTauthentication
from .serializers import UserSerializer, PermissionSerializer, RoleSerializers


@api_view(["GET"])
def users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    data = request.data
    if data["password"] != data["password_confirm"]:
        raise exceptions.APIException("Password Do not Match")

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return Response({"Message": "You are already logged in ..."}, status=400)
    username = request.data.get("username")
    password = request.data.get("password")

    user = (
        User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))
        .distinct()
        .first()
    )

    if user is None:
        raise exceptions.AuthenticationFailed("user not found")

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed("Incorrect password")

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {"jwt": token}
    return response


@api_view(["POST"])
def logout(request):
    response = Response()
    response.delete_cookie(key="jwt")
    response.data = {"message": "success"}
    return response


class AuthenticationUser(APIView):
    authentication_classes = [JWTauthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        serializer = UserSerializer(request.user)

        return Response({"data": serializer.data})


class PermissionAPIView(APIView):
    authentication_classes = [JWTauthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response({"data": serializer.data})


""" Viewsets for role """


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTauthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializers(Role.objects.all(), many=True)
        return Response({"data": serializer.data})

    def create(self, request):
        serializer = RoleSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
