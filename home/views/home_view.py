from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
import re
import os
import shutil
import json
import base64

from django.conf import settings
from cryptography.fernet import Fernet
from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Menu, SubMenu
from home.models import Contracheque, Recibo, Funcionario
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def generate_key():
    return Fernet.generate_key()

def encrypt_string(plain_text, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(plain_text.encode())
    return base64.urlsafe_b64encode(cipher_text).rstrip(b'=')

def decrypt_string(cipher_text, key):
    cipher_suite = Fernet(key)
    cipher_text += b'=' * (4 - (len(cipher_text) % 4))  # Add padding if needed
    decrypted_text = cipher_suite.decrypt(base64.urlsafe_b64decode(cipher_text)).decode()
    return decrypted_text

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

def find_phrase_in_line(text, phrase):
    lines = text.split('\n')

    for line in lines:
        if re.search(phrase, line):
            return line

    return None


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
            # print(f'Diretório {os.path.dirname(destino)} criado.')
            # Tenta mover o arquivo novamente
            shutil.move(origem, destino)
            # print(f'Arquivo movido de {origem} para {destino}')
        else:
            print(f'Erro: O arquivo em {origem} não foi encontrado.')
    except PermissionError:
        print(f'Erro: Permissão negada ao tentar mover o arquivo.')

@login_required(login_url='home:login')
def consultar_contracheque(request):

    # Assuming you have a User model and Recibo model with a ForeignKey 'user'
    user = get_object_or_404(User, id=request.user.id)
    funcionario = get_object_or_404(Funcionario, user=user)

    # Filter receipts based on the user ID
    recibos_instance = Recibo.objects.filter(user=funcionario)

    context = { 
        'recibos': recibos_instance, 
    }

    return render(request, 'home/consultar_contracheque.html', context)


# Create your views here.
@login_required(login_url='home:login')
def home(request):
    dataMenus = Menu.objects.all().order_by('id')
    dataSubMenus = SubMenu.objects.all()

    context = { 
        'menus': dataMenus, 
        'sub_menus': dataSubMenus
    }

    return render(request, 'home/index.html', context)

def adicionar_contracheque(request):

    if request.method == 'POST':

        if request.FILES.get('contracheque'):

            Contracheque_instance = Contracheque(
                nome=request.POST.get('nome'),
                data=request.POST.get('data'),
                arquivo=request.FILES.get('contracheque'),
            )

            # Pega o Contra Cheque mais recente criado
            Contracheque_instance.save()

            # Pega o Contra Cheque mais recente criado
            ContrachequeMaisRecente = Contracheque.objects.latest('id')

            # Get the complete path to the media folder
            media_folder_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)
            # Analisando o conteúdo do contracheque inserido
            with open(media_folder_path + '/' + ContrachequeMaisRecente.arquivo.name, 'rb') as infile:
                reader = PdfReader(infile)
                page = 0
                writer = PdfWriter()
                total_pages = len(reader.pages)

                while page < total_pages:

                    writer.add_page(reader.pages[page])

                    with open(media_folder_path + "/recibos/output-{}.pdf".format(page), 'wb') as outfile:
                        writer.write(outfile)
                        writer = PdfWriter()

                    text = extract_text(media_folder_path + "/recibos/output-{}.pdf".format(page))

                    # Frase específica a ser procurada
                    target_phrase_func = "Código Nome do Funcionário"
                    target_phrase_date = "Mês"

                    nome_cod_func = find_next_line_after_phrase(text, target_phrase_func)
                    mes = find_phrase_in_line(text, target_phrase_date)[4:]

                    if nome_cod_func and mes:
                        # Desconsiderar os 5 primeiros números
                        texto_sem_espacos = nome_cod_func.strip().lower()
                        texto_sem_numeros = nome_cod_func.lower()[5:]
                        codigo_user = nome_cod_func[:5]

                        # Validando caso não tenha usuário/funcionário cadastrado
                        try:
                            Funcionario.objects.get(codigo=codigo_user)
                        except Funcionario.DoesNotExist:
                            # Dividir a string em palavras
                            palavras = texto_sem_numeros.split()

                            # Extrair o primeiro e último nome
                            primeiro_nome = palavras[0]
                            ultimo_nome = palavras[-1]

                            user_instance = User.objects.create_user(username=primeiro_nome + '.' + ultimo_nome, password='senha@123')
                            user_instance.save()

                            latest_user = User.objects.latest('id')
                            funcionario_instance = Funcionario(codigo=codigo_user, user=latest_user)
                            funcionario_instance.save()

                        funcionario_instance = Funcionario.objects.get(codigo=codigo_user)

                        alterar_nome(media_folder_path + "/recibos/output-{}.pdf".format(page), texto_sem_espacos + '.pdf')

                        # Example usage
                        key = generate_key()
                        plaintext = texto_sem_espacos

                        # Encrypt the string
                        encrypted_url = encrypt_string(plaintext, key)  

                        # Exemplo de uso
                        origem_arquivo = media_folder_path + '/recibos/{}.pdf'.format(texto_sem_espacos)
                        destino_arquivo = media_folder_path + '/recibos/{}/{}.pdf'.format(codigo_user, encrypted_url)
                        arquivo_url = '/media/recibos/{}/{}.pdf'.format(codigo_user, encrypted_url)

                        mover_arquivo(origem_arquivo, destino_arquivo)                                          

                        recibo = Recibo(nome='Recibo {}'.format(mes) , user=funcionario_instance, contracheque=ContrachequeMaisRecente,  arquivo=arquivo_url )
                        recibo.save()

                    else:
                        print("Frase não encontrada ou não há próxima linha após a frase.")

                    page+=1

            return render(request, 'home/consultar_contracheque.html')

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