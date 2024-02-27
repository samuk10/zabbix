#!/usr/bin/python3
#########################################
#                                       #
# Author: Samuel Sampaio                #
# Email: samukasampaio@hotmail.com      #
# versão: v1.0                          #
#########################################

import subprocess
import re
import json
import sys


host_ip= sys.argv[1]
community= sys.argv[2]

# Função para executar o snmpwalk e retornar as linhas de saída
def execute_snmpwalk():
    command = f'snmpwalk -v2c -c {community} {host_ip} .1.3.6.1.4.1.6527.3.1.2.33.1.17.1.3'
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return []

# Executar o snmpwalk e capturar as linhas de saída
lines = execute_snmpwalk()

# Extrair os valores entre o primeiro "|" e o primeiro "."
values = []
for line in lines:
    match = re.search(r'\|([^\.]+)', line)
    if match:
        value = match.group(1).strip()
        values.append(value)

# Contar as ocorrências de cada valor
count_dict = {}
for value in values:
    if value not in count_dict:
        count_dict[value] = 1
    else:
        count_dict[value] += 1

# Preparar o resultado no formato JSON desejado
result = [{"IF_NAME": name, "IF_COUNT": count} for name, count in count_dict.items()]

# Imprimir o resultado
print(json.dumps(result, indent=4))
