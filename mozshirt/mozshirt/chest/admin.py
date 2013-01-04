from django.contrib import admin
from imagekit.admin import AdminThumbnail

from models import Shirt, ShirtShot

class ShirtShotAdmin(admin.ModelAdmin):
    model = ShirtShot
    list_display = ('id', 'shirt', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='thumbnail')

class ShirtAdmin(admin.ModelAdmin):
    model = Shirt

admin.site.register(ShirtShot, ShirtShotAdmin)
admin.site.register(Shirt, ShirtAdmin)
