# 📄 Proyecto Módulo 1 – Trivial en Python

## 🎮 Trivial de Series – Proyecto Módulo 1 (Python)

Un juego de preguntas y respuestas desarrollado en Python por el Equipo 2 formado por Camila López, María Granero y Nieves Sánchez.

El objetivo es practicar estructuras de control, diccionarios, listas, funciones, manejo de errores y lógica básica.

---

## 👥 Equipo y Roles

| Miembro        | Rol           | Tareas principales                                                              |
|----------------|---------------|---------------------------------------------------------------------------------|
| Nieves Sánchez | Scrum Master  | Organización, tablero Kanban, milestones, control de avances, README y revisión |
| Camila López   | Desarrollo    | Lógica del juego, funciones, control de errores y revisión                      |
| María Granero  | Documentación | Estructura de datos, README, presentación, prueba del juego y revisión          |

---

## 🎯 Objetivo del proyecto

Desarrollar un juego de trivial en consola donde:

- El jugador elige cuántas preguntas quiere jugar (mínimo 5).

- No puede elegir más preguntas de las que existen.

- Dispone de 3 vidas y pierde 1 por cada respuesta incorrecta.

- Si llega a 0 vidas → la partida termina automáticamente.

- Cada acierto suma 1 punto a la puntuación final.

- El juego finaliza cuando:

    - se responden todas las preguntas seleccionadas, o 
    - el jugador se queda sin vidas.

---

## 🧠 Contenidos de Python aplicados

Este proyecto pone en práctica:

- Variables y tipos de datos

- Listas y diccionarios

- Funciones

- Bucles for

- Condiciones if / elif / else

- Manejo de errores con try/except

- Conversión de datos (int(), upper(), etc.)

- Uso de librerías (random.sample)

---

## 🏗️ Estructura del juego

1. Inicio

    Mensaje de bienvenida

    Petición del nombre del jugador

    Petición del número de preguntas

    Validación: mínimo 5

    Validación: máximo = número total de preguntas disponibles

    Manejo de errores con try/except

2. Preparación de la partida

    Selección aleatoria de preguntas con random.sample()

    Inicialización de variables:

    puntuacion = 0

    vidas = 3

3. Bucle principal del juego

    Para cada pregunta del mazo:

    Mostrar pregunta y opciones

    Solicitar respuesta (A/B/C/D)

    Validar entrada

    Comparar con la respuesta correcta

    Si acierta → sumar 1 punto

    Si falla → restar 1 vida

    Si vidas == 0 → mensaje de fin de partida + break

4. Final del juego

    Mostrar puntuación total

    Mensaje final según:

    si ha agotado vidas

    o si ha terminado todas las preguntas

---

## 📦 Estructura de datos

Las preguntas están almacenadas en una lista de diccionarios, un formato como este:

preguntas = [
    {
        "pregunta": "Un pueblo donde lo inexplicable...",
        "opciones": {
            "A": "Dark",
            "B": "Stranger Things",
            "C": "The OA",
            "D": "Glitch"
        },
        "respuesta_correcta": "B"
    },
    ...
]

Este formato permite:

Acceso a cada pregunta mediante índices

Acceso limpio a opciones con claves A/B/C/D

Manipulación sencilla por parte del bucle del juego

---

## 🔀 Flujo del programa (resumen visual)

Inicio → Petición de nombre → Elección nº de preguntas → Validación  
↓  
random.sample → Crear mazo de juego  
↓  
Inicializar puntuación y vidas  
↓  
Bucle for de preguntas  
     ├─ Mostrar pregunta  
     ├─ Pedir respuesta  
     ├─ Validar  
     ├─ Acierto → +1 punto  
     └─ Fallo → -1 vida  
↓  
¿vidas == 0? → Fin  
↓  
Resultados y mensaje final

---

## 🧪 Pruebas realizadas

| Prueba                                       | Resultado                              |
|----------------------------------------------|----------------------------------------|
| Introducir texto en lugar de número          | Error controlado con `try/except`      |
| Elegir menos de 5 preguntas                  | Mensaje + nueva petición               |
| Elegir más preguntas de las disponibles      | Mensaje + nueva petición               |
| Responder con letras minúsculas              | Convertido a mayúsculas con `.upper()` |
| Perder todas las vidas                       | Bucle finaliza con `break`             |

---

## 🚀 Mejoras futuras

Interfaz gráfica con Tkinter

Modo dos jugadores

Guardado de puntuaciones en archivo

Categorías de preguntas

Añadir sonidos o animaciones

Integrar niveles de dificultad

---

## 🎤 Presentación del proyecto

Incluye:

Explicación del objetivo

Estructura del juego

Flujo de ejecución

Diapositivas en Canva

Demo en directo

Preguntas de la profesora (cliente)

---

## 🗂️ Estructura del repositorio

```text
proyecto-da-promo-64-modulo-1-team-2/   ← raíz del repo
├─ README.md
├─ trivial.ipynb
└─ trivial_pygame/
   ├─ main.py
   ├─ ui_utils.py
   └─ preguntas.py
```

---

## 📚 Cómo ejecutar el programa

### Opción 1: Ejecutar en Jupyter Notebook (versión original)

**Requisitos:**

- Python 3.x
- Jupyter Notebook (archivo `.ipynb`)

**Pasos:**

1. Abrir el archivo `trivial.ipynb`
2. Ejecutar todas las celdas

---

### Opción 2: Ejecutar la interfaz gráfica (Pygame)

**Requisitos:**

- Python 3.x
- `pygame` instalado

**Pasos (abre la terminal en la carpeta del repo y ejecuta):**

```bash
pip install pygame
python trivial_pygame/main.py

# En Windows también puede ser:
py trivial_pygame/main.py
```

---

## 📄 Licencia

Proyecto académico del bootcamp (Adalab). Uso educativo.

Autores: Camila López · María Granero · Nieves Sánchez
