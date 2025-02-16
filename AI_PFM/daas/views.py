from rest_framework import viewsets, permissions, response, status
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token    

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
    permission_classes = (permissions.IsAuthenticated,)
    
    @action(detail=False, methods=["GET"], url_path=r'agent/(?P<id>\d+)')
    def agent_list(self, request, id):
        prospects = self.queryset.filter(agent=id)
        return response.Response(self.serializer_class(prospects, many=True).data)
    
    
class DAASObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response.data['username'], response.data['email'] = user.username, user.email  
        return response