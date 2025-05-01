from ambiente import Ambiente
from agente import Agente
from simulador import Simulador
import random

if __name__ == "__main__":
    print("=== Configuración del Ambiente ===")
    filas = int(input("Ingrese número de filas: "))
    columnas = int(input("Ingrese número de columnas: "))
    porcentaje_oscuro = float(
        input("Ingrese porcentaje de celdas oscuras (0-100): "))
    porcentaje_pared_interna = float(
        input("Ingrese porcentaje de paredes internas (0-100): "))

    pasos_maximos = int(input("Ingrese número máximo de pasos a ejecutar: "))
    mostrar_malla_pasos_input = input(
        "¿Desea mostrar la malla después de cada paso? (s/n): ").lower()
    mostrar_malla_pasos = mostrar_malla_pasos_input == 's'

    # Crear ambiente
    ambiente = Ambiente(filas, columnas, porcentaje_oscuro,
                        porcentaje_pared_interna)

    # Buscar posición inicial aleatoria válida (no pared)
    posiciones_validas = [(i, j) for i in range(1, filas - 1) for j in range(1, columnas - 1)
                          if ambiente.obtener_celda(i, j) != '#']

    fila_inicio, columna_inicio = random.choice(posiciones_validas)
    orientacion_inicio=random.choice(['Norte', 'Sur', 'Este', 'Oeste'])

    # Impromir malla generada
    print("\n--- Malla Generada ---")
    ambiente.mostrar_malla_con_agente(fila_inicio, columna_inicio, orientacion_inicio)

    # Crear agente
    agente = Agente(ambiente, fila_inicio, columna_inicio, orientacion_inicio)

    # Crear simulador
    simulador = Simulador(ambiente, agente, pasos_maximos, mostrar_malla_pasos)

    # Ejecutar simulación
    simulador.ejecutar()
