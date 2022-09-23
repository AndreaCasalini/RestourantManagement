from datetime import date, datetime, timezone
from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from .models import Balance, Dish, Menu,Order,Table
# Create your views here.
NTABLE=10

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({},request))


def menu(request):
    menu=Dish.objects.all()
    template = loader.get_template('menu.html')
    context = {
        'menu': menu,
    }
    return HttpResponse(template.render(context,request))

#<a href="/restourant/order">Passa alla pagina degli ordini</a><br>

def table(request):
    template = loader.get_template('create_table.html')  
    print(request.method)  
    if request.method== 'POST':#POST
        table_id=request.POST['table_id']

        result=table_id.isdigit()
        if result is False:
            return HttpResponse(template.render({'error2':True},request))
        try:
            table=Table.objects.get(table_id=table_id)
        except Table.DoesNotExist:
            table_people=request.POST['table_people']
            result=table_people.isdigit()
            if result is False:
                return HttpResponse(template.render({'error2':True},request))
            if int(table_id) < 1 or int(table_id) > NTABLE:
                return HttpResponse(template.render({'error': True},request))
            if int(table_people) < 1:
                return HttpResponse(template.render({'error': True},request))
            context={
                'table_id':table_id,
                'table_people':table_people
            }
            table=Table.objects.create(table_id=table_id,table_people=table_people)
            table=Table.objects.get(table_id=table_id)
            dish=Dish.objects.get(dish_name='Coperto')
            table.save()
            i=0
            while i<int(table_people):
                i=i+1
                order=Order.objects.create(table=table,dish=dish)
                order.save()
            return HttpResponseRedirect('/restourant/order')
        return HttpResponse(template.render({'error1':True},request))
    else:#GET
        return HttpResponse(template.render({},request))
        
def modifyTable(request):
    template = loader.get_template('modify_table.html')  
    if request.method== 'POST':#POST
        table_id_old=request.POST['table_id_old']
        table=Table.objects.get(table_id=table_id_old)
        table_people_old=table.table_people
        table_id_new=request.POST['table_id_new']
        table_people_new=request.POST['table_people_new']

        try:
            table=Table.objects.get(table_id=table_id_old)
        except Table.DoesNotExist:
            return HttpResponse(template.render({'error':True},request))

        table=Table.objects.filter(table_id=table_id_old,table_people=table_people_old).update(table_id=table_id_new,table_people=table_people_new)
        table=Table.objects.get(table_id=table_id_new,table_people=table_people_new)
        diff_people=int(table_people_new)-int(table_people_old)
        print(diff_people)
        dish=Dish.objects.get(dish_name='Coperto')
        if diff_people > 0:
            i=0
            while i<abs(int(diff_people)):
                i=i+1
                order=Order.objects.create(table=table,dish=dish)
                order.save()
        elif diff_people < 0:
            i=0
            order=Order.objects.filter(table=table,dish=dish)
            for o in order:
                if i<abs(int(diff_people)):
                    i=i+1
                    o.delete()
                    #order.save()
        return HttpResponse(template.render({'modify':True},request))
    else: #GET
        return HttpResponse(template.render({},request))

def order(request):
    template = loader.get_template('order.html')
    order=Order.objects.all()
    return HttpResponse(template.render({'order':order},request))

def orderTable(request):
    template = loader.get_template('orderTable.html')
    list_appetizer=Dish.objects.filter(dish_category='appetizer')
    list_first=Dish.objects.filter(dish_category='first')
    list_second=Dish.objects.filter(dish_category='second')
    list_dessert=Dish.objects.filter(dish_category='dessert')

    context={
        'list_appetizer':list_appetizer,
        'list_first':list_first,
        'list_second':list_second,
        'list_dessert':list_dessert,

    }
    print(list_appetizer)
    if request.method== 'POST':#POST
        dish_name=request.POST['piatto']
        dish_quantity=request.POST['quantity']
        table_id=request.POST['table_id']
        try:
            table=Table.objects.get(table_id=table_id)
        except Table.DoesNotExist:
            context['error']=True
            return HttpResponse(template.render(context,request))
        try:
            dish=Dish.objects.get(dish_name=dish_name)
        except Dish.DoesNotExist:
            context['error']=True
            return HttpResponse(template.render(context,request))
        i=0
        while i<int(dish_quantity):
            i=i+1
            order=Order.objects.create(table=table,dish=dish)
            order.save()
        context['update']=True
        return HttpResponse(template.render(context,request))
    else:#GET
        return HttpResponse(template.render(context,request))


def receipt(request):
    template = loader.get_template('receipt.html')
    if request.method== 'POST':#POST
        table_id=request.POST['table_id']
        try:
            table=Table.objects.get(table_id=table_id)
        except Table.DoesNotExist:
            return HttpResponse(template.render({'error':True},request))
        order=Order.objects.filter(table_id=table_id)
        price=0
        for o in order:
            price=price+o.dish.dish_price
        #delete from db info of table and info about order of that table
        table=Table.objects.filter(table_id=table_id).delete()
        add_recap=Balance.objects.create(data=datetime.today().date(),price=price)
        #print(add_recap.data)
        return HttpResponse(template.render({'order':order,'price':price,'set':True},request))
    else:#GET
        return HttpResponse(template.render({},request))

def recap(request):
    template = loader.get_template('recap.html')
    list_receive=Balance.objects.all().order_by('data')
    total=0
    diz_day={}
    current=''
    for i in list_receive:
        total=total+i.price
        if i.data not in diz_day:
            diz_day[i.data]=0
    for i in diz_day:
        obj_day=Balance.objects.filter(data=i)
        for u in obj_day:
            diz_day[i]=diz_day[i]+u.price
    print(diz_day)
    print(list_receive)
    return HttpResponse(template.render({'recap':list_receive,'total':total,'diz_day':diz_day},request))

def kitchen(request):  
    
    template = loader.get_template('kitchen.html')
    list_order=Order.objects.all()
    list_dish=Dish.objects.all()
    list_table=Table.objects.all()
    context={
        'list_order':list_order,
        'list_dish':list_dish,
        'list_table':list_table
    }
    if request.method== 'POST':#POST
        table_id=request.POST['table_id']
        dish_name=request.POST['dish_name']
        dish=Dish.objects.get(dish_name=dish_name)

        try:
            obj=Order.objects.get(table_id=table_id,dish=dish)
        except Order.DoesNotExist:
            context['error']=True
            return HttpResponse(template.render(context,request))
        if obj.done==True:
            context['error1']=True
            return HttpResponse(template.render(context,request))
        obj.update(done=True)
        return HttpResponse(template.render(context,request))
    else:#get
        return HttpResponse(template.render(context,request))

