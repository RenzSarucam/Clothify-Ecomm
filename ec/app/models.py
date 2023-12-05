from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PROVINCE_CHOICES = (
    ('Abra', 'Abra'), ('Agusan del Norte', 'Agusan del Norte'), ('Agusan del Sur', 'Agusan del Sur'),
    ('Aklan', 'Aklan'), ('Albay', 'Albay'), ('Antique', 'Antique'), ('Apayao', 'Apayao'), ('Aurora', 'Aurora'),
    ('Basilan', 'Basilan'), ('Bataan', 'Bataan'), ('Batanes', 'Batanes'), ('Batangas', 'Batangas'),
    ('Benguet', 'Benguet'), ('Biliran', 'Biliran'), ('Bohol', 'Bohol'), ('Bukidnon', 'Bukidnon'),
    ('Bulacan', 'Bulacan'), ('Cagayan', 'Cagayan'), ('Camarines Norte', 'Camarines Norte'),
    ('Camarines Sur', 'Camarines Sur'), ('Camiguin', 'Camiguin'), ('Capiz', 'Capiz'), ('Catanduanes', 'Catanduanes'),
    ('Cavite', 'Cavite'), ('Cebu', 'Cebu'), ('Compostela Valley', 'Compostela Valley'), ('Cotabato', 'Cotabato'),
    ('Davao del Norte', 'Davao del Norte'), ('Davao del Sur', 'Davao del Sur'), ('Davao Occidental', 'Davao Occidental'),
    ('Davao Oriental', 'Davao Oriental'), ('Dinagat Islands', 'Dinagat Islands'), ('Eastern Samar', 'Eastern Samar'),
    ('Guimaras', 'Guimaras'), ('Ifugao', 'Ifugao'), ('Ilocos Norte', 'Ilocos Norte'), ('Ilocos Sur', 'Ilocos Sur'),
    ('Iloilo', 'Iloilo'), ('Isabela', 'Isabela'), ('Kalinga', 'Kalinga'), ('La Union', 'La Union'), ('Laguna', 'Laguna'),
    ('Lanao del Norte', 'Lanao del Norte'), ('Lanao del Sur', 'Lanao del Sur'), ('Leyte', 'Leyte'),
    ('Maguindanao', 'Maguindanao'), ('Marinduque', 'Marinduque'), ('Masbate', 'Masbate'),
    ('Misamis Occidental', 'Misamis Occidental'), ('Misamis Oriental', 'Misamis Oriental'),
    ('Mountain Province', 'Mountain Province'), ('Negros Occidental', 'Negros Occidental'),
    ('Negros Oriental', 'Negros Oriental'), ('Northern Samar', 'Northern Samar'), ('Nueva Ecija', 'Nueva Ecija'),
    ('Nueva Vizcaya', 'Nueva Vizcaya'), ('Occidental Mindoro', 'Occidental Mindoro'),
    ('Oriental Mindoro', 'Oriental Mindoro'), ('Palawan', 'Palawan'), ('Pampanga', 'Pampanga'),
    ('Pangasinan', 'Pangasinan'), ('Quezon', 'Quezon'), ('Quirino', 'Quirino'), ('Rizal', 'Rizal'),
    ('Romblon', 'Romblon'), ('Samar', 'Samar'), ('Sarangani', 'Sarangani'), ('Siquijor', 'Siquijor'),
    ('Sorsogon', 'Sorsogon'), ('South Cotabato', 'South Cotabato'), ('Southern Leyte', 'Southern Leyte'),
    ('Sultan Kudarat', 'Sultan Kudarat'), ('Sulu', 'Sulu'), ('Surigao del Norte', 'Surigao del Norte'),
    ('Surigao del Sur', 'Surigao del Sur'), ('Tarlac', 'Tarlac'), ('Tawi-Tawi', 'Tawi-Tawi'), ('Zambales', 'Zambales'),
    ('Zamboanga del Norte', 'Zamboanga del Norte'), ('Zamboanga del Sur', 'Zamboanga del Sur'),
    ('Zamboanga Sibugay', 'Zamboanga Sibugay')
)

CATEGORY_CHOICES=(
    ('SL', 'Sleeves'),
    ('TS', 'Shirts'),
    ('SS', 'Shorts'),
    ('JT', 'Jackets'),
    
    
)

STATUS_CHOICES=(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
    
)

PAYMENT_CHOICES=(
     ('Cash on Delivery', 'Cash on Delivery'),
    ('Pick Up', 'Pick up'),
    
  
    
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)
     
     @property
     def total_cost(self):
         return self.quantity * self.product.discounted_price
     
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    amount = models.FloatField() 
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Pending')
    paid = models.BooleanField(default=False)
     

class OrderPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE),
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)
    product_image = models.ImageField(upload_to='product')
    # Assuming STATUS_CHOICES is defined somewhere
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
  

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

                              
    
    