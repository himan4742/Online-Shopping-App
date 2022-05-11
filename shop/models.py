from datetime import datetime

from django.db import models


class Category(models.Model):
    """."""

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    """."""

    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=250, null=True , blank=True)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    def __str__(self):
        """."""

        return self.name

    @staticmethod
    def get_all_products():
        """Get a list of all products"""

        return Product.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        """Get a list of all products in same category"""

        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Customer(models.Model):
    """."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        """."""

        return self.first_name

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True

        return False


class Order(models.Model):
    """."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=250, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

    objects = models.Manager()

