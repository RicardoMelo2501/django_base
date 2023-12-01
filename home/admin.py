# Register your models here.
from django.contrib import admin
from home.models import Contracheque, Recibo
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Funcionario
@admin.register(Contracheque)
class ContrachequeAdmin(admin.ModelAdmin):
    list_display = 'nome', 'data'
    
class FuncionarioInline(admin.StackedInline):
    model = Funcionario
    can_delete = False
    verbose_name_plural = 'Funcionario'

class CustomUserAdmin(UserAdmin):
    inlines = (FuncionarioInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)