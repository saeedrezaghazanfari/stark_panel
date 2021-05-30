from django.contrib import admin
from .models import (
	SettingVideo, SettingCategory, NotifyModel
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

admin.site.register(SettingVideo, SettingVideoAdmin)
admin.site.register(SettingCategory, SettingCategoryAdmin)
admin.site.register(NotifyModel, NotifyModelAdmin)