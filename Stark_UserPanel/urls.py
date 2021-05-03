
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import select_lang_redirect

urlpatterns = [
	path('captcha/', include('captcha.urls')),
    path('', select_lang_redirect),
]

urlpatterns += i18n_patterns(
	path('', include('Stark_account.urls')),
	path('', include('Stark_panel.urls')),
    path('stark/panel/administrator/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)