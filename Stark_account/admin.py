from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class User_Admin(UserAdmin):
	UserAdmin.fieldsets[2][1]['fields'] = ('is_active', 'is_staff', 'is_acountants', 'is_suppurt', 'groups', 'user_permissions', 'avatar', 'phone', 'backup_email', 'user_code', 'stoke', 'payment_total', 'impression_total', 'robot_sub_total')
	list_display = ('id', 'user_code' ,'username', 'email', 'tag_avatar', 'is_staff', 'is_suppurt', 'is_acountants', 'stoke')

	search_fields = ['user_code', 'username']
	ordering = ['-id']

admin.site.register(User, User_Admin)
admin.site.site_header = _("پنل مدیریت استارک")
admin.site.unregister(Group)