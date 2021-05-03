from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StarkPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Stark_panel'
    verbose_name = _('ماژول توکن')
