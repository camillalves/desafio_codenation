import requests
import json
import string
import hashlib

#Requisitando
token = "1419b8976f74d4c867babe07ccf70fc5b6440d09"
r = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(token))

#Convertendo
dados = r.json()

#Criando o Arquivo
arquivo_json = open("answer.json", "w")

#Atulizando
json.dump(dados, arquivo_json)

#Descodificando
alfabeto = list(string.ascii_lowercase)
numero_casas = dados["numero_casas"]
decifrado = ""
for i in dados["cifrado"]:
    if i in alfabeto:
        for j in alfabeto:
            if j == i:
                posicao = alfabeto.index(j)
                nova_posicao = posicao - numero_casas
                nova_letra = alfabeto[nova_posicao]
                decifrado = decifrado + nova_letra
    else:
        decifrado = decifrado + i

#Atualizando - 'Decifrado'
dados["decifrado"] = decifrado
arquivo_json = open("answer.json", "w")
json.dump(dados, arquivo_json)


#Resumo Criptográfico
dados["resumo_criptografico"] = hashlib.sha1(decifrado.encode("utf-8")).hexdigest()

#Atualizando - 'Resumo Criptográfico'
arquivo_json = open("answer.json", "w")
json.dump(dados, arquivo_json)

arquivo_json.close()

#Enviando
answer = {"answer": open("answer.json","r")}
r = requests.post("https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}".format(token), files = answer)
print(r.text)
