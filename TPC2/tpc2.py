import sys
import re

def headers(linha):
    correspondencia = re.match(r" *#+ ",linha)
    if correspondencia is not None:
        carateres = correspondencia.end()
        linha_html = f"<h{carateres-1}>{linha[carateres:]}</h{carateres-1}>"
    else:
        linha_html = linha

    return linha_html

def inicio_fim_html(valor, texto):
    expressao = f"<{valor}>{texto}</{valor}>"
    return expressao

def bold(linha):
    return re.sub(r"\*\*(.+?)\*\*", lambda match:inicio_fim_html('b', match.group(1)),linha)

def italico(linha):
    return re.sub(r"\*(.+?)\*", lambda match:inicio_fim_html('i', match.group(1)),linha)

#def imagens(linha):
#    numero = len(re.findall(r"!\[",linha))
#    r = ""
#    if(numero == 0):
#        r = linha
#    else:
#        while(numero>0):
#
#            inicio, fim = re.search(r"!\[",linha).span()
#            r+=linha[:inicio]
#            linha = linha[fim:]
#
#            inicio, fim = re.search(r"\] *\(",linha).span()
#            texto_imagem = linha[:inicio]
#            linha = linha[fim:]
#
#            inicio, fim = re.search(r"\)",linha).span()
#            path_imagem = linha[:inicio]
#            linha = linha[fim:]
#
#            r+= "<img src=\""
#            r+= path_imagem
#            r+= "\" alt=\""
#            r+= texto_imagem
#            r+= "\"/>"
#            r+= linha
#
#            numero -= 1
#    return r

#def links (linha):
#    numero = len(re.findall(r"\[",linha))
#    r = ""
#    if(numero == 0):
#        r = linha
#    else:
#        while(numero>0):
#
#            inicio, fim = re.search(r"\[",linha).span()
#            r+=linha[:inicio]
#            linha = linha[fim:]
#
#            inicio, fim = re.search(r"\] *\(",linha).span()
#            texto = linha[:inicio]
#            linha = linha[fim:]
#
#            inicio, fim = re.search(r"\)",linha).span()
#            endereco_url = linha[:inicio]
#            linha = linha[fim:]
#
#            r+= "<a href=\""
#            r+= endereco_url
#            r+= "\">"
#            r+= texto
#            r+= "</a>"
#            r+= linha
#
#            numero -= 1
#    return r

def imagens(linha):
    return re.sub(r"!\[(.+?)\] *\((.+?)\)", lambda match: f"<img src=\"{match.group(2)}\" alt=\"{match.group(1)}\"/>",linha)

def links(linha):
    return re.sub(r"\[(.+?)\] *\((.+?)\)", lambda match: f"<a href=\"{match.group(2)}\">{match.group(1)}</a>",linha)

ordered_list = False

def listas(linha):
    global ordered_list
    correspondencia = re.match(r" *\d+\. ",linha)
    if correspondencia is not None:
        _, carateres = correspondencia.span()
        if ordered_list:
            linha_html = f"\t\t\t<li>{linha[carateres:]}</li>\n"
        else:
            ordered_list = True
            linha_html = f"\t\t<ol>\n\t\t\t<li>{linha[carateres:]}</li>\n"
    else:
        if ordered_list:
            ordered_list = False
            linha_html = "\t\t</ol>\n\t\t<p>" + linha + "</p>\n"
        else:
            linha_html = "\t\t<p>" + linha + "</p>\n"
    return linha_html


def main(input):
    f = open(input[1])
    html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{input[1]} convertido para html</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta charset="utf-8"/>
    </head>
    <body>
    """
    for linha in f:
        conteudo = linha.strip()    
        html += listas(links(imagens(italico(bold(headers(conteudo))))))
    f.close()

    html += """
    </body>
</html>
    """

    ficheiro_html = re.sub(r"\.md",".html",input[1],re.IGNORECASE)
    f2 = open(ficheiro_html,'w')
    f2.write(html)
    f2.close()

if __name__ == "__main__":
    main(sys.argv)