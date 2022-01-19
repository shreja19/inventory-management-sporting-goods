from django.shortcuts import render, HttpResponse, redirect
from .forms import UserSignupForm
from django.contrib import messages
from .models import UserSignupModel

from .models import Customer, Login, UsertypeDetails, Inventory, Products, Orders, PurchaseDetails,Category, CartDetails_Model
#from admins.models import ProductsModel
from datetime import datetime
from django.db import connection


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        cursor = connection.cursor()
        query = f"INSERT INTO `customer` (`fname`,`lname`,`city`,`zip`,`email`,`phone`)VALUES ('{fname}','{lname}','{city}','{zip}','{email}','{phone}')"
        cursor.execute(query)

        cursor.execute(f"select max(customer_id) from customer")
        cust_id = cursor.fetchone()
        cust_id = cust_id[0]
        cursor.execute(f"INSERT INTO `login`(`username`,`cid`,`usertype_id`,`password`)VALUES('{username}','{cust_id}',1112,'{password}')")
        messages.success(request, 'You have been successfully registered')
        form = UserSignupForm()
        return render(request, 'registrn.html', {'form': form})

    else:
        form = UserSignupForm()
    return render(request, 'registrn.html', {'form': form})


def UserLoginCheck(request):
    cursor = connection.cursor()
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            cursor.callproc(f"verify_login_credentials",({loginid}, {pswd}))
            data2 = cursor.fetchall()
            ps_data = []
            columnNames = [column[0] for column in cursor.description]
            for record in data2:
                ps_data.append(dict(zip(columnNames, record)))
                print(ps_data)
                user_type = ps_data[0].get('usertype_value')
                username=ps_data[0].get('username')
                cid=ps_data[0].get('cid')

            request.session['username'] = username
            request.session['cid'] = cid

            if user_type == 'customer':
                return render(request, 'users/UserHome.html', )
            elif user_type == 'admin':
                return render(request, 'admins/AdminHome.html', )
            else:
                 messages.success(request, 'Invalid Login id and password')
                 return render(request, 'login.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'login.html', {})


def UserHome(request):
    cust_id = request.session['username']
    return render(request, 'users/UserHome.html')


def user_search_by_category(request):
    if request.method == 'POST':
        cat_name = request.POST.get('category_name')

        cursor = connection.cursor()
        cursor.callproc(f"search_products_by_category", ({cat_name}))

        data = cursor.fetchall()
        print(data)
        ps_data = []
        columnNames = [column[0] for column in cursor.description]
        for record in data:
            ps_data.append(dict(zip(columnNames, record)))
        print(ps_data)

        return render(request, 'users/user_search_by_category.html', {'data': ps_data})
    else:
        return render(request, 'users/user_search_by_category.html')


def user_add_cart(request):
    cursor = connection.cursor()
    if request.method == 'GET':
        product_id = request.GET.get('id')
        username = request.session['username']
        cust_id = request.session['cid']
        customer = Customer.objects.get(customer_id=cust_id)
        print(product_id)
        products = Products.objects.get(product_id=product_id)

        price = products.price_per_unit
        product_name = products.product_name
        discount = products.discount_per_unit
        cid = str(customer.customer_id)
        pid = str(product_id)

        query = f"INSERT INTO `cart_details`(`purchase_state`, `product_id`, `customer_id`) VALUES('waiting','{pid}' ,'{cid}')"

        cursor.execute(query)

        messages.success(request, 'Your products have been added to the cart successfully!..')
    return render(request, 'users/user_search_by_category.html')


def check_cart_count(id):
    cursor = connection.cursor()
    cursor.execute(f"select count(*) from cart_details where customer_id={int(id)} and purchase_state='waiting'")
    cartin = cursor.fetchall()
    return cartin[0]


def userCheckCartData(request):
    user_id = request.GET.get('cust_id')

    cursor = connection.cursor()
    cursor.execute(f"SELECT c.cart_id, p.product_name, p.price_per_unit,p.discount_per_unit FROM products p natural join cart_details c  where c.purchase_state='waiting' and c.customer_id={int(user_id)}")
    records = cursor.fetchall()

    cart = []
    columnnames = [column[0] for column in cursor.description]

    for record in records:
        cart.append(dict(zip(columnnames, record)))

    total = calculate_total_payble_amount(user_id)

    cartin = check_cart_count(user_id)
    print(total,':',cartin)

    return render(request, "users/check_cart_data.html", {'data': cart, 'total': total, 'count': cartin[0]})


def calculate_total_payble_amount(user_id):

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM cart_details where customer_id={int(user_id)} and purchase_state='waiting'")
    cart = cursor.fetchall()
    total = 0.0

    for pid in cart:
        p = pid[2]
        products = Products.objects.get(product_id=p)
        print(
            f'Customer ID: {user_id} Product ID: {products.product_id} Product Name {products.product_name} Price ${products.price_per_unit} Discount ${products.discount_per_unit}')
        price = products.price_per_unit
        discount = products.discount_per_unit
        cost = price - discount
        total += float(cost)

    return round(total, 2)


def update_customer_cart(id):
    CartDetails_Model.objects.filter(cart_id=id).update(purchase_state='purchased')


def user_check_out(request):
    user_id = request.GET.get('cust_id')

    cursor = connection.cursor()
    cursor.execute(f"select * from cart_details where customer_id={int(user_id)} and purchase_state='waiting'")
    data = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in data:
        insertObject.append(dict(zip(columnNames, record)))


    o_date=datetime.now()
    cid = str(user_id)
    cursor.execute(f"INSERT INTO `orders` (`order_date`,`customer_id`,`payment_type`,`order_status`)VALUES('{o_date}','{cid}','credit card','success')")

    for inv in insertObject:
        customer_id = inv['customer_id']
        product_id = inv['product_id']
        purchase_state = inv['purchase_state']

        prod = Products.objects.get(product_id=product_id)
        price = prod.price_per_unit
        discount = prod.discount_per_unit
        price=price-discount

        cursor.execute(f"select max(order_id) from orders")
        oid = cursor.fetchone()
        oid = oid[0]
        order_id=str(oid)

        cursor.execute(f"INSERT INTO `purchase_details`(`order_id`,`product_id`,`units_on_order`,`total_bill_amount`,`discount_applied`)VALUES('{order_id}','{product_id}',1,'{price}','{discount}')")

        update_customer_cart(inv['cart_id'])

    messages.success(request, 'Your order has been placed successfully!..')
    return render(request, 'users/check_cart_data.html')


def user_order_details(request):

    cid = request.session['cid']
    print(cid)
    cursor = connection.cursor()
    cursor.callproc(f"list_all_orders_by_customer", ({int(cid)}))
    data2 = cursor.fetchall()
    ps_data = []
    columnNames = [column[0] for column in cursor.description]
    for record in data2:
        ps_data.append(dict(zip(columnNames, record)))

    return render(request, 'users/user_orders.html', {"data": ps_data})


def get_purchase_list(request):
    order_id = request.GET.get('order_id')
    cursor = connection.cursor()
    cursor.callproc(f"list_purchased_items_in_order", ({int(order_id)}))
    data2 = cursor.fetchall()
    ps_data = []
    columnNames = [column[0] for column in cursor.description]
    for record in data2:
        ps_data.append(dict(zip(columnNames, record)))


    return render(request, 'users/purchase_details.html', {"data": ps_data})



