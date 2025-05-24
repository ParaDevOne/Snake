# constants.py
# Módulo de constantes para el juego Tetris
# Autor: [ParaDevOne]
# Fecha: Mayo 2025

from typing import Literal
import pygame

# -----------------------------
# Dimensiones y configuración
# -----------------------------

# Dimensiones de la ventana (píxeles)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Dimensiones del tablero (celdas)
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Tamaño de celda (píxeles)
CELL_SIZE = 25

# FPS objetivo
FPS = 60

# -----------------------------
# Colores (RGB)
# -----------------------------

# Colores de las piezas
COLORS: dict[str, tuple[int, int, int]] = {
    "I": (0, 240, 240),   # Cian
    "O": (240, 240, 0),   # Amarillo
    "T": (160, 0, 240),   # Púrpura
    "S": (0, 240, 0),     # Verde
    "Z": (240, 0, 0),     # Rojo
    "J": (0, 0, 240),     # Azul
    "L": (240, 160, 0),   # Naranja
}

# Colores de la interfaz
BG_COLOR: tuple[Literal[0], Literal[0], Literal[0]] = (0, 0, 0)           # Negro (fondo general)
GRID_COLOR: tuple[Literal[50], Literal[50], Literal[50]] = (50, 50, 50)      # Gris oscuro (líneas de cuadrícula)
TEXT_COLOR: tuple[Literal[255], Literal[255], Literal[255]] = (255, 255, 255)   # Blanco (texto general)
UI_BG_COLOR: tuple[Literal[30], Literal[30], Literal[30]] = (30, 30, 30)     # Gris muy oscuro (fondos de la interfaz)
BORDER_COLOR: tuple[Literal[80], Literal[80], Literal[80]] = (80, 80, 80)    # Gris medio (bordes)

# -----------------------------
# Configuración del juego
# -----------------------------

# Velocidad (frames por caída de pieza)
INITIAL_FALL_SPEED = 50     # Más alto = más lento
FALL_SPEED_DECREMENT = 5    # Disminución de velocidad por nivel
MIN_FALL_SPEED = 1          # Velocidad mínima (más rápido)

# Puntuaciones
SCORE_SOFT_DROP = 1          # Puntos por soft drop (caída suave)
SCORE_HARD_DROP = 2          # Puntos por hard drop (caída dura)
SCORE_SINGLE = 40            # Puntos por 1 línea
SCORE_DOUBLE = 100           # Puntos por 2 líneas
SCORE_TRIPLE = 300           # Puntos por 3 líneas
SCORE_TETRIS = 1200          # Puntos por 4 líneas

# Retraso para eliminación de líneas (ms)
LINE_CLEAR_DELAY = 200

# -----------------------------
# Formas de las piezas
# -----------------------------

"""
Para cada pieza se definen 4 rotaciones (0°, 90°, 180°, 270°).
Las formas se representan como matrices donde:
    0 = celda vacía
    1 = celda ocupada
"""

# Definición de las formas de las piezas con sus cuatro rotaciones
SHAPES: dict[str, list[list[list[int]]]] = {
    # Pieza I (línea)
    "I": [
        # Rotación 0°
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ],
        # Rotación 180°
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ],
        # Rotación 270°
        [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0]
        ]
    ],
    
    # Pieza O (cuadrado)
    "O": [
        # Todas las rotaciones son iguales para O
        [
            [1, 1],
            [1, 1]
        ],
        [
            [1, 1],
            [1, 1]
        ],
        [
            [1, 1],
            [1, 1]
        ],
        [
            [1, 1],
            [1, 1]
        ]
    ],
    
    # Pieza T
    "T": [
        # Rotación 0°
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ],
        # Rotación 180°
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        # Rotación 270°
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]
        ]
    ],
    
    # Pieza S
    "S": [
        # Rotación 0°
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 1]
        ],
        # Rotación 180°
        [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 0]
        ],
        # Rotación 270°
        [
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0]
        ]
    ],
    
    # Pieza Z
    "Z": [
        # Rotación 0°
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0]
        ],
        # Rotación 180°
        [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 1]
        ],
        # Rotación 270°
        [
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0]
        ]
    ],
    
    # Pieza J
    "J": [
        # Rotación 0°
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ],
        # Rotación 180°
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]
        ],
        # Rotación 270°
        [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]
        ]
    ],
    
    # Pieza L
    "L": [
        # Rotación 0°
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ],
        # Rotación 90°
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
        # Rotación 180°
        [
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0]
        ],
        # Rotación 270°
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
    ]
}

# -----------------------------
# Controles del juego
# -----------------------------

# Teclas de movimiento
KEY_LEFT: int = pygame.K_LEFT
KEY_RIGHT: int = pygame.K_RIGHT
KEY_DOWN: int = pygame.K_DOWN
KEY_ROTATE: int = pygame.K_UP
KEY_HARD_DROP: int = pygame.K_SPACE

# Teclas de menú
KEY_PAUSE: int = pygame.K_p
KEY_ESCAPE: int = pygame.K_ESCAPE
KEY_ENTER: int = pygame.K_RETURN
