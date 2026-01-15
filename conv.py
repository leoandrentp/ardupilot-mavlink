from dronekit import connect
import time
import math

# 1. CONEXÃO
print("Conectando ao drone via telemetria...")
# Certifique-se de que a porta COM5 está correta para o seu rádio
veiculo = connect('COM5', baud=57600, wait_ready=True)

def converter_rc_para_graus(pwm, limite_max):
    """Converte PWM 1000-2000 para Graus -limite a +limite (Centro 1500)"""
    if pwm is None: return 0.0
    desvio = pwm - 1500
    return desvio * (limite_max / 500.0)

def converter_throttle_para_porcentagem(pwm):
    """Converte PWM 1000-2000 para Porcentagem 0% a 100%"""
    if pwm is None: return 0.0
    # Garante que o PWM está no range correto
    pwm = max(1000, min(2000, pwm))
    porcentagem = (pwm - 1000) / 10.0
    return porcentagem

try:
    print("\n--- Monitor Delta V: RC & Atitude (Ctrl+C para sair) ---")
    while True:
        # EXPLICAÇÃO: Lendo o dicionário de canais da Pixhawk
        # Canal 1: Roll, 2: Pitch, 3: Throttle, 4: Yaw
        canais = veiculo.channels

        pwm_r = canais.get('1')
        pwm_p = canais.get('2')
        pwm_t = canais.get('3') # CANAL DE THROTTLE ADICIONADO
        pwm_y = canais.get('4')

        # Conversões
        roll_cmd     = converter_rc_para_graus(pwm_r, 45)
        pitch_cmd    = converter_rc_para_graus(pwm_p, 45)
        throttle_pct = converter_throttle_para_porcentagem(pwm_t)
        yaw_taxa_cmd = converter_rc_para_graus(pwm_y, 180)

        # Atitude Real para comparação
        real_roll  = math.degrees(veiculo.attitude.roll)
        real_pitch = math.degrees(veiculo.attitude.pitch)

        # Exibição no Terminal
        # Adicionamos o Throttle na visualização
        print(f"\r[THR: {throttle_pct:3.0f}%] | [ROLL] Cmd: {roll_cmd:5.1f}° Real: {real_roll:5.1f}° | [PITCH] Cmd: {pitch_cmd:5.1f}° Real: {real_pitch:5.1f}°", end="")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nMonitoramento encerrado pelo utilizador.")
    veiculo.close()