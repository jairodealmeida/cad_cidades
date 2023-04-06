import requests
import socket

def log_usage(plugin_name, action, params=None):
    # Nome da ação que está sendo registrada (por exemplo, "Inicialização", "Seleção de camada")
    action_name = action

    # Nome do host que está executando o plugin
    host_name = socket.gethostname()

    # Outras informações relevantes que você deseja registrar
    # (por exemplo, ID do usuário, versão do QGIS, etc.)
    additional_params = params or {}

    # URL para enviar as informações (substitua com a sua URL)
    url = "http://datakode.com.br/licence"

    # Crie um dicionário com todas as informações que serão enviadas para o servidor
    log_data = {
        "plugin": plugin_name,
        "action": action_name,
        "host": host_name,
        **additional_params,
    }

    # Envie as informações para o servidor
    try:
        response = requests.post(url, json=log_data, timeout=0.5)
        response.raise_for_status()
        return response.text 
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar informações de uso: {e}")
        return f"Licença não checada, offline : {e}"