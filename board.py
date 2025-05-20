# board.py
# Módulo para manejar el tablero y la lógica de juego del Tetris
# Autor: [Tu nombre]
# Fecha: Mayo 2025

from constants import GRID_WIDTH, GRID_HEIGHT, SCORE_SINGLE, SCORE_DOUBLE, SCORE_TRIPLE, SCORE_TETRIS

class Board:
    """
    Clase que representa el tablero de juego de Tetris.
    Maneja la lógica del tablero, colisiones, y puntuaciones.
    """
    
    def __init__(self):
        """
        Inicializa un tablero de juego vacío.
        El tablero es una matriz donde cada celda contiene el color de la pieza
        si está ocupada, o None si está vacía.
        """
        # Crear un tablero vacío como una matriz 2D (GRID_HEIGHT x GRID_WIDTH)
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Inicializar la puntuación y líneas eliminadas
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
    
    def is_valid_position(self, piece):
        """
        Verifica si una pieza puede ocupar la posición actual.
        
        Args:
            piece (Piece): La pieza a verificar
            
        Returns:
            bool: True si la posición es válida, False en caso contrario
        """
        # Obtener coordenadas de la pieza
        for x, y in piece.get_coordinates():
            # Verificar límites del tablero
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            
            # Si la pieza está por encima del tablero, es válido (para permitir spawning)
            if y < 0:
                continue
            
            # Verificar colisión con otras piezas en el tablero
            if self.grid[y][x] is not None:
                return False
                
        return True
    
    def add_piece(self, piece):
        """
        Fija una pieza al tablero.
        
        Args:
            piece (Piece): La pieza a fijar en el tablero
            
        Returns:
            bool: True si la pieza se fijó correctamente, False en caso contrario
        """
        # Obtener coordenadas de la pieza
        for x, y in piece.get_coordinates():
            # Ignorar las coordenadas que están fuera del tablero (por arriba)
            if y < 0:
                # Si una parte de la pieza está fuera del tablero, es game over
                return False
            
            # Añadir la pieza al tablero
            self.grid[y][x] = piece.color
            
        # Buscar y eliminar líneas completas
        lines_removed = self.clear_lines()
        
        # Actualizar puntuación
        self.update_score(lines_removed)
        
        return True
    
    def clear_lines(self):
        """
        Busca y elimina las líneas completas del tablero.
        
        Returns:
            int: Número de líneas eliminadas
        """
        lines_to_clear = []
        
        # Buscar líneas completas
        for y in range(GRID_HEIGHT):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # Eliminar líneas completas (de abajo hacia arriba)
        for y in sorted(lines_to_clear, reverse=True):
            # Eliminar la línea completa
            del self.grid[y]
            # Añadir una nueva línea vacía en la parte superior
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        # Actualizar contador de líneas eliminadas
        self.lines_cleared += len(lines_to_clear)
        
        # Actualizar nivel (cada 5 líneas)
        self.level = (self.lines_cleared // 5) + 1
        
        return len(lines_to_clear)
    
    def update_score(self, lines_removed):
        """
        Actualiza la puntuación basada en el número de líneas eliminadas.
        
        Args:
            lines_removed (int): Número de líneas eliminadas
        """
        if lines_removed == 0:
            return
        
        # Calcular puntos según número de líneas eliminadas
        points = 0
        if lines_removed == 1:
            points = SCORE_SINGLE
        elif lines_removed == 2:
            points = SCORE_DOUBLE
        elif lines_removed == 3:
            points = SCORE_TRIPLE
        elif lines_removed >= 4:
            points = SCORE_TETRIS
        
        # Multiplicar puntos por nivel actual
        self.score += points * self.level
    
    def is_game_over(self):
        """
        Verifica si el juego ha terminado (hay piezas en la parte superior del tablero).
        
        Returns:
            bool: True si el juego ha terminado, False en caso contrario
        """
        # Si hay piezas en la primera fila, el juego ha terminado
        return any(cell is not None for cell in self.grid[0])
    
    def get_board_state(self):
        """
        Obtiene el estado actual del tablero.
        
        Returns:
            list: Una copia de la matriz del tablero
        """
        # Devolver una copia profunda del tablero
        return [row[:] for row in self.grid]
    
    def preview_piece_position(self, piece):
        """
        Calcula la posición más baja posible para una pieza (para hard drop).
        
        Args:
            piece (Piece): La pieza a calcular su posición más baja
            
        Returns:
            int: La coordenada Y más baja posible para la pieza
        """
        # Hacer una copia de la pieza para no modificar la original
        test_piece = piece
        original_y = test_piece.y
        
        # Mover la pieza hacia abajo hasta que colisione
        while self.is_valid_position(test_piece):
            test_piece.y += 1
        
        # Retroceder un paso (la última posición válida)
        final_y = test_piece.y - 1
        
        # Restaurar la posición original
        test_piece.y = original_y
        
        return final_y
    
    def hard_drop(self, piece):
        """
        Realiza un hard drop de la pieza (la coloca en la posición más baja posible).
        
        Args:
            piece (Piece): La pieza a colocar
            
        Returns:
            int: La distancia que cayó la pieza
        """
        original_y = piece.y
        
        # Calcular la posición más baja
        lowest_y = self.preview_piece_position(piece)
        
        # Mover la pieza a la posición más baja
        piece.y = lowest_y
        
        # Calcular la distancia recorrida (para puntos extra)
        distance = lowest_y - original_y
        
        return distance

