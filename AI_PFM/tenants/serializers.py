from rest_framework import serializers
from .models import User, Transaction, Budget
from django.db.models import Sum, Avg

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'tenant')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['tenant'] = request.tenant
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TransactionSerializer(serializers.ModelSerializer):
    budget_title = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self, validated_data):
        # Access the user from the request context
        user = self.context['request'].user
        # Add the user to validated_data
        validated_data['user'] = user
        return super().create(validated_data)

    def get_budget_title(self, obj):
        return obj.budget.title if obj.budget else None
   
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # Get 'fields' from kwargs
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    
    def create(self, validated_data):
        # Access the user from the request context
        user = self.context['request'].user
        # Add the user to validated_data
        validated_data['user'] = user
        return super().create(validated_data)

class UserDashboardSerializer(serializers.ModelSerializer):
    budget_transactions = serializers.SerializerMethodField()
    budgets = serializers.SerializerMethodField()
    averages = serializers.SerializerMethodField()
    
    class Meta:
        model = User  # Or a custom model for dashboard data
        fields = ('budget_transactions', 'budgets', 'averages')
    
    def get_budget_transactions(self, obj):
        # budget_with_totals = Budget.objects.filter(user=obj, active=True, id=self.context.get('budget_id')).annotate(total_amount=Sum('transactions__amount')).order_by('-date')
        if 'budget_id' in self.context:
            return TransactionSerializer(Transaction.objects.filter(user=obj, budget=self.context.get('budget_id')).order_by('date'), many=True).data
        else:
            budget = Budget.objects.filter(user=obj, active=True).order_by('-date').first()
            return TransactionSerializer(Transaction.objects.filter(user=obj, budget=budget.id).order_by('date'), many=True).data
               
    
    def get_budgets(self, obj):
        budget_with_totals = Budget.objects.filter(user=obj, active=True).annotate(total_amount=Sum('transactions__amount')).order_by('-date')
        fields = ['id', 'title', 'total_amount', 'amount']
        return [{'id': budget.id, 'title': budget.title, 'total_amount': budget.total_amount, 'amount': budget.amount}
                for budget in budget_with_totals]
    
    def get_averages(self, obj):
        if 'budget_id' in self.context:
            recent_average = Transaction.objects.filter(user=obj, budget=self.context.get('budget_id')).order_by('date').aggregate(Avg('amount'))
            count = Transaction.objects.filter(user=obj, budget=self.context.get('budget_id')).count()
            last_average = {'amount__avg': 0}
            if count > 1:
                last_average = Transaction.objects.filter(user=obj, budget=self.context.get('budget_id')).order_by('-date')[1:].aggregate(Avg('amount'))       
            if recent_average['amount__avg']:
                diff = round((recent_average['amount__avg']-last_average['amount__avg']) / recent_average['amount__avg'], 2)
            else:
                diff = 0
            
            return {'recent_average': recent_average, 'diff': diff}
        else:
            budget = Budget.objects.filter(user=obj, active=True).order_by('-date').first()
            count = Transaction.objects.filter(user=obj, budget=budget.id).count()
            recent_average = Transaction.objects.filter(user=obj, budget=budget.id).order_by('date').aggregate(Avg('amount'))
            last_average = {'amount__avg': 0}
            
            if count > 1:
                last_average = Transaction.objects.filter(user=obj, budget=budget.id).order_by('-date')[1:].aggregate(Avg('amount'))
            
            if recent_average['amount__avg']:
                diff = round((recent_average['amount__avg']-last_average['amount__avg']) / recent_average['amount__avg'], 2)
            else:
                diff = 0
            return {'recent_average': recent_average, 'diff': diff}

               