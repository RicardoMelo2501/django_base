from menu.models import Menu, SubMenu

# Adicionado os valores de Menu e Submenu como context padrões
def default_context_values(request):
    dataMenus = Menu.objects.all().order_by('id')
    dataSubMenus = SubMenu.objects.all()
    
    return { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus,
    }