# Agente Seguidor de Línea – Tarea 3 (FIA - Maestría en Inteligencia Artificial)

## 🧠 Descripción del proyecto

Este proyecto implementa un **agente reflejo simple** capaz de seguir líneas en una malla NxM simulada. Las líneas están representadas por celdas oscuras, y el entorno incluye paredes, zonas blancas y discontinuidades. El agente decide sus movimientos basándose únicamente en su percepción actual, sin memoria, salvo en caso de choque.

---

## ⚙️ Estructura del proyecto

```
./
|
├── main.py                  # Punto de entrada (interacción con el usuario)
├── agente.py                # Clase Agente: sensores, acciones, orientación
├── ambiente.py              # Clase Ambiente: malla, celdas, visualización textual
├── simulador.py             # Clase Simulador: lógica de reglas, recorrido y estadísticas
├── detector_bucle.py        # Detección de bucles infinitos
│
├── recorrido_agente.txt     # Registro generado, indica el paso a paso del movimiento del agente
├── resultado_simulacion.txt # Registro generado, indica las estadísticas y desempeño del agente
└── README.md                # Este archivo
```

---

## 🚀 Cómo ejecutar

Desde la terminal, dentro del proyecto:

```bash
python main.py
```

El programa solicitará:

- Número de filas y columnas
- Porcentaje de celdas oscuras (línea)
- Porcentaje de paredes internas
- Número máximo de pasos
- Si deseas ver la malla paso a paso (por consola)

---

## 📊 Estadísticas calculadas

Al finalizar, se generan los siguientes datos en consola y en `resultado_simulacion.txt`:

- Número total de pasos ejecutados
- Reglas diferentes utilizadas
- Cantidad de avances, rotaciones, choques
- Porcentaje de celdas oscuras pisadas
- Detección de bucles (sí/no)
- Uso de cada regla de decisión

También se guarda en `recorrido_agente.txt` el paso a paso completo del agente.

---

## 🧠 Reflexión académica

Este proyecto demuestra la implementación de un agente reflejo simple basado en reglas de decisión. La simulación refuerza conceptos como sensores, percepción, acciones, lógica condicional y evaluación del desempeño de agentes autónomos en entornos parcialmente accesibles y episódicos.

---

## 👨‍🏫 Datos del trabajo

- **Curso**: Fundamentos de Inteligencia Artificial – UNI
- **Tarea**: Tarea 3
- **Integrantes**:
  - Guillermo Choque
  - Kevin Chipana
  - Nicolás Dávila
  - Saúl Vega
  - Oscar Huayascachi

---
