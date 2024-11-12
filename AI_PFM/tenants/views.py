from rest_framework import viewsets, permissions, status
from .serializers import UserDashboardSerializer
from .serializers import UserRegistrationSerializer, TransactionSerializer, BudgetSerializer
from .models import User, Transaction, Budget
from django.db.models import Sum
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

class UserDashboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserDashboardSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)  

    @action(detail=False, methods=['get'], url_path=r'budgets/(?P<id>\d+)')
    def Budget_Transactions(self, request, id=None):
        user = self.get_queryset()
        context = super().get_serializer_context()
        context['budget_id'] = id
        serializer = self.get_serializer(user, many=True, context=context)
        return Response(serializer.data) 
    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Pass the request to the serializer context
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
                    

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all().order_by('-date')
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Pass the request to the serializer context
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'history')
    def budgets_history(self, request):
        budget_with_totals = Budget.objects.filter(user=request.user, active=True).annotate(total_amount=Sum('transactions__amount')).order_by('date')
        fields = ['id', 'title', 'total_amount', 'amount', 'category', 'date', 'period']
        return Response([{'id': budget.id, 'title': budget.title, 'total_amount': budget.total_amount, 'amount': budget.amount, 'category': budget.category, 'date': budget.date, 'period': budget.period}
                for budget in budget_with_totals]) 
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {
            'budget': self.get_serializer(instance).data,
            'transactions': TransactionSerializer(instance.transactions.all(), many=True).data
        }
        return Response(data)