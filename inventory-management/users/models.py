from django.db import models

# Create your models here.
class UserSignupModel(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    zip = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=100)
    mobile = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'signup'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'category'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    city = models.CharField(max_length=80)
    zip = models.CharField(max_length=6)
    email = models.CharField(max_length=60)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return '' + self.customer_id

    class Meta:
        managed = False
        db_table = 'customer'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.CharField(max_length=200)
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)
    discount_per_unit = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Inventory(models.Model):
    product = models.ForeignKey(Products, models.DO_NOTHING, primary_key=True)
    units_in_stock = models.IntegerField()
    category = models.ForeignKey(Category, models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'inventory'


class UsertypeDetails(models.Model):
    usertype_id = models.AutoField(primary_key=True)
    usertype_value = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'usertype_details'


class Login(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    cid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cid')
    usertype = models.ForeignKey(UsertypeDetails, models.DO_NOTHING)
    password = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'login'


class Customer_cart_Model(models.Model):
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    username = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField()
    quantity = models.IntegerField()
    purchase_state = models.CharField(max_length=100, default='waiting')
    c_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "" + self.customer_id

    class Meta:
        managed = False
        db_table = 'customerscart'


class CartDetails_Model(models.Model):
    cart_id = models.AutoField(primary_key=True, max_length=30)
    purchase_state = models.CharField(max_length=100, default='waiting')
    product_id = models.ForeignKey(Products, models.DO_NOTHING)
    customer_id = models.ForeignKey(Customer, models.DO_NOTHING)

    def __str__(self):
        return "" + self.customer_id

    class Meta:
        managed = False
        db_table = 'cart_details'

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField()
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    payment_type = models.CharField(max_length=25)
    order_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'orders'


class PurchaseDetails(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    units_on_order = models.IntegerField()
    total_bill_amount = models.DecimalField(max_digits=9, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'purchase_details'
