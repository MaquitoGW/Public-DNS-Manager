import requests
import json
import schedule
import time

# funcão para pegar ip publico 
def get_public_ip():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return data['ip']
    except Exception as e:
        print(f"Erro ao obter o endereço IP: {e}")
        return None

# funcao para salvar o ip
def save_ip(ip):
    try:  
        # Abre o arquivo para escrita
        with open('cache.txt', "w") as arquivo:
            # Escreve os dados no arquivo
            arquivo.write(ip)
            
        return "Ip salvo no cache."
    except:
        return "Erro ao salvar ip."

# Fucao para ler o arquivo de cache    
def open_ip():
    try: 
        # Abre o arquivo para leitura
        with open('cache.txt', "r") as arquivo:
            # Lê os dados do arquivo
            return arquivo.read()
    except:
        return None

def config(value):
    try:
        # Abre o arquivo para leitura
        with open("config.json", "r") as arquivo:
            # Lê os dados do arquivo
            file = arquivo.read()
            data = json.loads(file)  # Use json.loads() para analisar a string JSON
            return data[value]
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")


# atualizar o Cloudflare 
def update_cloudflare(new_ip_address):
    try:
        # Configurações da API
        api_key = config('api_key')
        api_email = config('api_email')
        zone_id = config('zone_id')
        record_name = config('record_name')
        
        ## Endpoint da Cloudflare API para obter informações sobre a zona
        zone_info_endpoint = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
        
        # Parâmetros para a solicitação
        params = {'name': record_name}
        
        # Headers da solicitação
        headers = {
            'X-Auth-Email': api_email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json'
        }
        
        # Realizar a solicitação para obter informações sobre os registros DNS
        response = requests.get(zone_info_endpoint, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            dns_records = data['result']
        
            # Encontrar o ID do registro DNS desejado
            record_id = None
            for record in dns_records:
                if record['name'] == record_name:
                    record_id = record['id']
                    break
        
            if record_id is not None:
                # Endpoint da Cloudflare API para atualizar um registro DNS
                update_endpoint = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
        
                # Payload para a atualização
                payload = {
                    'type': 'A',
                    'name': record_name,
                    'content': new_ip_address,
                    'ttl': 1,  # Time-to-Live em segundos (1 segundo neste exemplo)
                    'proxied': False  # Se estiver utilizando a proteção da Cloudflare (Proxy)
                }
        
                # Realizar a atualização
                response = requests.put(update_endpoint, headers=headers, json=payload)
        
                if response.status_code == 200:
                    print(f"Registro DNS atualizado com sucesso para {new_ip_address}")
                else:
                    print(f"Falha ao atualizar o registro DNS. Código de status: {response.status_code}")
            else:
                print(f"Registro DNS '{record_name}' não encontrado na zona.")
        else:
            print(f"Falha ao obter informações sobre os registros DNS. Código de status: {response.status_code}")
    except: 
        print('Erro ao atulizar o DNS no Cloudflare')
        return None

 # Verificar se ip salvo e igual atual
def job():
    atual_ip = get_public_ip()
    cache_ip = open_ip()

    if atual_ip != cache_ip:
        # atualizar ip
        save_ip(atual_ip)  # atualiza o cache local
        update_cloudflare(atual_ip)  # atualiza o dns no Cloudflare
        print('Ip alterado com sucesso!')
    else:
        # Ip está ok
        print('Ip não precisa ser alterado.')

# Agendar a execução do job a cada 30 minutos
schedule.every(30).minutes.do(job)

# Executar o job uma vez para iniciar
job()

# Manter o script em execução para permitir que o schedule funcione
while True:
    schedule.run_pending()
    time.sleep(1)
