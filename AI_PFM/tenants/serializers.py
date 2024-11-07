from rest_framework import serializers
from .models import User, Transaction, Budget
from django.db.models import Sum

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
    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self, validated_data):
        # Access the user from the request context
        user = self.context['request'].user
        # Add the user to validated_data
        validated_data['user'] = user
        return super().create(validated_data)

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
    recent_transactions = serializers.SerializerMethodField()
    budget_summary = serializers.SerializerMethodField()
    budget_transactions = serializers.SerializerMethodField()
    budgets = serializers.SerializerMethodField()

    class Meta:
        model = User  # Or a custom model for dashboard data
        fields = ('recent_transactions', 'budget_summary', 'budget_transactions', 'budgets')

    def get_recent_transactions(self, obj):
        # Logic to fetch recent transactions for the user
        return TransactionSerializer(Transaction.objects.filter(user=obj).order_by('-date')[:5], many=True).data

    def get_budget_summary(self, obj):
        # Logic to calculate budget summary
        return BudgetSerializer(Budget.objects.filter(user=obj), many=True).data
    
    def get_budget_transactions(self, obj):
        budget_with_totals = Budget.objects.filter(user=obj).annotate(total_amount=Sum('transactions__amount'))
        return [{"total_amount": budget.total_amount, 'title': budget.title, 'amount': budget.amount} for budget in budget_with_totals]
    
    def get_budgets(self, obj):
        fields = ['id', 'title']
        return BudgetSerializer(Budget.objects.filter(user=obj), many=True, fields=fields).data