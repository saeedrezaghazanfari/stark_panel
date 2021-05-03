from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StarkSitesettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Stark_siteSetting'
    verbose_name = _('تنظیمات وبسایت')
