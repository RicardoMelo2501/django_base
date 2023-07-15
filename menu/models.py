from django.db import models

# Create your models here.
class Menu(models.Model):
    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
    
    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    font_awesome_icon = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class SubMenu(models.Model):
    class Meta:
        verbose_name = 'Sub Menu'
        verbose_name_plural = 'Sub Menus'
    
    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    font_awesome_icon = models.CharField(max_length=2048)
    parent_menu = models.ForeignKey('Menu', on_delete=models.DO_NOTHING, null=False, blank=False)
    new_tab = models.BooleanField(default=False)

    def __str__(self):
        return self.text

def case_upload_location(instance, filename):
    case_name = instance.name_id
    file_name = filename.lower().replace(" ", "-")
    return "licitacoes/{}/{}".format(case_name, file_name)

class Case(models.Model):
    # datos del caso
    name = models.CharField('Nombre', max_length=250)
    observations = models.TextField('Observaciones', null = True, blank = True)
    number_folder = models.CharField('Numero de Carpeta', max_length=250)

class CaseFile(models.Model):
    name = models.ForeignKey(Case, on_delete=models.CASCADE) # When a Case is deleted, upload models are also deleted
    file = models.FileField(upload_to=case_upload_location, null = True, blank = True)