from django.contrib import admin
from pos_app.models import User,JenisPembayaran,Layanan,StatusModel,Category,Pembayaran

admin.site.register(User)
admin.site.register(JenisPembayaran)
admin.site.register(Layanan)
admin.site.register(StatusModel)
admin.site.register(Category)
admin.site.register(Pembayaran)

# Register your models here.
