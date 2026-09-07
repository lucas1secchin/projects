#lucas secchin
import random

palavras_por_tamanho = {}
historico_tentativas = {}
numero_tentativas = 0

# Carrega as palavras do arquivo
with open("palavras_portugues.txt", "r") as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue

        partes = linha.split(";")
        if len(partes) < 2:
            continue

        palavra = partes[1]

        for tamanho in range(4, 11):
            if len(palavra) == tamanho:
                if tamanho not in palavras_por_tamanho:
                    palavras_por_tamanho[tamanho] = []
                palavras_por_tamanho[tamanho].append(palavra)

# Carrega os recordes
recordes = {}

try:
    with open("recordes.txt", "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip().split(",")
            tamanho = int(linha[0])
            recorde = int(linha[1])
            recordes[tamanho] = recorde

except FileNotFoundError:
    for tamanho in range(4, 11):
        recordes[tamanho] = 0


# Pergunta se deseja continuar jogo salvo
while True:
    continuar = input("Deseja continuar uma partida salva? (S/N): ").upper()

    if continuar == "S":

        try:
            with open("jogo_salvo.txt", "r") as arquivo:

                palavra_secreta = arquivo.readline().strip()
                tamanho_escolhido = int(arquivo.readline().strip())
                numero_tentativas = int(arquivo.readline().strip())

                for linha in arquivo:
                    linha = linha.rstrip("\n").split(",")

                    palavra_tentada = linha[0]

                    resultado = []

                    for simbolo in linha[1]:
                        resultado.append(simbolo)

                    historico_tentativas[palavra_tentada] = resultado

            print("Jogo carregado com sucesso.")

            break

        except FileNotFoundError:
            print("Nenhum jogo salvo foi encontrado.")
            continuar = "N"

    if continuar == "N":

        # Escolhe o tamanho da palavra
        while True:

            try:
                tamanho_escolhido = int(input(
                    "Digite o número de letras desejado (4-10) ou 0 para sortear: "
                ))

            except ValueError:
                print("Entrada inválida.")
                continue

            if tamanho_escolhido == 0:
                tamanho_escolhido = random.randint(4, 10)

            if tamanho_escolhido < 4 or tamanho_escolhido > 10:
                print("Número inválido. Digite um número entre 4 e 10.")
                continue

            palavra_secreta = random.choice(
                palavras_por_tamanho[tamanho_escolhido]
            )

            break

        break

    else:
        print("Digite apenas S ou N.")


# Jogo
while True:

    if numero_tentativas == 10:
        print("Você atingiu o número máximo de tentativas.")
        print(f"A palavra correta era: {palavra_secreta}")
        break


    # Mostra o histórico
    if len(historico_tentativas) > 0:
        print("\nHistórico:")

        for palavra_tentada in historico_tentativas:
            print(" ".join(palavra_tentada))
            print(" ".join(historico_tentativas[palavra_tentada]))


    # Escolhe entre tentar ou salvar
    acao = input(
        "\nDigite 'T' para tentar adivinhar a palavra ou 'S' para salvar o jogo: "
    ).upper()


    if acao == "S":

        with open("jogo_salvo.txt", "w") as arquivo:

            arquivo.write(f"{palavra_secreta}\n")
            arquivo.write(f"{tamanho_escolhido}\n")
            arquivo.write(f"{numero_tentativas}\n")

            for palavra_tentada in historico_tentativas:

                resultado = historico_tentativas[palavra_tentada]

                arquivo.write(f"{palavra_tentada},")

                for simbolo in resultado:
                    arquivo.write(simbolo)

                arquivo.write("\n")

        print("Jogo salvo com sucesso.")
        break


    elif acao == "T":

        tentativa_atual = input(
            f"Tentativa {numero_tentativas + 1}/10: "
        ).upper()


        # Verifica tamanho
        if len(tentativa_atual) != tamanho_escolhido:
            print(
                f"A palavra deve ter {tamanho_escolhido} letras."
            )
            continue


        # Verifica se a palavra existe
        if tentativa_atual not in palavras_por_tamanho[tamanho_escolhido]:
            print("Palavra não encontrada na lista.")
            continue


        # Verifica se já foi tentada
        if tentativa_atual in historico_tentativas:
            print("Você já tentou essa palavra.")
            continue


        resultado = []
        letras_disponiveis = []


        # Cria uma cópia da palavra secreta
        for i in range(len(palavra_secreta)):
            letras_disponiveis.append(palavra_secreta[i])


        # Verifica letras na posição correta
        for posicao in range(len(tentativa_atual)):

            if tentativa_atual[posicao] == palavra_secreta[posicao]:

                resultado.append("+")
                letras_disponiveis[posicao] = ""

            else:
                resultado.append(" ")


        # Verifica letras existentes em posição errada
        for posicao in range(len(tentativa_atual)):

            if resultado[posicao] != "+":

                if tentativa_atual[posicao] in letras_disponiveis:

                    resultado[posicao] = "-"
                    letras_disponiveis.remove(
                        tentativa_atual[posicao]
                    )


        # Salva tentativa no histórico
        historico_tentativas[tentativa_atual] = resultado

        numero_tentativas += 1


        # Mostra a tentativa atual
        print(" ".join(tentativa_atual))
        print(" ".join(resultado))


        # Verifica vitória
        if tentativa_atual == palavra_secreta:

            print("Parabéns! Você acertou a palavra!")

            # Verifica recorde
            if tamanho_escolhido not in recordes:
                recordes[tamanho_escolhido] = numero_tentativas

            elif recordes[tamanho_escolhido] == 0:
                recordes[tamanho_escolhido] = numero_tentativas

            elif numero_tentativas < recordes[tamanho_escolhido]:
                recordes[tamanho_escolhido] = numero_tentativas


            # Salva todos os recordes
            with open("recordes.txt", "w") as arquivo:

                for tamanho in range(4, 11):

                    if tamanho in recordes:
                        arquivo.write(
                            f"{tamanho},{recordes[tamanho]}\n"
                        )

                    else:
                        arquivo.write(f"{tamanho},0\n")


            print(
                f"Recorde para palavras de {tamanho_escolhido} letras: "
                f"{recordes[tamanho_escolhido]} tentativas."
            )

            break


    else:
        print("Opção inválida. Digite T ou S.")