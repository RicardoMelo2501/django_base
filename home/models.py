# Create your models here.
from django.db import models
from django.conf import settings
from datetime import datetime    
from django.contrib.auth.models import User

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=5)

    def __str__(self):
        if self.user:
            return self.user.username
        return "no user related to this profile"
    
    # def __str__(self):
    #     return self.user.username

class Contracheque(models.Model):
    nome  = models.CharField('Nome', max_length=250)
    data = models.DateTimeField(default=datetime.now, null=False)
    arquivo = models.FileField(upload_to="contracheques")

    def __str__(self):
        return self.nome
    
class Recibo(models.Model):
    nome = models.CharField('nome', max_length=250)
    user = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    contracheque = models.ForeignKey(Contracheque, on_delete=models.DO_NOTHING, null=False, blank=False)
    arquivo = models.CharField('nome', max_length=150)

    def __str__(self):
        return self.nome