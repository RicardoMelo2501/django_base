# Create your models here.
from django.db import models
from django.conf import settings
from datetime import datetime    

class Contracheque(models.Model):
    nome  = models.CharField('Nome', max_length=250)
    data = models.DateTimeField(default=datetime.now, null=False)
    arquivo = models.FileField(upload_to="contracheques")

    def __str__(self):
        return self.nome
    
class Recibo(models.Model):
    data = models.CharField('nome', max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contracheque = models.ForeignKey(Contracheque, on_delete=models.DO_NOTHING, null=False, blank=False)
    arquivo = models.FileField()

    def __str__(self):
        return self.nome