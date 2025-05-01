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
