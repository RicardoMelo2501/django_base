#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
from pdfminer.high_level import extract_text

from django.shortcuts import render, redirect
from menu.models import Menu, SubMenu
from django.contrib import auth, messages

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='home:login')
def home(request):
    dataMenus = Menu.objects.all().order_by('id')
    dataSubMenus = SubMenu.objects.all()

    context = { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus,
        # 'form' : myForm
    }

    return render(request, 'home/index.html', context)

def default_page(request):
    dataMenus = Menu.objects.all()
    dataSubMenus = SubMenu.objects.all()

    context = { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus,
        # 'form' : myForm
    }

    return render(request, 'default_pages/index.html', context)