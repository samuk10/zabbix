#!/usr/bin/python3

from collections import defaultdict
import subprocess
import re
import json
import sys

host_ip= sys.argv[1]
community= sys.argv[2]

# Value mapping
value_mapping = {
    0: 'invalid',
    1: 'inactive',
    2: 'activatePending',
    3: 'active',
    4: 'deactivatePending',
    5: 'disablePending',
    6: 'disabled'
}

# Função para executar o snmpwalk e retornar as linhas de saída
def execute_snmpwalk():
    command = f'snmpwalk -v2c -c {community} {host_ip} .1.3.6.1.4.1.6771.10.1.5.1.5'
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return []

# Executar o snmpwalk e capturar as linhas de saída
snmp_data = execute_snmpwalk()

# Parse snmp data
pon_data = defaultdict(lambda: defaultdict(int))

for line in snmp_data:
    if line.strip():
        match = re.match(r'.*\.(\d+)\.(\d+)\.(\d+) = INTEGER: (\d+)', line)
        if match:
            slot, pon, pos, value = map(int, match.groups())
            pon_data[f"gpon{slot}/{pon}"][value_mapping[value]] += 1

# Aggregate data
total_data = defaultdict(int)
for pon, data in pon_data.items():
    total_data['ONU_Count'] += sum(data.values())
    total_data['ONU_Active'] += data['active']
    total_data['ONU_Inactive'] += data['inactive']
    total_data['ONU_Others'] += sum(data.values()) - data['active'] - data['inactive']

# Convert to JSON
result = []
for pon, data in pon_data.items():
    pon_result = {
        'IFALIAS': pon,
        'ONU_Count': sum(data.values()),
        'ONU_Active': data['active'],
        'ONU_Inactive': data['inactive'],
        'ONU_Others': sum(data.values()) - data['active'] - data['inactive']
    }
    result.append(pon_result)

# Append total data
total_result = {
    'IFALIAS': 'total',
    'ONU_Count': total_data['ONU_Count'],
    'ONU_Active': total_data['ONU_Active'],
    'ONU_Inactive': total_data['ONU_Inactive'],
    'ONU_Others': total_data['ONU_Others']
}
result.append(total_result)

# Print or save the JSON
print(json.dumps(result, indent=4))
