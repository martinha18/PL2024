import sys
import re

def main(input):
    f = open(input[1])
    texto = f.read()
    f.close()

    divisao = re.split(r"(on|off|=)", texto, flags=re.I)

    counter = 0
    i=0
    state = True

    size = len(divisao)

    while (i < size):
        if (re.fullmatch(r"on", divisao[i], flags=re.I)):
            state = True
        elif (re.fullmatch(r"off", divisao[i], flags=re.I)):
            state = False
        elif (re.fullmatch(r"=", divisao[i])):
            print(counter)
        else:
            if state:
                counter += sum(map(int,re.findall(r"\d+", divisao[i])))
        i += 1
    
    print(f"A soma total é: {counter}")
            
            


if __name__ == "__main__":
    main(sys.argv)