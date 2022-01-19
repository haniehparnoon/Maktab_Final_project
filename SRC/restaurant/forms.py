from .models import *
from django.forms import ModelForm
from django.db.models import Q

class FoodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Food
        fields = '__all__'

class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Category
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'status_id',
       
        ]

    def __init__(self, *args, **kwargs):
        #self_status_id = self.status_id
        status_sent = OrderStatus.objects.get(status = "sent")
        status_complete = OrderStatus.objects.get(status = "complete")
        super(OrderForm, self).__init__(*args, **kwargs)
        print("mmmmmmmmmmmmmmmmmmm",self.instance.status_id)
        print(type(self))
        if self.instance.status_id == status_complete:
            self.fields['status_id'].queryset = OrderStatus.objects.filter(Q(status  = "delivered")| Q(status ='sent'))
        if self.instance.status_id == status_sent:
            self.fields['status_id'].queryset = OrderStatus.objects.filter(status  = "delivered")