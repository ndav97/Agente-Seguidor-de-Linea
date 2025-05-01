import hashlib
from reglas import decidir_accion
from detector_bucle import DetectorBucle

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

<<<<<<< HEAD
=======
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

>>>>>>> bc40a41 (Inicializando el proyecto de la tarea 3)
    def ejecutar(self):
        with open("recorrido_agente.txt", "w") as recorrido:
            while self.pasos_realizados < self.pasos_maximos and not self.bucle_detectado:
                percepcion = self.agente.percepcion_actual()
<<<<<<< HEAD
                acciones, regla_disparada = decidir_accion(percepcion)
=======
                acciones, regla_disparada = self.decidir_accion(percepcion)
>>>>>>> bc40a41 (Inicializando el proyecto de la tarea 3)

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
<<<<<<< HEAD
            resumen.append(f"{regla}: {veces} vez/veces")
=======
            resumen.append(f"{regla}: {veces} veces")
>>>>>>> bc40a41 (Inicializando el proyecto de la tarea 3)
        resumen.append("------------------------------------")

        for linea in resumen:
            print(linea)

        with open("resultado_simulacion.txt", "w") as archivo:
            for linea in resumen:
<<<<<<< HEAD
                archivo.write(linea + "\n")
=======
                archivo.write(linea + "\n")
>>>>>>> bc40a41 (Inicializando el proyecto de la tarea 3)
