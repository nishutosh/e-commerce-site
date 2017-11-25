import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [ 'Order_Date_Time','id','Order_Customer__User_customer__username']



        
