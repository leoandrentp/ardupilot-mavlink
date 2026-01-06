from dronekit import connect
import time
import math

# 1. CONEXÃO VIA TELEMETRIA
print("Conectando ao veículo via telemetria (57600 baud)...")
veiculo = connect('udp:127.0.0.1:14550', wait_ready=True)

def ajustar_parametro(nome_param, valor):
    """Função auxiliar para escrita e confirmação via rádio"""
    try:
        veiculo.parameters[nome_param] = valor
        time.sleep(1.2) # Tempo para sincronia da telemetria
        print(f"  [OK] {nome_param}: {veiculo.parameters[nome_param]}")
        return valor
    except Exception as e:
        print(f"  [ERRO] Falha ao ajustar {nome_param}: {e}")

def atualizar_ganhos_drone(kp_rp, ki_rp, kd_rp, kp_yaw, ki_yaw, kd_yaw):
    """
    Atualiza Roll e Pitch com os mesmos valores, e Yaw separadamente.
    """
    print("\n--- INICIANDO ATUALIZAÇÃO DE GANHOS ---")
    
    # AJUSTE ROLL (RLL)
    print("Ajustando ROLL...")
    ajustar_parametro('ATC_RAT_RLL_P', kp_rp)
    ajustar_parametro('ATC_RAT_RLL_I', ki_rp)
    ajustar_parametro('ATC_RAT_RLL_D', kd_rp)
    
    # AJUSTE PITCH (PIT) - IGUAL AO ROLL
    print("Ajustando PITCH (Simétrico ao Roll)...")
    ajustar_parametro('ATC_RAT_PIT_P', kp_rp)
    ajustar_parametro('ATC_RAT_PIT_I', ki_rp)
    ajustar_parametro('ATC_RAT_PIT_D', kd_rp)
    
    # AJUSTE YAW (DIFERENTE)
    print("Ajustando YAW...")
    ajustar_parametro('ATC_RAT_YAW_P', kp_yaw)
    ajustar_parametro('ATC_RAT_YAW_I', ki_yaw)
    ajustar_parametro('ATC_RAT_YAW_D', kd_yaw)
    
    print("--- PROCESSO CONCLUÍDO ---\n")

def radians_to_degrees(radians):
    return math.degrees(radians)

# Define an attitude listener callback function
def attitude_callback(attr_name, value):
    # 'value' is a Quaternion object with attributes pitch, roll, and yaw (in radians)
    pitch = radians_to_degrees(value.pitch)
    roll = radians_to_degrees(value.roll)
    yaw = radians_to_degrees(value.yaw)
    print(f"Attitude (degrees): Pitch={pitch:.2f}°, Roll={roll:.2f}°, Yaw={yaw:.2f}°")
    return pitch, roll, yaw

veiculo.add_attribute_listener('attitude', attitude_callback)

# --- ÁREA DE CONFIGURAÇÃO DO USUÁRIO ---

# Defina aqui os ganhos para ROLL e PITCH (Iguais)
KP_ROLL_PITCH = 0.150
KI_ROLL_PITCH = 0.010
KD_ROLL_PITCH = 0.004

# Defina aqui os ganhos para YAW (Diferente)
KP_YAW = 0.200
KI_YAW = 0.020
KD_YAW = 0.000

# Executa a atualização
atualizar_ganhos_drone(KP_ROLL_PITCH, KI_ROLL_PITCH, KD_ROLL_PITCH, 
                       KP_YAW, KI_YAW, KD_YAW)


###### LEITURA DOS CANAIS DO CONTROLE ######

canal = veiculo.channels
print(" Roll (Ch1): %s" % canal[1])
print(" Pitch (Ch2): %s" % canal[2])
print(" Throttle (Ch4): %s" % canal[3])
print(" Yaw (Ch3): %s" % canal[4])

######
try:
    while True:
        print("Ch1: %s, Ch2: %s, Ch3: %s, Ch4: %s" % (
            canal[1], canal[2], canal[3], canal[4])
            )
        time.sleep(1)

except KeyboardInterrupt:
    print("Fim da conexão com o veículo.")
    veiculo.close()

veiculo.remove_attribute_listener('attitude', attitude_callback)
veiculo.close()