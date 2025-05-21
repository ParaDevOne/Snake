# pieces.py
# Módulo para manejar las piezas de Tetris
# Autor: [ParaDevOne]
# Fecha: Mayo 2025
# Licencia: Simplified Open License (SOL) v1.0

import random
from constants import COLORS, SHAPES

class Piece:
    """
    Clase que representa una pieza de Tetris.
    Maneja la inicialización, rotación y movimiento de las piezas.
    """
    
    def __init__(self, shape_name=None, x=None, y=None):
        """
        Inicializa una pieza de Tetris.
        
        Args:
            shape_name (str, opcional): Nombre de la forma de la pieza. Si es None, se elige una aleatoria.
            x (int, opcional): Posición X inicial. Si es None, se calcula automáticamente.
            y (int, opcional): Posición Y inicial. Si es None, se calcula automáticamente.
        """
        # Si no se especifica una forma, elegir una al azar
        if shape_name is None:
            self.shape_name = random.choice(list(SHAPES.keys()))
        else:
            self.shape_name = shape_name
            
        # Establecer la forma y el color de la pieza
        self.shape = SHAPES[self.shape_name]
        self.color = COLORS[self.shape_name]
        
        # Establecer la rotación inicial (0, 90, 180 o 270 grados)
        self.rotation = 0
        
        # Calcular las dimensiones de la pieza según su forma
        self.width = len(self.shape[0])
        self.height = len(self.shape)
        
        # Establecer la posición inicial
        from constants import GRID_WIDTH
        self.x = (GRID_WIDTH // 2) - (self.width // 2) if x is None else x
        self.y = 0 if y is None else y
        
    def rotate(self):
        """
        Rota la pieza 90 grados en sentido horario.
        
        Returns:
            list: Nueva representación de la pieza rotada.
        """
        # Actualizar rotación
        self.rotation = (self.rotation + 90) % 360
        
        # Índice correspondiente a la rotación actual (0, 1, 2, 3)
        rot_index = self.rotation // 90
        
        # Obtener la forma rotada
        rotated_shape = SHAPES[self.shape_name][rot_index]
        
        # Actualizar dimensiones
        self.width = len(rotated_shape[0])
        self.height = len(rotated_shape)
        
        return rotated_shape
        
    def move_left(self):
        """Mueve la pieza una posición a la izquierda."""
        self.x -= 1
        
    def move_right(self):
        """Mueve la pieza una posición a la derecha."""
        self.x += 1
        
    def move_down(self):
        """Mueve la pieza una posición hacia abajo."""
        self.y += 1
        
    def get_coordinates(self):
        """
        Obtiene las coordenadas absolutas de las celdas ocupadas por la pieza.
        
        Returns:
            list: Lista de tuplas (x, y) para cada celda ocupada.
        """
        coords = []
        # Índice correspondiente a la rotación actual
        rot_index = self.rotation // 90
        shape = SHAPES[self.shape_name][rot_index]
        
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    coords.append((self.x + j, self.y + i))
        
        return coords

class PieceGenerator:
    """
    Clase que se encarga de generar piezas aleatorias
    y mantener una cola de piezas siguientes.
    """
    
    def __init__(self, queue_size=3):
        """
        Inicializa el generador de piezas.
        
        Args:
            queue_size (int): Tamaño de la cola de piezas siguientes.
        """
        self.queue_size = queue_size
        self.next_pieces = []
        
        # Inicializar la cola de piezas
        self._refill_queue()
        
    def _refill_queue(self):
        """Rellena la cola de piezas hasta alcanzar el tamaño deseado."""
        while len(self.next_pieces) < self.queue_size:
            # Seleccionar una forma aleatoria
            shape_name = random.choice(list(SHAPES.keys()))
            # Crear una nueva pieza en una posición "fuera del tablero"
            # (solo para mostrar vista previa)
            self.next_pieces.append(Piece(shape_name=shape_name, x=0, y=0))
    
    def get_next_piece(self):
        """
        Obtiene la siguiente pieza de la cola y genera una nueva.
        
        Returns:
            Piece: La siguiente pieza a jugar.
        """
        # Obtener la primera pieza de la cola
        next_piece = self.next_pieces.pop(0)
        
        # Regenerar la posición inicial correcta para la pieza
        from constants import GRID_WIDTH
        next_piece.x = (GRID_WIDTH // 2) - (next_piece.width // 2)
        next_piece.y = 0
        
        # Rellenar la cola
        self._refill_queue()
        
        return next_piece
    
    def peek_next_pieces(self):
        """
        Muestra las siguientes piezas sin sacarlas de la cola.
        
        Returns:
            list: Lista de las siguientes piezas en la cola.
        """
        return self.next_pieces.copy()

