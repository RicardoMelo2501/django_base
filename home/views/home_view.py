from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
import re
import os
import shutil
import json

from django.shortcuts import render, redirect
from menu.models import Menu, SubMenu
from home.models import Contracheque, Recibo, Funcionario
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Procurar a próxima linha após uma frase específica
def find_next_line_after_phrase(text, phrase):
    lines = text.split('\n')
    next_line = None
    found_phrase = False

    for line in lines:
        if found_phrase:
            next_line = line
            break
        if re.search(phrase, line):
            found_phrase = True

    return next_line


def alterar_nome(caminho_atual_value, novo_nome_value):
  # Especifica o caminho do arquivo atual e o novo nome desejado
  caminho_atual = caminho_atual_value
  novo_nome = novo_nome_value

  # Junta o caminho do arquivo atual com o novo nome
  novo_caminho = os.path.join(os.path.dirname(caminho_atual), novo_nome)

  # Renomeia o arquivo
  os.rename(caminho_atual, novo_caminho)

  print(f'O arquivo foi renomeado para {novo_nome}')

def mover_arquivo(origem, destino):
    try:
        # Move o arquivo da origem para o destino
        shutil.move(origem, destino)
        print(f'Arquivo movido de {origem} para {destino}')
    except FileNotFoundError:
        # Verifica se o diretório de destino existe
        if not os.path.exists(os.path.dirname(destino)):
            # Cria o diretório se não existir
            os.makedirs(os.path.dirname(destino))
            print(f'Diretório {os.path.dirname(destino)} criado.')
            # Tenta mover o arquivo novamente
            shutil.move(origem, destino)
            print(f'Arquivo movido de {origem} para {destino}')
        else:
            print(f'Erro: O arquivo em {origem} não foi encontrado.')
    except PermissionError:
        print(f'Erro: Permissão negada ao tentar mover o arquivo.')

# Create your views here.
@login_required(login_url='home:login')
def home(request):
    dataMenus = Menu.objects.all().order_by('id')
    dataSubMenus = SubMenu.objects.all()

    context = { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus,
        'user' : user
    }

    return render(request, 'home/index.html', context)

def adicionar_contracheque(request):

    if request.method == 'POST':

        if request.FILES.get('contracheque'):

            new_hobby = Contracheque(
                nome=request.POST.get('nome'),
                data=request.POST.get('data'),
                arquivo=request.FILES.get('contracheque'),
            )

            new_hobby.save()

            # Pega o Contra Cheque mais recente criado
            ContrachequeMaisRecente = Contracheque.objects.latest('id')

            # Analisando o conteúdo do contracheque inserido
            with open("media/" + ContrachequeMaisRecente.arquivo.name, 'rb') as infile:
                reader = PdfReader(infile)
                page = 0
                writer = PdfWriter()
                total_pages = len(reader.pages)

                while page < total_pages:

                    writer.add_page(reader.pages[page])

                    with open("media/recibos/output-{}.pdf".format(page), 'wb') as outfile:
                        writer.write(outfile)
                        writer = PdfWriter()

                    text = extract_text("media/recibos/output-{}.pdf".format(page))

                    # Frase específica a ser procurada
                    target_phrase = "Código Nome do Funcionário"

                    next_line = find_next_line_after_phrase(text, target_phrase)

                    if next_line:
                        alterar_nome("media/recibos/output-{}.pdf".format(page), next_line.strip() + '.pdf')

                        # Exemplo de uso
                        origem_arquivo = 'media/recibos/{}.pdf'.format(next_line.strip())
                        destino_arquivo = 'media/recibos/1111/{}.pdf'.format(next_line.strip())

                        mover_arquivo(origem_arquivo, destino_arquivo)

                        funcionario = Funcionario.objects.get(codigo=111)
                        User = User.objects.get(id=funcionario.user_id)

                        recibo = Recibo(nome='Mês de Janeiro', user=User, contracheque=ContrachequeMaisRecente,  arquivo='media/recibos/1111/{}.pdf'.format(next_line.strip()) )
                    else:
                        print("Frase não encontrada ou não há próxima linha após a frase.")

                    page+=1

            return render(request, 'home/adicionar_contracheque.html', {'recibo' : new_hobby })

        else :
            return render(request, 'home/adicionar_contracheque.html')

    return render(request, 'home/adicionar_contracheque.html')

def default_page(request):
    dataMenus = Menu.objects.all()
    dataSubMenus = SubMenu.objects.all()

    context = { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus,
        # 'form' : myForm
    }

    return render(request, 'default_pages/index.html', context)