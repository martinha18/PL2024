import sys

def modalidades(infos):
    set_modalidades = set()
    for atleta in infos.values():
        set_modalidades.add(atleta[7])
    return sorted(set_modalidades)

def atletas_aptos(infos, atletas):
    aptos=0
    for atleta in infos.values():
        if atleta[11]=="true":
            aptos += 1
    return aptos/atletas*100

def distribuicao_etaria(infos):
    distribuicao = {}
    for atleta in infos.values():
        idade = int(atleta[4])
        escalao = idade // 5
        if escalao in distribuicao.keys():
            distribuicao[escalao] += 1
        else:
            distribuicao[escalao] = 1
    return distribuicao



def main(input):

    infos = {}
    atletas = 0

    f = open(input[1])
    f.readline()
    for linha in f:
        atletas += 1
        conteudo = linha.strip().split(',')
        infos[conteudo[0]] = conteudo[1:]
    f.close()

    #Lista ordenada alfabeticamente das modalidades;
    print(f"Modalidades existentes: {modalidades(infos)}\n")

    #Percenteagem de atletas aptos e inaptos;
    aptos = atletas_aptos(infos, atletas)
    print(f"Percentagem de atletas aptos: {aptos}%\nPercentagem de atletas inaptos: {100 - aptos}%\n")
    
    #Distribuição de atletas por escalão etário (intervalos de 5 anos).
    print("Distribuição por escalão etário")
    distribuicao = distribuicao_etaria(infos)
    for i in range(30):
        if i in distribuicao.keys():
            print (f"[{i*5},{i*5+4}] -> {distribuicao[i]} -> {round(distribuicao[i]/atletas*100,3)}%")


if __name__ == "__main__":
    main(sys.argv)