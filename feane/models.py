from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200 )
    slug = models.CharField(max_length=200,default=0.0 )
    limit = models.IntegerField(default = 0)

    def __str__(self):
        return self.title


class Posts(models.Model):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500 ,blank=True, null=True)
    description = models.TextField()
    post_image = models.ImageField(upload_to="images",null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE ,null=True)

    def __str__(self):
        return self.title
    

class Product_Category(models.Model): 
    name = 	models.CharField ( max_length =100 )

    def __str__(self):
        return self.name
    
 
class Product(models.Model):
    content_type=(
        ('burger','Burger'),
        ('pizza','Pizza'),
        ('pasta' ,'Pasta'),
        ('fries','Fries')
    ) 
    title = models.CharField( max_length=500)
    subtitle = models.CharField(max_length=500)
    description = models.TextField()
    product_category = models.ForeignKey(Product_Category,on_delete=models.CASCADE ,null=True)
    content_type = models.CharField(max_length=200,choices=content_type,default="")
    price = models.DecimalField(decimal_places=0, max_digits=8,)
    discounted_price = models.DecimalField(max_digits=5, decimal_places=0, default="0")
    offer_percentage = models.IntegerField(default=0)  # New field for offer in %
    product_image = models.ImageField( upload_to ='static/images' )

    def offer_price(self):
        discount = self.price * self.offer_percentage / 100
        return self.price - discount
    

class Book_table(models.Model):
    person_choice =[
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=10)
    email = models.EmailField()
    num_of_persons = models.PositiveIntegerField(choices=person_choice)
    date = models.DateField()

    def __str__(self):
        return self.name 
    

class ShippingDetails(models.Model):
    
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    
    
    def __str__(self):
        return f'Shipping Details {self.id} - {self.full_name}' 


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # UserID as Foreign Key
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_details = models.ForeignKey(ShippingDetails, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Order {self.id} by User {self.user.username} - Subtotal: ${self.subtotal}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")  # OrderID as Foreign Key
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # ProductID as Foreign Key
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of (product price * quantity)

    def __str__(self):
        return f'Item {self.product.title} (x{self.quantity}) for Order {self.order.id}'
 