from rest_framework import viewsets, permissions
from .serializers import UserDashboardSerializer
from .serializers import UserRegistrationSerializer, TransactionSerializer, BudgetSerializer
from .models import User, Transaction, Budget
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

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)