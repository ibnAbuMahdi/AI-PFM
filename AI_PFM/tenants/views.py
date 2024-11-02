from rest_framework import viewsets, permissions
from .serializers import UserDashboardSerializer
from .serializers import UserRegistrationSerializer
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token    
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)  # Allow anyone to register
    

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response.data['tenant_id'] = user.tenant.id  # Include tenant ID
        return response

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Logged out successfully.'})


class UserDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = UserDashboardSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)