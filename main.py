import random

class Agente:
    DIRECCIONES = ['Norte', 'Este', 'Sur', 'Oeste']
    MOVIMIENTOS = {
        'Norte': (-1, 0),
        'Sur': (1, 0),
        'Este': (0, 1),
        'Oeste': (0, -1)
    }

    def __init__(self, ambiente, fila_inicio, columna_inicio, orientacion_inicio='Norte'):
        self.ambiente = ambiente
        self.fila = fila_inicio
        self.columna = columna_inicio
        self.orientacion = orientacion_inicio
        self.choque = False

    def sensor_contacto(self):
        """Detecta si el agente ha chocado."""
        return self.choque

    def sensor_camara_base(self):
        """Detecta si la celda donde está parado es oscura o blanca."""
        celda = self.ambiente.obtener_celda(self.fila, self.columna)
        return 'oscura' if celda == '-' else 'blanca'

    def sensores_camaras_frontales(self):
        """Detecta qué hay en las celdas adelante: izquierda, centro, derecha."""
        percepciones = {'izquierda': 'pared',
                        'centro': 'pared', 'derecha': 'pared'}

        # Según orientación, calcular posiciones
        if self.orientacion == 'Norte':
            posiciones = {
                'izquierda': (self.fila - 1, self.columna - 1),
                'centro': (self.fila - 1, self.columna),
                'derecha': (self.fila - 1, self.columna + 1)
            }
        elif self.orientacion == 'Sur':
            posiciones = {
                'izquierda': (self.fila + 1, self.columna + 1),
                'centro': (self.fila + 1, self.columna),
                'derecha': (self.fila + 1, self.columna - 1)
            }
        elif self.orientacion == 'Este':
            posiciones = {
                'izquierda': (self.fila - 1, self.columna + 1),
                'centro': (self.fila, self.columna + 1),
                'derecha': (self.fila + 1, self.columna + 1)
            }
        elif self.orientacion == 'Oeste':
            posiciones = {
                'izquierda': (self.fila + 1, self.columna - 1),
                'centro': (self.fila, self.columna - 1),
                'derecha': (self.fila - 1, self.columna - 1)
            }

        # Leer el contenido de cada posición
        for direccion, (fila, columna) in posiciones.items():
            contenido = self.ambiente.obtener_celda(fila, columna)
            if contenido == '#':
                percepciones[direccion] = 'pared'
            elif contenido == '-':
                percepciones[direccion] = 'oscura'
            elif contenido == ' ':
                percepciones[direccion] = 'blanca'

        return percepciones

    def sensor_propioceptor(self):
        """Devuelve la orientación actual."""
        return self.orientacion

    def avanzar(self):
        """Avanza una celda en la dirección actual si es posible."""
        delta_fila, delta_columna = self.MOVIMIENTOS[self.orientacion]
        nueva_fila = self.fila + delta_fila
        nueva_columna = self.columna + delta_columna

        if self.ambiente.es_celda_valida(nueva_fila, nueva_columna):
            self.fila = nueva_fila
            self.columna = nueva_columna
            self.choque = False
        else:
            self.choque = True

    def rotar_izquierda(self):
        """Rota +90 grados (izquierda)."""
        idx = (self.DIRECCIONES.index(self.orientacion) - 1) % 4
        self.orientacion = self.DIRECCIONES[idx]

    def rotar_derecha(self):
        """Rota -90 grados (derecha)."""
        idx = (self.DIRECCIONES.index(self.orientacion) + 1) % 4
        self.orientacion = self.DIRECCIONES[idx]

    def percepcion_actual(self):
        """Obtiene todas las percepciones actuales en un solo diccionario."""
        return {
            'contacto': self.sensor_contacto(),
            'camara_base': self.sensor_camara_base(),
            'camaras_frontales': self.sensores_camaras_frontales(),
            'orientacion': self.sensor_propioceptor()
        }

