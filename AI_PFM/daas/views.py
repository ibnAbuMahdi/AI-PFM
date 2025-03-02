from rest_framework import viewsets, permissions, response, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token    
import json

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = DAASUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    
    def update(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = self.queryset.get(email=email)
        except User.DoesNotExist:
            return response.Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the password
        user.set_password(password)
        user.activated = True
        # user.code = request.data.get('code')
        user.save()

        serializer = self.get_serializer(user)
        return response.Response(serializer.data)
    
class ProspectViewSet(viewsets.ModelViewSet):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer
    
    @action(detail=False, methods=["GET"], url_path=r'agent/(?P<id>\d+)', permission_classes=[permissions.IsAuthenticated])
    def agent_list(self, request, id):
        prospects = self.queryset.filter(agent=id)
        return response.Response(self.serializer_class(prospects, many=True).data)
    
    
    def create(self, request, *args, **kwargs):
        # Custom logic before creation
        jsondata = request.data.keys()[0]
        data = json.loads(jsondata)
        data.package = data.get('package')[0] if len(data.get('package')) else None
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Custom logic after creation
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class DAASObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response.data['id'], response.data['username'], response.data['email'] = user.id, user.username, user.email  
        return response