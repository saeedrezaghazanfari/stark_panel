from django.shortcuts import redirect

# perisan lang is defined default here
def select_lang_redirect(request):
    return redirect('/fa')