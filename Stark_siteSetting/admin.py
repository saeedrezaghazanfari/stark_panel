from django.contrib import admin
from .models import (
	SettingVideo, SettingCategory, NotifyModel, Stark_Setting
)

class SettingVideoAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'poster', 'ext']
	search_fields = ['video', 'ext']
	ordering = ['-id']

class SettingCategoryAdmin(admin.ModelAdmin):
	list_display = ['days', 'price']
	search_fields = ['days', 'price']
	ordering = ['-id']

class NotifyModelAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'link', 'is_active', 'date']
	search_fields = ['__str__', 'link', 'is_active', 'date']
	ordering = ['-id']

class Stark_SettingModelAdmin(admin.ModelAdmin):
	list_display = ['wallet_addr', 'img_qrcode']
	search_fields = ['wallet_addr', 'img_qrcode']
	ordering = ['-id']

admin.site.register(SettingVideo, SettingVideoAdmin)
admin.site.register(SettingCategory, SettingCategoryAdmin)
admin.site.register(NotifyModel, NotifyModelAdmin)
admin.site.register(Stark_Setting, Stark_SettingModelAdmin)