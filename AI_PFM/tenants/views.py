from rest_framework import viewsets, permissions, status
from .serializers import UserDashboardSerializer
from .serializers import UserRegistrationSerializer, TransactionSerializer, BudgetSerializer
from .models import User, Transaction, Budget
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token    
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)  # Allow anyone to register

    def get_serializer_context(self):
        # Add request to the context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response.data['tenant_id'], response.data['username'], response.data['email'] = user.tenant.id, user.username, user.email  # Include tenant ID
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

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Pass the request to the serializer context
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
                    

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)