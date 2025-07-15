from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.shortcuts import render, redirect
#new add
import datetime

def convert_to_roman(number):
    if number == str (1):
        roman = 'I'
    elif number == str(2):
        roman = 'II'
    elif number == str(3):
        roman = 'III'
    elif number == str(4):
        roman = 'IV'
    elif number == str(5):
        roman = 'V'
    elif number == str(6):
        roman = 'VI'
    elif number == str(7):
        roman = 'VII'
    elif number == str(8):
        roman = 'VIII'
    elif number == str(9):
        roman = 'IX'
    elif number == str(10):
        roman = 'X'
    elif number == str(11):
        roman = 'XI'
    elif number == str(12):
        roman = 'XII'
    return roman

def convert_to_number(roman):
    if roman == 'I':
        number = int(1)
    elif roman == 'II':
        number = int(2)
    elif roman == 'III':
        number = int(3)
    elif roman == 'IV':
        number = int(4)
    elif roman == 'V':
        number = int(5)
    elif roman == 'VI':
        number = int(6)
    elif roman == 'VII':
        number = int(7)
    elif roman == 'VIII':
        number = int(8)
    elif roman == 'IX':
        number = int(9)
    elif roman == 'X':
        number = int(10)
    elif roman == 'XI':
        number = int(11)
    elif roman == 'XII':
        number = int(12)
    return number

# Create your models here.

class User(AbstractUser):
    is_waitress = models.BooleanField(default = False )
    is_cashier = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.username}, {self.first_name}, {self.last_name}'

class StatusModel(models.Model):
    status_choices = (
        ("Aktif","Aktif"),
        ("Tidak Aktif","Tidak Aktif")
    )
    status=models.CharField(max_length=15,choices=status_choices) 

    def __str__(self):
        return self.status

class Category(models.Model):
    status_choices = (
        ("Half Face","Half Face"),
        ("Full Face","Full Face"),
    )
    name=models.CharField(max_length=100)
    status=models.CharField(max_length=15,choices=status_choices)
    user_create= models.ForeignKey(User,related_name="user_create_category",blank=True,null=True,on_delete=models.SET_NULL)
    user_update= models.ForeignKey(User,related_name="user_update_category",blank=True,null=True,on_delete=models.SET_NULL)
    create_on = models.DateTimeField (auto_now_add=True)
    last_modified= models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
def increment_Layanan_code():
        last_code = Layanan.objects.all().order_by('id').last()
        if not last_code:
            return 'MN-0001'
        code = last_code.code
        code_int = int(code[3:7])
        new_code_int = code_int + 1
        return 'MN-' + str(new_code_int).zfill(4)
    
def increment_menu_resto_code():
    from .models import MenuResto
    last_code = MenuResto.objects.order_by('id').last()
    if not last_code:
        return 'MR001'
    code = last_code.code
    code_number = int(code.replace('MR', '')) + 1
    return 'MR{:03d}'.format(code_number)

class Layanan(models.Model):
    status_choices = (
        ("Laundry","Laundry"),
        ("Penitipan","Penitipan"),
    )
    #code = models.CharField(max_length=20,editable = False)
    name=models.CharField(max_length=100)
    price=models.FloatField(default=0.00)
    description=models.CharField(default="-")
    image_menu=models.ImageField(default='default_images/empt.jpg',upload_to="menu_images/",blank=True,null=True)
    category=models.ForeignKey(Category,related_name='category_menu',blank=True,null=True,on_delete=models.SET_NULL)
    status=models.ForeignKey(StatusModel,related_name="status_of_menu",blank=True,null=True,on_delete=models.SET_NULL)
    user_create= models.ForeignKey(User,related_name="user_create_layanan",blank=True,null=True,on_delete=models.SET_NULL)
    user_update= models.ForeignKey(User,related_name="user_update_layanan",blank=True,null=True,on_delete=models.SET_NULL)
    create_on = models.DateTimeField (auto_now_add=True)
    last_modified= models.DateField(auto_now=True)

    def __str__(self):
        return self.name
    
class JenisPembayaran(models.Model):
    status_choices = (
        ("Tunai","Tunai"),
        ("Debit","Debit"),
        ("Kredit","Kredit"),
        ("Transfer","Transfer")
    )
    status=models.CharField(max_length=15,choices=status_choices,default="Tunai")
    user_create= models.ForeignKey(User,related_name="user_create_jenis_pembayaran",blank=True,null=True,on_delete=models.SET_NULL)
    user_update= models.ForeignKey(User,related_name="user_update_jenis_pembayaran",blank=True,null=True,on_delete=models.SET_NULL)
    create_on = models.DateTimeField (auto_now_add=True)
    last_modified= models.DateField(auto_now=True)

    def __str__(self):
        return self.status

    
class Pembayaran(models.Model):
    status_choices = (
        ("Lunas", "Lunas"),
        ("Belum Lunas", "Belum Lunas"),
    )
    layanan = models.ForeignKey(Layanan, related_name="pembayaran", on_delete=models.CASCADE)
    total_bayar = models.FloatField(default=0.0)
    status = models.CharField(max_length=15, choices=status_choices, default="Belum Lunas")
    jenis_pembayaran = models.ForeignKey(JenisPembayaran, related_name="pembayaran", on_delete=models.CASCADE)
    user_create = models.ForeignKey(User, related_name="user_create_pembayaran", blank=True, null=True, on_delete=models.SET_NULL)
    user_update = models.ForeignKey(User, related_name="user_update_pembayaran", blank=True, null=True, on_delete=models.SET_NULL)
    create_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)  # Ganti ke DateTimeField

    def __str__(self):
        return self.status

def create_pembayaran(request):
    if request.method == 'POST':
        layanan_id = request.POST.get('layanan')
        jenis_pembayaran_id = request.POST.get('jenis_pembayaran')

        layanan = Layanan.objects.get(id=layanan_id)
        jenis_pembayaran = JenisPembayaran.objects.get(id=jenis_pembayaran_id)

        pembayaran = Pembayaran.objects.create(
            Layanan=layanan,
            total_bayar=layanan.price,
            status = "Belum Lunas",  # Default status
            Jenis_pembayaran=jenis_pembayaran,
            user_create=request.user,
            user_update=request.user,
        )

        return redirect('nama_url_sukses')
