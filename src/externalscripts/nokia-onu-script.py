#!/usr/bin/python3

import subprocess
import re
import json

#########################################
#                                       #
# Author: Samuel Sampaio                #
# Email: samukasampaio@hotmail.com      #
# versão: v1.0                          #
#########################################

# Função para executar o comando snmpwalk e retornar a saída
def run_snmpwalk(community, ip, oid):
    command = ["snmpwalk", "-v2c", "-c", community, ip, oid]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

# Função para extrair as informações do comando snmpwalk e criar o JSON
def parse_snmp_results(ifdescr_output, ifoperstatus_output):
    # Dicionário para armazenar informações de cada PON
    pon_info = {}

    # Extrair informações de ifdescr_output
    for line in ifdescr_output.split('\n'):
        match = re.match(r'.*\.(\d+) = STRING: "(.*)"', line)
        if match:
            ifindex = match.group(1)
            ifdescr = match.group(2)
            pon_info[ifindex] = {'IFDESCR': ifdescr, 'ONU_Count': 0, 'ONU_Active': 0, 'ONU_Inactive': 0}

    # Extrair informações de ifoperstatus_output
    for line in ifoperstatus_output.split('\n'):
        match = re.match(r'.*\.(\d+)\.(\d+) = INTEGER: (\d+)', line)
        if match:
            ifindex = match.group(1)
            status = int(match.group(3))
            if ifindex in pon_info:
                pon_info[ifindex]['ONU_Count'] += 1
                if status == 1:
                    pon_info[ifindex]['ONU_Active'] += 1
                else:
                    pon_info[ifindex]['ONU_Inactive'] += 1

    # Calcular total
    total_info = {'IFDESCR': 'total', 'ONU_Count': 0, 'ONU_Active': 0, 'ONU_Inactive': 0}
    for info in pon_info.values():
        total_info['ONU_Count'] += info['ONU_Count']
        total_info['ONU_Active'] += info['ONU_Active']
        total_info['ONU_Inactive'] += info['ONU_Inactive']

    # Adicionar total ao dicionário de PONs
    pon_info['total'] = total_info

    # Remover PONs com ONU_Count zerado
    pon_info = {key: value for key, value in pon_info.items() if value['ONU_Count'] > 0}

    return list(pon_info.values())

# Configurações
community = "now-snmp"
ip = "10.3.2.132"

# Executar snmpwalk para IFDESCR e IFOPERSTATUS
ifdescr_output = run_snmpwalk(community, ip, "1.3.6.1.4.1.637.61.1.35.11.2.1.19")
ifoperstatus_output = run_snmpwalk(community, ip, "1.3.6.1.4.1.637.61.1.35.11.4.1.5")

# Processar os resultados e criar o JSON
pon_info = parse_snmp_results(ifdescr_output, ifoperstatus_output)

# Imprimir o JSON resultante
print(json.dumps(pon_info, indent=4))
