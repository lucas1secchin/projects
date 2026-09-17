#lucas Secchin
from pathlib import Path
from datetime import datetime
agora = datetime.now().strftime("%Y-%m-%d_%H-%M")
contas={}
#---------------------------------------------------------------------------------
# 1
# verifica o caminho
#---------------------------------------------------------------------------------
while True:
    pasta=Path(input("Digite o caminho da pasta: "))
    if pasta.is_dir():
        arquivo_contas = pasta / "contas.txt"
        arquivo_movimentacoes = pasta / "moviment.txt"
        if arquivo_contas.is_file() and arquivo_movimentacoes.is_file():
            print("Arquivos encontrados.")
            break
        else: 
            print('Arquivos não encontrados')
    else:
        print("Caminho inválido. Tente novamente.")
#---------------------------------------------------------------------------------
# 2
# carregar arquivos_contas
#---------------------------------------------------------------------------------
with arquivo_contas.open('r') as arquivo:
    for linha in arquivo:
        lista=linha.strip().split(',')
        try:
            contas[lista[0]]={'nome':lista[1], 'saldo' : float(lista[2])}
        except:
            print(f'erro ao carregar a {linha.strip()}')
#---------------------------------------------------------------------------------
# 3
# carregar arquivos_movimentacoes
#---------------------------------------------------------------------------------
with arquivo_movimentacoes.open('r') as arquivo:
    for linha in arquivo:
        lista_m=linha.strip().split(',')
        try:
            if lista_m[0] in contas:
                if lista_m[1] == 'S':
                    contas[lista_m[0]]['saldo']-= float(lista_m[2])
                elif lista_m[1] == 'D':
                    contas[lista_m[0]]['saldo']+= float(lista_m[2])
        except: 
            print('error')
#---------------------------------------------------------------------------------
# 4
# salvar em contas 
#---------------------------------------------------------------------------------
with arquivo_contas.open('w') as arquivo:
    for i in contas:
        arquivo.write(f"{i},{contas[i]['nome']},{contas[i]['saldo']}\n")
#---------------------------------------------------------------------------------
# 5
# arquivo na pasta old
#---------------------------------------------------------------------------------
pasta_old = pasta / "OLD"
pasta_old.mkdir(exist_ok=True)

arquivo_movimentacoes.rename(pasta_old / f"{agora}-moviment.txt")