class Ambiente:
    def __init__(self, filas: int, columnas: int, porcentaje_oscuro: float, porcentaje_pared_interna: float = 0):
        self.filas = filas
        self.columnas = columnas
        self.porcentaje_oscuro = porcentaje_oscuro
        self.porcentaje_pared_interna = porcentaje_pared_interna
        self.malla = []
        self.generar_malla()

    def generar_malla(self):
        """Genera la malla con paredes en los bordes y celdas internas aleatorias."""
        self.malla = [['' for _ in range(self.columnas)]
                      for _ in range(self.filas)]

        # Primero, colocar las paredes de borde
        for i in range(self.filas):
            for j in range(self.columnas):
                if i == 0 or i == self.filas - 1 or j == 0 or j == self.columnas - 1:
                    self.malla[i][j] = '#'

        # Crear lista de posiciones internas disponibles
        posiciones_internas = [(i, j) for i in range(
            1, self.filas - 1) for j in range(1, self.columnas - 1)]

        celdas_internas = len(posiciones_internas)

        # Calcular cuántas celdas serán oscuras y cuántas serán paredes internas
        cantidad_oscuro = int(celdas_internas * self.porcentaje_oscuro / 100)
        cantidad_pared_interna = int(
            celdas_internas * self.porcentaje_pared_interna / 100)

        # Elegir aleatoriamente las celdas para paredes internas y oscuras sin solaparse
        posiciones_paredes = random.sample(
            posiciones_internas, cantidad_pared_interna)
        posiciones_disponibles = list(
            set(posiciones_internas) - set(posiciones_paredes))
        posiciones_oscuras = random.sample(
            posiciones_disponibles, cantidad_oscuro)

        for i, j in posiciones_internas:
            if (i, j) in posiciones_paredes:
                self.malla[i][j] = '#'  # Pared interna
            elif (i, j) in posiciones_oscuras:
                self.malla[i][j] = '-'  # Celda oscura (línea)
            else:
                self.malla[i][j] = ' '  # Celda blanca (libre)

    def mostrar_malla(self):
        """Imprime la malla en consola."""
        for fila in self.malla:
            print(' '.join(fila))

    def mostrar_malla_con_agente(self, fila_agente, columna_agente, orientacion_agente):
        """Imprime la malla mostrando la posición del agente con orientación."""
        simbolos_orientacion = {
            'Norte': '^',
            'Sur': 'v',
            'Este': '>',
            'Oeste': '<'
        }
        simbolo_agente = simbolos_orientacion.get(orientacion_agente, 'A')

        for i in range(self.filas):
            fila_mostrar = ''
            for j in range(self.columnas):
                if i == fila_agente and j == columna_agente:
                    fila_mostrar += simbolo_agente + ' '
                else:
                    fila_mostrar += self.malla[i][j] + ' '
            print(fila_mostrar.rstrip())

    def obtener_celda(self, fila: int, columna: int) -> str:
        """Devuelve el contenido de una celda específica."""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            return self.malla[fila][columna]
        else:
            return '#'  # Fuera de límites = Pared

    def es_celda_valida(self, fila: int, columna: int) -> bool:
        """Verifica si una celda es transitable (no pared)."""
        contenido = self.obtener_celda(fila, columna)
        return contenido != '#'

