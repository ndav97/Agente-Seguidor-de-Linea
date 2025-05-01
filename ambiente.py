import random

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
