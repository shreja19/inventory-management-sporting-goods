from django.shortcuts import render, HttpResponse
from django.contrib import messages
from users.models import Products, Inventory, Category, Orders, PurchaseDetails
from django.db import connection

# Create your views here.

def AdminHome(request):
    return render(request, 'admins/AdminHome.html')


def admin_products(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        price_per_unit = request.POST.get('price_per_unit')
        discount_per_unit = request.POST.get('discount_per_unit')
        category_name = request.POST.get('category_name')
        query=f"INSERT INTO `products`(`product_name`, `product_description`, `price_per_unit`, `discount_per_unit`) VALUES('{product_name}', '{product_description}', '{price_per_unit}', '{discount_per_unit}')"
        cursor.execute(query)

        cursor.execute(f"select category_id from category where category_name='{category_name}'")
        cat_id = cursor.fetchone()
        cat_id = cat_id[0]

        cursor.execute(f"select max(product_id) from products")
        pid = cursor.fetchone()
        pid = pid[0]
        print(f"Category {cat_id} Product id {pid}")

        cursor.execute(f"INSERT INTO `inventory`(`product_id`, `units_in_stock`, `category_id`) VALUES('{pid}',10,'{cat_id}')")
        cursor.callproc(f"list_inventory_items")
        data1 = cursor.fetchall()
        ps_data= []
        columnNames = [column[0] for column in cursor.description]
        for record in data1:
            ps_data.append(dict(zip(columnNames, record)))

        return render(request, 'admins/admin_product.html', {'data': ps_data})
    else:
        cursor = connection.cursor()
        cursor.callproc(f"list_inventory_items")
        data2 = cursor.fetchall()
        ps_data = []
        columnNames = [column[0] for column in cursor.description]
        for record in data2:
            ps_data.append(dict(zip(columnNames, record)))
            #print(ps_data)
        return render(request, 'admins/admin_product.html', {'data': ps_data})
    return HttpResponse('Response working')


def AdminUpdateProducts(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        cursor = connection.cursor()
        cursor.callproc(f"get_products_by_pid",({int(id)}))
        data2 = cursor.fetchall()
        data = []
        columnNames = [column[0] for column in cursor.description]
        for record in data2:
            data.append(dict(zip(columnNames, record)))
            print(data)
    return render(request, 'admins/admin_product_update.html', {'data': data[0]})


def AdminDeleteProduct(request):
    cursor = connection.cursor()
    if request.method == 'GET':
        id = request.GET.get('id')
        id = int(id)

        cursor.execute(f"delete from products where product_id='{id}'")
        cursor.callproc(f"list_inventory_items")
        data2 = cursor.fetchall()
        ps_data = []
        columnNames = [column[0] for column in cursor.description]
        for record in data2:
            ps_data.append(dict(zip(columnNames, record)))

    return render(request, 'admins/admin_product.html', {'data': ps_data})


def admin_products_update(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        id = request.POST.get('id')
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        price_per_unit = float(request.POST.get('price_per_unit'))
        discount_per_unit = float(request.POST.get('discount_per_unit'))
        units_in_stock = int(request.POST.get('units_in_stock'))
        print(f'product_is:{id} Product Name {product_name}')

        cursor.execute(f"update products set product_name='{product_name}', product_description='{product_description}',price_per_unit='{float(price_per_unit)}', discount_per_unit='{float(discount_per_unit)}' where product_id='{int(id)}'")
        cursor.execute(f"update inventory set units_in_stock='{int(units_in_stock)}' where product_id='{int(id)}'")

        cursor.callproc(f"list_inventory_items")
        data2 = cursor.fetchall()
        ps_data = []
        columnNames = [column[0] for column in cursor.description]
        for record in data2:
            ps_data.append(dict(zip(columnNames, record)))

    return render(request, 'admins/admin_product.html', {'data': ps_data})


def admin_view_orders(request):

    cursor = connection.cursor()
    cursor.callproc(f"view_all_orders")
    data2 = cursor.fetchall()
    ps_data = []
    columnNames = [column[0] for column in cursor.description]
    for record in data2:
        ps_data.append(dict(zip(columnNames, record)))

    return render(request,'admins/admin_view_orders.html', {'data': ps_data})


def admin_view_purchase_items(request):
    order_id = request.GET.get("order_id")

    cursor = connection.cursor()
    cursor.callproc(f"list_purchased_items_in_order", ({int(order_id)}))
    data2 = cursor.fetchall()
    ps_data = []
    columnNames = [column[0] for column in cursor.description]
    for record in data2:
        ps_data.append(dict(zip(columnNames, record)))

    return render(request, 'admins/admin_purchase_list.html', {'data': ps_data})

