from django import template
from django.utils.translation import get_language
from Stark_panel.models import Ticket
from Stark_siteSetting.models import NotifyModel
register = template.Library()

@register.simple_tag
def get_counter_suppurt():
    objs_counter = Ticket.objects.filter(is_suppurt=False, is_seen=False).all().count()
    if objs_counter:
        return objs_counter
    return 0

@register.simple_tag
def get_unread_tickets_counter(id):
    objs_counter = Ticket.objects.filter(user__id=id, is_seen_user=False, is_suppurt=True).order_by('-id').count()
    if objs_counter:
        return objs_counter
    return 0

@register.simple_tag
def get_ticket(id):
    objs = Ticket.objects.filter(user__id=id, is_seen_user=False, is_suppurt=True).order_by('-id')
    if objs:
        a = []
        if get_language() == 'fa':
            for i in objs:
                a.append({
                    'title': i.title, 
                    'subject': i.subject, 
                    'date': i.j_date 
                })
        else:
            for i in objs:
                a.append({
                    'title': i.title, 
                    'subject': i.subject, 
                    'date': i.date 
                })
        return a
    else:
        return None

@register.simple_tag
def get_notify():
    objs = NotifyModel.objects.filter(is_active=True).order_by('-id')
    if objs:
        a = []
        if get_language() == 'fa':
            for i in objs:
                a.append({
                    'title_fa': i.title_fa,
                    'title_en': i.title_en,
                    'title_ar': i.title_ar,
                    'message_fa': i.message_fa,
                    'message_en': i.message_en,
                    'message_ar': i.message_ar,
                    'link': i.link,
                    'date': i.j_date,
                })
        else:
            for i in objs:
                a.append({
                    'title_fa': i.title_fa,
                    'title_en': i.title_en,
                    'title_ar': i.title_ar,
                    'message_fa': i.message_fa,
                    'message_en': i.message_en,
                    'message_ar': i.message_ar,
                    'link': i.link,
                    'date': i.date,
                })
        return a
    else:
        return None

@register.simple_tag
def get_last_string(dataStr):
    return dataStr[-5:]