from dronekit import connect
import time

# 1. CONEXÃO VIA TELEMETRIA
# No Windows, verifique no Gerenciador de Dispositivos qual é a porta COM do seu rádio.
# Baudrate padrão de rádios de telemetria é 57600.
print("Conectando ao veículo via telemetria...")
vehicle = connect('COM5', baud=57600, wait_ready=True) #

def alterar_parametro_pid(eixo, tipo_ganho, valor):
    """
    eixo: 'RLL', 'PIT' ou 'YAW'
    tipo_ganho: 'P', 'I' ou 'D'
    valor: o número float que você deseja definir
    """
    # Constrói o nome exato do parâmetro do ArduPilot
    nome_parametro = f"ATC_RAT_{eixo.upper()}_{tipo_ganho.upper()}"
    
    try:
        # Lê o valor atual antes da alteração
        valor_antigo = vehicle.parameters[nome_parametro] #
        print(f"Alterando {nome_parametro}: {valor_antigo} -> {valor}")
        
        # Envia o novo valor para a Pixhawk
        vehicle.parameters[nome_parametro] = valor #
        
        # A telemetria precisa de um tempo para processar e confirmar
        time.sleep(1.5) 
        
        # Verifica se o valor foi atualizado com sucesso
        valor_confirmado = vehicle.parameters[nome_parametro] #
        print(f"Confirmação de {nome_parametro}: {valor_confirmado}")
        
    except KeyError:
        print(f"Erro: O parâmetro {nome_parametro} não foi encontrado no veículo.")
    except Exception as e:
        print(f"Erro na conexão: {e}")

# --- ESPAÇO PARA SEUS AJUSTES MANUAIS ---

# Exemplos de uso (Basta descomentar e colocar o valor que você quer):

# ROLL
# alterar_parametro_pid('RLL', 'P', 0.15)
# alterar_parametro_pid('RLL', 'I', 0.01)
# alterar_parametro_pid('RLL', 'D', 0.004)

# PITCH
# alterar_parametro_pid('PIT', 'P', 0.15)
# alterar_parametro_pid('PIT', 'I', 0.01)
# alterar_parametro_pid('PIT', 'D', 0.004)

# YAW
# alterar_parametro_pid('YAW', 'P', 0.20)
# alterar_parametro_pid('YAW', 'I', 0.02)
# alterar_parametro_pid('YAW', 'D', 0.00)

print("Operação concluída.")
vehicle.close() #