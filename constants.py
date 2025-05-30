# constants.py
# Módulo de constantes para el juego Tetris

from typing import Literal
import pygame

# -----------------------------
# Dimensiones y configuración
# -----------------------------

# Dimensiones de la ventana (píxeles)
WINDOW_WIDTH: Literal[800] = 800
WINDOW_HEIGHT: Literal[600] = 600

# Dimensiones del tablero (celdas)
GRID_WIDTH: Literal[10] = 10
GRID_HEIGHT: Literal[20] = 20

# Tamaño de celda (píxeles)
CELL_SIZE: Literal[25] = 25

# FPS objetivo
FPS: Literal[60] = 60

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
BG_COLOR: tuple[Literal[10], Literal[10], Literal[30]] = (10, 10, 30)      # Azul muy oscuro (fondo general)
GRID_COLOR: tuple[Literal[60], Literal[60], Literal[70]] = (60, 60, 70)      # Gris azulado (líneas de cuadrícula)
TEXT_COLOR: tuple[Literal[240], Literal[240], Literal[255]] = (240, 240, 255)  # Blanco azulado (texto general)
UI_BG_COLOR: tuple[Literal[25], Literal[25], Literal[40]] = (25, 25, 40)     # Azul oscuro (fondos de la interfaz)
BORDER_COLOR: tuple[Literal[100], Literal[100], Literal[120]] = (100, 100, 120)  # Gris azulado medio (bordes)

# -----------------------------
# Configuración del juego
# -----------------------------

# Velocidad (frames por caída de pieza)
INITIAL_FALL_SPEED = 150     # Más alto = más lento
FALL_SPEED_DECREMENT = 5    # Disminución de velocidad por nivel
MIN_FALL_SPEED = 1          # Velocidad mínima (más rápido)

# Puntuaciones (solo por líneas completadas)
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
