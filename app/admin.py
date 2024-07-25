from django.contrib import admin
from .models import *
# Register your models here.




@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(HospitalCategory)
class HospitalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(HospitalDepartments)
class HospitalDepartmentsAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day_of_week', 'start_time', 'end_time']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product']

@admin.register(Product_Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('user', 'quantity', 'active', 'created_timestamp',)
    readonly_fields = ('created_timestamp',)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']

class AvailableTimeAdmin(admin.TabularInline):
    model = TimeSlot
    fields = ('time', 'doctor', 'is_booked', 'patient', 'type')
    extra = 0

@admin.register(AvailableDays)
class AvailableDaysAdmin(admin.ModelAdmin):
    list_display = ['date']
    inlines = (AvailableTimeAdmin,) 




class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('tags', 'created_at')

admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Image)