class DetectorBucle:
    def __init__(self, umbral_bucle=6):
        self.umbral_bucle = umbral_bucle
        self.historial_estados = []

    def actualizar_estado(self, fila, columna, orientacion, camaras_frontales):
        estado_actual = (
            fila,
            columna,
            orientacion,
            camaras_frontales['izquierda'],
            camaras_frontales['centro'],
            camaras_frontales['derecha']
        )

        self.historial_estados.append(estado_actual)
        historial = self.historial_estados

        for n in range(self.umbral_bucle, len(historial)//2 + 1):
            if historial[-2*n:-n] == historial[-n:]:
                return True

        return False

class Simulador:
    def __init__(self, ambiente, agente, pasos_maximos, mostrar_malla_pasos=False, umbral_bucle=6):
        self.ambiente = ambiente
        self.agente = agente
        self.pasos_maximos = pasos_maximos
        self.mostrar_malla_pasos = mostrar_malla_pasos

        self.bucle_detectado = False
        self.detector_bucle = DetectorBucle(umbral_bucle)
        self.pasos_realizados = 0

        self.total_celdas_oscura = sum(row.count('-') for row in ambiente.malla)
        self.celdas_oscura_pisadas = set()
        self.reglas_contador = {}
        self.acciones_ejecutadas = set()

        # Estadísticas
        self.contador_avances = 0
        self.contador_rotaciones_izq = 0
        self.contador_rotaciones_der = 0
        self.contador_choques = 0
        self.reglas_usadas = set()

    def decidir_accion(self, percepcion):
        contacto = percepcion['contacto']
        camaras = percepcion['camaras_frontales']

        izquierda = camaras['izquierda']
        centro = camaras['centro']
        derecha = camaras['derecha']

        # Regla 1: Choque
        if contacto:
            giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
            return [giro], 'Regla_1_Choque_GiroAleatorio'

        # Regla 2: Centro adelante es pared y derecha es oscura
        if centro == 'pared' and derecha == 'oscura':
            return ['rotar_derecha'], 'Regla_2_CentroPared_DerechaOscura'

        # Regla 3: Izquierda oscura, centro pared, derecha blanca
        if izquierda == 'oscura' and centro == 'pared' and derecha == 'blanca':
            return ['rotar_izquierda'], 'Regla_3_IzqOscura_CentroPared'

        # Regla 4: Izquierda oscura, centro pared, derecha oscura
        if izquierda == 'oscura' and centro == 'pared' and derecha == 'oscura':
            giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
            return [giro], 'Regla_4_IzqDerOscura_CentroPared'

        # Regla 5: Todo pared
        if izquierda == 'pared' and centro == 'pared' and derecha == 'pared':
            giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
            return [giro], 'Regla_5_TodoPared'

        # Regla 6: Esquina izquierda
        if izquierda == 'pared' and centro == 'pared' and derecha == 'blanca':
            return ['rotar_derecha'], 'Regla_6_EsquinaIzquierda'

        # Regla 7: Esquina derecha
        if izquierda == 'blanca' and centro == 'pared' and derecha == 'pared':
            return ['rotar_izquierda'], 'Regla_7_EsquinaDerecha'

        # Regla 8: Centro pared, lados blancos
        if izquierda == 'blanca' and centro == 'pared' and derecha == 'blanca':
            giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
            return [giro], 'Regla_8_CentroPared_LadosBlancos'

        # Regla 9: Centro oscura
        if centro == 'oscura':
            return ['avanzar'], 'Regla_9_CentroOscura'

        # Regla 10: Centro blanca, derecha oscura
        if centro == 'blanca' and derecha == 'oscura':
            return ['avanzar', 'rotar_derecha'], 'Regla_10_DerechaOscura'

        # Regla 11: Centro blanca, izquierda oscura
        if centro == 'blanca' and izquierda == 'oscura':
            return ['avanzar', 'rotar_izquierda'], 'Regla_11_IzquierdaOscura'

        # Regla 12: Centro blanca, lados oscuros
        if centro == 'blanca' and izquierda == 'oscura' and derecha == 'oscura':
            giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
            return ['avanzar', giro], 'Regla_12_CaminoBlancoTotal'

        # Regla 13: Centro blanca, pared en ambos lados
        if centro == 'blanca' and izquierda == 'pared' and derecha == 'pared':
            return ['avanzar'], 'Regla_13_ParedIzquierda'

        # Regla 14: Centro blanca, pared izquierda, derecha blanca
        if centro == 'blanca' and izquierda == 'pared' and derecha == 'blanca':
            accion = random.choice([
                ['avanzar'],
                ['avanzar', 'rotar_derecha']
            ])
            return accion, 'Regla_14_AvanzarOR_AvanzarRotarDer'

        # Regla 15: Centro blanca, izquierda blanca, derecha pared
        if centro == 'blanca' and izquierda == 'blanca' and derecha == 'pared':
            accion = random.choice([
                ['avanzar'],
                ['avanzar', 'rotar_izquierda']
            ])
            return accion, 'Regla_15_AvanzarOR_AvanzarRotarIzq'

        # Regla 16: Centro blanca, lados blancos
        if centro == 'blanca' and izquierda == 'blanca' and derecha == 'blanca':
            accion = random.choice([
                ['avanzar', 'rotar_izquierda'],
                ['avanzar', 'rotar_derecha']
            ])
            return accion, 'Regla_16_BlancoTotal_Exploracion'

        # Regla 17: Default avanzar si se puede
        if centro != 'pared':
            return ['avanzar'], 'Regla_17_Default_Avanzar'

        # Regla 18: Default girar aleatoriamente si no se puede avanzar
        giro = random.choice(['rotar_izquierda', 'rotar_derecha'])
        return [giro], 'Regla_18_Default_GiroAleatorio'

    def ejecutar(self):
        with open("recorrido_agente.txt", "w") as recorrido:
            while self.pasos_realizados < self.pasos_maximos and not self.bucle_detectado:
                percepcion = self.agente.percepcion_actual()
                acciones, regla_disparada = self.decidir_accion(percepcion)

                for accion in acciones:
                    self.acciones_ejecutadas.add(accion)
                    if accion == 'avanzar':
                        self.agente.avanzar()
                        self.contador_avances += 1
                        if self.agente.sensor_contacto():
                            self.contador_choques += 1
                            break
                    elif accion == 'rotar_izquierda':
                        self.agente.rotar_izquierda()
                        self.contador_rotaciones_izq += 1
                    elif accion == 'rotar_derecha':
                        self.agente.rotar_derecha()
                        self.contador_rotaciones_der += 1

                if self.mostrar_malla_pasos:
                    print(f"\n--- Paso {self.pasos_realizados + 1} ---")
                    self.ambiente.mostrar_malla_con_agente(
                        self.agente.fila, self.agente.columna, self.agente.orientacion)

                recorrido.write(f"\n--- Paso {self.pasos_realizados + 1} ---\n")
                recorrido.write(self.generar_malla_con_agente())

                if regla_disparada:
                    self.reglas_usadas.add(regla_disparada)
                    self.reglas_contador[regla_disparada] = self.reglas_contador.get(regla_disparada, 0) + 1

                # Registrar celda oscura si está en una
                celda_actual = self.ambiente.obtener_celda(self.agente.fila, self.agente.columna)
                if celda_actual == '-':
                    self.celdas_oscura_pisadas.add((self.agente.fila, self.agente.columna))

                self.bucle_detectado = self.detector_bucle.actualizar_estado(
                    self.agente.fila,
                    self.agente.columna,
                    self.agente.orientacion,
                    percepcion['camaras_frontales']
                )

                self.pasos_realizados += 1

        self.mostrar_estadisticas()

    def generar_malla_con_agente(self):
        simbolos_orientacion = {
            'Norte': '^',
            'Sur': 'v',
            'Este': '>',
            'Oeste': '<'
        }
        simbolo_agente = simbolos_orientacion.get(self.agente.orientacion, 'A')
        resultado = ''

        for i in range(self.ambiente.filas):
            fila_mostrar = ''
            for j in range(self.ambiente.columnas):
                if i == self.agente.fila and j == self.agente.columna:
                    fila_mostrar += simbolo_agente + ' '
                else:
                    fila_mostrar += self.ambiente.malla[i][j] + ' '
            resultado += fila_mostrar.rstrip() + '\n'
        return resultado

    def mostrar_estadisticas(self):
        porcentaje_oscura_pisada = (len(self.celdas_oscura_pisadas) / self.total_celdas_oscura * 100) if self.total_celdas_oscura > 0 else 0
        porcentaje_acciones_usadas = (len(self.acciones_ejecutadas) / 3 * 100)  # asumiendo 3 acciones posibles

        resumen = []
        resumen.append("\n--- Estadísticas de la Simulación ---")
        resumen.append(f"Pasos realizados: {self.pasos_realizados}")
        resumen.append(f"Número de reglas usadas: {len(self.reglas_usadas)}")
        resumen.append(f"Número de avances: {self.contador_avances}")
        resumen.append(f"Número de rotaciones izquierda (+90°): {self.contador_rotaciones_izq}")
        resumen.append(f"Número de rotaciones derecha (-90°): {self.contador_rotaciones_der}")
        resumen.append(f"Número de choques contra pared: {self.contador_choques}")
        resumen.append(f"Bucle detectado: {'Sí' if self.bucle_detectado else 'No'}")
        resumen.append(f"Cantidad de celdas oscuras totales: {self.total_celdas_oscura}")
        resumen.append(f"Cantidad de celdas oscuras pisadas: {len(self.celdas_oscura_pisadas)}")
        resumen.append(f"% de celdas oscuras pisadas: {porcentaje_oscura_pisada:.2f}%")
        resumen.append(f"% de acciones ejecutadas: {porcentaje_acciones_usadas:.2f}%")
        resumen.append("\n--- Uso de Reglas ---")
        for regla, veces in self.reglas_contador.items():
            resumen.append(f"{regla}: {veces} veces")
        resumen.append("------------------------------------")

        for linea in resumen:
            print(linea)

        with open("resultado_simulacion.txt", "w") as archivo:
            for linea in resumen:
                archivo.write(linea + "\n")

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
