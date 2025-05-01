import random

def decidir_accion(percepcion):
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