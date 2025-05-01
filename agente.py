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
