from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Conectar ao veículo (ajuste a string de conexão se necessário)
# Exemplo para SITL: 'udp:127.0.0.1:14550'
vehicle = connect('127.0.0.1:14550', wait_ready=True)

def monitor_altitude():
    """Imprime a altitude relativa atual."""
    print(f" Altitude Atual: {vehicle.location.global_relative_frame.alt:.2f}m")

def arm_and_takeoff(target_altitude):
    print("Iniciando verificações básicas...")
    while not vehicle.is_armable:
        print(" Aguardando inicialização do veículo...")
        time.sleep(1)

    print("Alterando para modo GUIDED...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Aguardando armamento...")
        time.sleep(1)

    print(f"Decolando para {target_altitude}m!")
    vehicle.simple_takeoff(target_altitude)

    # Monitorar subida
    while True:
        monitor_altitude()
        # Se atingir 95% da altitude alvo, saímos do loop
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Altitude alvo alcançada.")
            break
        time.sleep(1)

# --- Fluxo Principal ---

try:
    # 1. Decolagem em modo GUIDED
    arm_and_takeoff(10)

    # 2. Alteração para modo ALTHOLD
    print("Alterando modo para ALTHOLD...")
    vehicle.mode = VehicleMode("ALTHOLD")

    # 3. Monitoramento contínuo (exemplo de 10 segundos)
    print("Mantendo altitude em modo ALTHOLD. Monitorando...")
    for _ in range(10):
        monitor_altitude()
        time.sleep(1)

    print("Missão finalizada. Retornando para pouso (RTL)...")
    vehicle.mode = VehicleMode("RTL")

finally:
    # Fechar conexão
    print("Encerrando conexão.")
    vehicle.close()