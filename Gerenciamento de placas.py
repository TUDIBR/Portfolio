import random
import string
from color import color
from time import sleep
import datetime
import ast
import sys
# Variaveis
cores = ['vermelho', 'verde', 'amarelo', 'azul', 'lilas', 'ciano', 'cinza']
count = 0


# Função para criar placa
def placa():
    numero = str(random.randint(100, 999))
    letras = placa = ''
    
    for c in range(0, 3):
        letras += random.choice(string.ascii_letters).upper() # Sorteia as letras da placa
    placa = letras + '-' + numero # Junta as letras com o numero na variavel placa
    return placa

# Função para aplicar uma multa na placa
def multa(placa, multa):
    encontrado = False
    with open('placas.txt', 'r') as placa_2:
        ler = placa_2.read()
        placa_view = ast.literal_eval(ler)

    for v, c in enumerate(placa_view):
        if placa == c[0]:
            placa_view[v][1] += multa
            placa_view[v][2] += 1
            with open('placas.txt', 'w') as placa_3:
               placa_3.write(str(placa_view))
    



# Função para conseguir dados da placa
def consulta(placa):
    with open('placas.txt', 'r') as placa_2:
        ler = placa_2.read()
    placa_view = ast.literal_eval(ler)

    encontrado = False
    for v, c in enumerate(placa_view):
        if placa == c[0]:
            encontrado = True
            print(f'{color(texto='verde')}Placa: {placa}{color()}')
            print(f'{color(texto='azul')}Multa: R${c[1]}{color()}')
            print(f'{color(texto='lilas')}Multas: {placa_view[v][2]} {color()}')
    if encontrado == False:
        print(f'{color(texto='vermelho')}Placa não encontrada{color()}')

# Função para remover uma placa
def remove(placa):
    encontrou = False

    # Capturando a lista do banco de dados
    with open('placas.txt', 'r') as placa__:
        ler = placa__.read()
    lista_lida4 = ast.literal_eval(ler)

    for v, c in enumerate(lista_lida4):
        if placa == c[0]:
            encontrou = True
            lista_lida4.pop(v)
            print(f'{color(texto='vermelho')}Placa removida com sucesso!')
        with open('placas.txt', 'w') as placa_5:
            placa_5.write(str(lista_lida4))
            
            
        if encontrou == False:
            print(f'{color(texto='vermelho')}Placa não encontrada!{color()}')


# Program principal
try:
    while True:
        print('[ 1 ] Ver placas')
        print('[ 2 ] Consultar placa')
        print('[ 3 ] Criar placa')
        print('[ 4 ] Adicionar multa')
        print('[ 5 ] Remover placa')

            # Escolhendo opções
        try:    
            resp = int(input(f'{color(texto='amarelo')}Opção: {color()}'))
        except ValueError:
            print(f'{color(texto='vermelho')}Opção invalida! Tente novamente{color()}')
            continue
        # Ver todas placas

        if resp == 1:
            with open('placas.txt', 'r') as placaview:
                a = placaview.read()
                b = ast.literal_eval(a)
            print('~~~~ LISTA DE PLACAS ~~~~')
            for c in b:
                print(f'{color(fundo=cores[count], fonte='negrito')}{c}{color()}')
                count += 1
                if count >= 6:
                    count = 0
            print(f'{color()}~~~~~~~~~~~~~~~~~~~~~~~~~')
        elif resp == 2:
            placa_ = str(input('Placa: ')).upper().strip()
            consulta(placa_)
        # Criação da placa


        elif resp == 3:
            print('Criando placa aguarde...')
            sleep(1)
            while True:
                with open('placas.txt', 'r') as banco:
                    leitura2 = banco.read()   
                lista_lida2 = ast.literal_eval(leitura2)
                placa_criada = placa()
                if not placa_criada in lista_lida2:
                    break
            print(f'A placa escolhida foi: {color(texto='azul')}{placa_criada}{color()}')
            with open('placas.txt', 'r') as banco:
                leitura = banco.read()   
            lista_lida = ast.literal_eval(leitura)
            lista_lida.append([placa_criada, 0, 0])
            with open('placas.txt', 'w') as banco:
                banco.write(str(lista_lida))
        # Aplicar multa

        elif resp == 4:
            while True:
                try:
                    placa = str(input('Placa: ')).upper().strip()
                    multa_add = int(input('Multa: '))
                    multa(placa, multa_add)
                    break
                except:
                    print(f'{color(texto='vermelho')}Tente novamente!{color()}')
        # Remover placa

        elif resp == 5:
            resp2 = str(input('Placa: ')).upper().strip()
            remove(resp2)

except TypeError as erro:
    print(f'{color(texto='vermelho')}Ocorreu algum erro: {erro}{color()}')
