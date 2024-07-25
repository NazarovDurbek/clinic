from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from users.models import CustomUser
# Create your models here.




class Cities(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    






class Hospital(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(max_length=200)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='hospatals_photo', null=True, blank=True)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("app:hospital_detail", args=[self.slug])
    




class HospitalCategory(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ManyToManyField(Hospital, related_name='hospital_category')

    def __str__(self):
        return self.name
    
class HospitalDepartments(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='DepartmentImage')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,  related_name='hospital_departments')

    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    experience = models.PositiveSmallIntegerField(default=0)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_doctor')
    specialty = models.ForeignKey(HospitalCategory, on_delete=models.CASCADE, related_name='hospital_doctor_category')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='doctor_photo', null=True, blank=True)
    languages = models.ManyToManyField(Language)
    salary = models.FloatField()
    visits = models.IntegerField(default=0)


    def __str__(self):
        return self.name    
    

    def get_absolute_url(self):
        return reverse("app:doctor_detail", args=[self.id])
    

class AvailableDays(models.Model):
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"

class TimeSlot(models.Model):
    available_slot = models.ForeignKey(AvailableDays, related_name='time_slots', on_delete=models.CASCADE)
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_time_slot')
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_time_slot', null=True, blank=True)
    type = models.CharField(max_length=10, choices=[('online', 'онлайн'), ('offline', 'оффлайн')], default='online')

    def __str__(self):
        return f"{self.time}"


    
class WorkSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_schedule')
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.doctor.name
    

class Product_Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Product(models.Model): 
    name = models.CharField(max_length=100) 
    price = models.FloatField(default=0) 
    product_counts = models.IntegerField(default=0)
    discount = models.FloatField(default=0) 
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, related_name='product_category')

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except IndexError:
                return "-"
        else:
            return None

    def dis_price(self):
        price = self.price - (self.price * self.discount / 100)
        return price



    @property
    def discounted_price(self):
        if self.discount > 0:
            discounted_price = self.price - (self.price * self.discount / 100)
            return '{0:.2f}'.format(discounted_price).rstrip('0').rstrip('.')
        return '{0:.2f}'.format(self.price).rstrip('0').rstrip('.')
        

    def get_absolute_url(self):
        return reverse("app:product_detail", args=[self.id])
    def __str__(self):
        return self.name 
    
class ProductDescription(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_description')
    name = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=50, choices=[('dc', 'Description'), ('ai', 'Additional Information')])
    

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images')

    def __str__(self) -> str:
        return f"{self.product.name}_{self.pk}"
    



class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)


    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def total_tax(self):
        total = self.total_sum()
        tax = total * 0.05
        return tax
    
    111111111111111111111111111111111111111

class Basket(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = BasketQuerySet.as_manager()
    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'


    def sum(self):
        return self.product.dis_price() * self.quantity
    



class Order(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    baskets = models.ManyToManyField(Basket)
    total_price = models.FloatField()
    created_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Отправлен','shipped'), ( 'Доставлен','delivered')], default='Отправлен')
    receiver_address = models.CharField(max_length=100)
    receiver_city = models.ForeignKey(Cities, on_delete=models.CASCADE, blank=True, null=True)
    receiver_name = models.CharField(max_length=50)
    receiver_phone = models.CharField(max_length=16)
    receiver_email = models.EmailField()
    receiver_surname = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)
    


    def __str__(self):
        return f'Заказ для {self.user.username} | Сумма: {self.total_price}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    phone = models.CharField(max_length=16)
    created_timestamp = models.DateTimeField(auto_now_add=True)




class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    tags = models.ManyToManyField(Tag, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except IndexError:
                return "-"
        else:
            return None

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.article.title}"
    
