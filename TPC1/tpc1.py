import sys

def modalidades(infos):
    set_modalidades = set()
    for atleta in infos.values():
        set_modalidades.add(atleta[7])
    return sorted(set_modalidades)

def atletas_aptos(infos):
    aptos=0
    total=0
    for atleta in infos.values():
        total += 1
        if atleta[11]=="true":
            aptos += 1
    return aptos/total*100




def main(input):

    infos = {}

    f = open(input[1])
    f.readline()
    for linha in f:
        conteudo = linha.strip().split(',')
        infos[conteudo[0]] = conteudo[1:]
    f.close()

    #Lista ordenada alfabeticamente das modalidades;
    print("Modalidades existentes: ", modalidades(infos))

    #Percenteagem de atletas aptos e inaptos;
    aptos = atletas_aptos(infos)
    print("A percentagem de atletas aptos é de", aptos,"% e a percentagem de atletas inaptos é de",100 - aptos,"%")
    #Distribuição de atletas por escalão etário (intervalos de 5 anos).




if __name__ == "__main__":
    main(sys.argv)