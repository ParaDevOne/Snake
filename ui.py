# ui.py
# Módulo para manejar la interfaz gráfica del Tetris

import pygame
import logging

from pygame.font import Font
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, 
    CELL_SIZE, COLORS, BG_COLOR, GRID_COLOR, TEXT_COLOR,
    UI_BG_COLOR, BORDER_COLOR
)

# Inicialización básica de pygame
# Configurar variables de entorno para compatibilidad

class GameUI:
    """
    Clase que maneja la interfaz gráfica del juego Tetris.
    Se encarga de la visualización del tablero, piezas, puntuaciones y menús.
    """
    
    def __init__(self, score_manager):
        """
        Inicializa la interfaz gráfica del juego.
        
        Args:
            score_manager (ScoreManager): Gestor de puntuaciones
        """
        try:
            # Inicialización básica de pygame
            pygame.init()
            
            # Verificar que el display se puede inicializar
            if not pygame.display.get_init():
                pygame.display.init()
            
            pygame.display.set_caption("Tetris")
            
            # Crear ventana con configuración básica
            logging.info("Creando ventana con configuración básica...")
            self.window: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            logging.info("Ventana creada correctamente")
            
            # Inicializar el subsistema de fuentes
            if not pygame.font.get_init():
                pygame.font.init()
        except Exception as e:
            logging.error(f"Error al crear ventana: {e}")
            import traceback
            logging.error(traceback.format_exc())
            pygame.quit()
            raise
        
        # Fuentes para texto
        self.title_font: Font = pygame.font.SysFont('Arial', 48, bold=True)
        self.large_font: Font = pygame.font.SysFont('Arial', 38, bold=True)  # Aumentado de 36 a 38
        self.score_font: Font = pygame.font.SysFont('Arial', 42, bold=True)  # Nueva fuente más grande para puntuación
        self.medium_font: Font = pygame.font.SysFont('Arial', 26)  # Aumentado de 24 a 26
        self.small_font: Font = pygame.font.SysFont('Arial', 18)
        
        # Gestor de puntuaciones
        self.score_manager = score_manager

        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        
        # Calcular dimensiones y posiciones
        self._calculate_layout()
        
        # Estado actual del menú (main, game, pause, gameover)
        self.current_state = "main"
        
        # Opciones de menú
        self.menu_options: dict[str, list[str]] = {
            "main": ["Jugar", "Rankings", "Salir"],
            "pause": ["Continuar", "Reiniciar", "Salir al Menú"]
        }
        self.selected_option = 0
        
    def _calculate_layout(self):
        """
        Calcula las dimensiones y posiciones de los elementos de la interfaz.
        """
        # Área del tablero
        self.board_width = GRID_WIDTH * CELL_SIZE
        self.board_height = GRID_HEIGHT * CELL_SIZE
        self.board_x = (WINDOW_WIDTH - self.board_width) // 4
        self.board_y = (WINDOW_HEIGHT - self.board_height) // 2
        
        # Área del panel lateral
        self.sidebar_width = WINDOW_WIDTH - self.board_width - (self.board_x * 2)
        self.sidebar_height = self.board_height
        self.sidebar_x = self.board_x + self.board_width + 20
        self.sidebar_y = self.board_y
        
        # Área de próximas piezas
        self.next_pieces_x = self.sidebar_x + 10
        self.next_pieces_y = self.sidebar_y + 40
        self.next_piece_size: float = CELL_SIZE * 0.8
        
    def draw_board(self, board):
        """
        Dibuja el tablero del juego.
        
        Args:
            board (Board): Objeto tablero con el estado actual
        """
        # Dibujar fondo del tablero
        pygame.draw.rect(
            self.window,
            BORDER_COLOR,
            (self.board_x - 2, self.board_y - 2, self.board_width + 4, self.board_height + 4)
        )
        pygame.draw.rect(
            self.window,
            BG_COLOR,
            (self.board_x, self.board_y, self.board_width, self.board_height)
        )
        
        # Dibujar cuadrícula
        self.draw_grid()
        
        # Dibujar piezas en el tablero
        grid_state = board.get_board_state()
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid_state[y][x]:
                    color = grid_state[y][x]
                    self.draw_cell(x, y, color)
    
    def draw_grid(self):
        """
        Dibuja la cuadrícula del tablero.
        """
        # Líneas verticales
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(
                self.window,
                GRID_COLOR,
                (self.board_x + x * CELL_SIZE, self.board_y),
                (self.board_x + x * CELL_SIZE, self.board_y + self.board_height),
                1
            )
        
        # Líneas horizontales
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(
                self.window,
                GRID_COLOR,
                (self.board_x, self.board_y + y * CELL_SIZE),
                (self.board_x + self.board_width, self.board_y + y * CELL_SIZE),
                1
            )
    
    def draw_cell(self, x, y, color, offset_x=0, offset_y=0, size=None):
        """
        Dibuja una celda en el tablero o en la vista previa.
        
        Args:
            x (int): Coordenada X de la celda
            y (int): Coordenada Y de la celda
            color (tuple): Color RGB de la celda
            offset_x (int): Desplazamiento X adicional
            offset_y (int): Desplazamiento Y adicional
            size (int, optional): Tamaño de la celda (si es diferente al estándar)
        """
        cell_size = size if size is not None else CELL_SIZE
        
        # Calcular posición real en pantalla
        screen_x = self.board_x + x * cell_size + offset_x
        screen_y = self.board_y + y * cell_size + offset_y
        
        # Dibujar celda (con borde más oscuro)
        pygame.draw.rect(
            self.window,
            color,
            (screen_x, screen_y, cell_size, cell_size)
        )
        
        # Borde para dar efecto 3D
        darker_color = tuple(max(0, c - 50) for c in color)
        pygame.draw.rect(
            self.window,
            darker_color,
            (screen_x, screen_y, cell_size, cell_size),
            1
        )
    
    def draw_piece(self, piece, board_offset=True, preview=False, size=None):
        """
        Dibuja una pieza en la pantalla.
        
        Args:
            piece (Piece): La pieza a dibujar
            board_offset (bool): Si es True, dibuja con offset del tablero
            preview (bool): Si es True, dibuja como vista previa
            size (int, optional): Tamaño de la celda (para vistas previas)
        """
        # Obtener coordenadas
        rot_index = piece.rotation // 90
        shape = piece.shape[rot_index]
        color = piece.color
        
        # Tamaño de la celda
        cell_size = size if size is not None else CELL_SIZE
        
        # Offset del tablero (solo si no es vista previa)
        offset_x: int = self.board_x if board_offset else 0
        offset_y: int = self.board_y if board_offset else 0
        
        # Si es vista previa, añadir transparencia
        draw_color = color
        if preview:
            draw_color = color[0], color[1], color[2], 128
        
        # Dibujar cada bloque de la pieza
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    screen_x = offset_x + (piece.x + j) * cell_size
                    screen_y = offset_y + (piece.y + i) * cell_size
                    
                    # Dibujar bloque
                    pygame.draw.rect(
                        self.window,
                        draw_color,
                        (screen_x, screen_y, cell_size, cell_size)
                    )
                    
                    # Borde
                    darker_color = tuple(max(0, c - 50) for c in color[:3])
                    pygame.draw.rect(
                        self.window,
                        darker_color,
                        (screen_x, screen_y, cell_size, cell_size),
                        1
                    )
    
    def draw_next_pieces(self, next_pieces):
        """
        Dibuja las próximas piezas en el panel lateral.
        
        Args:
            next_pieces (list): Lista de piezas siguientes
        """
        # Dibujar fondo
        pygame.draw.rect(
            self.window,
            UI_BG_COLOR,
            (self.sidebar_x, self.next_pieces_y - 30, self.sidebar_width, 250)
        )
        
        # Título
        self.draw_text("Próximas Piezas", self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 10, self.next_pieces_y - 25)
        
        # Dibujar cada pieza en la lista
        for i, piece in enumerate(next_pieces):
            # Posición de cada pieza
            piece_y: int = self.next_pieces_y + i * 60
            
            # Ajustar coordenadas para centrar la pieza en el panel
            rot_index = piece.rotation // 90
            shape = piece.shape[rot_index]
            width: float = len(shape[0]) * self.next_piece_size
            height: float = len(shape) * self.next_piece_size
            
            # Centrar en x
            piece_x: float = self.sidebar_x + (self.sidebar_width - width) // 2
            
            # Dibujar cada bloque
            for y in range(len(shape)):
                for x in range(len(shape[0])):
                    if shape[y][x]:
                        draw_x: float = piece_x + x * self.next_piece_size
                        draw_y: float = piece_y + y * self.next_piece_size
                        pygame.draw.rect(
                            self.window,
                            piece.color,
                            (draw_x, draw_y, self.next_piece_size, self.next_piece_size)
                        )
                        # Borde
                        darker_color = tuple(max(0, c - 50) for c in piece.color)
                        pygame.draw.rect(
                            self.window,
                            darker_color,
                            (draw_x, draw_y, self.next_piece_size, self.next_piece_size),
                            1
                        )
    
    def draw_score_panel(self, current_score, level, lines, highscore):
        """
        Dibuja el panel con puntuación, nivel y líneas.
        Mejorado con mejor visibilidad y espacio optimizado.
        
        Args:
            current_score (int): Puntuación actual
            level (int): Nivel actual
            lines (int): Líneas eliminadas
            highscore (int): Puntuación máxima
        """
        # Posición en y (debajo de próximas piezas)
        y_pos: int = self.next_pieces_y + 250
        
        # Dibujar fondo principal
        pygame.draw.rect(
            self.window,
            UI_BG_COLOR,
            (self.sidebar_x, y_pos, self.sidebar_width, 190)  # Aumentado altura de 180 a 190
        )
        
        # Añadir borde sutil para mejorar la visibilidad
        pygame.draw.rect(
            self.window,
            BORDER_COLOR,
            (self.sidebar_x, y_pos, self.sidebar_width, 190),
            2  # Borde de 2 píxeles
        )
        
        # Formatear puntuaciones
        score_str = self.score_manager.format_score(current_score)
        high_str = self.score_manager.format_score(highscore)
        
        # Dibujar textos con mejor espaciado
        self.draw_text("Puntuación", self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 10, y_pos + 10)
                    
        # Fondo destacado para la puntuación actual
        score_width = self.score_font.size(score_str)[0] + 20  # Ancho del texto + margen
        score_height = self.score_font.get_height() + 8  # Alto del texto + margen
        
        # Dibujar fondo semi-transparente para destacar la puntuación
        score_bg = pygame.Surface((score_width, score_height), pygame.SRCALPHA)
        score_bg.fill((100, 100, 255, 60))  # Azul semi-transparente
        self.window.blit(score_bg, (self.sidebar_x + 5, y_pos + 38))
        
        # Dibujar puntuación con fuente más grande
        self.draw_text(score_str, self.score_font, TEXT_COLOR, 
                    self.sidebar_x + 15, y_pos + 40)
        
        # Nivel y líneas en una sola fila para mejor distribución
        self.draw_text("Nivel:", self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 10, y_pos + 90)
        self.draw_text(str(level), self.large_font, TEXT_COLOR, 
                    self.sidebar_x + 80, y_pos + 88)
        
        self.draw_text("Líneas:", self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 130, y_pos + 90)
        self.draw_text(str(lines), self.large_font, TEXT_COLOR, 
                    self.sidebar_x + 200, y_pos + 88)
        
        # Récord con mejor visibilidad
        self.draw_text("Récord", self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 10, y_pos + 140)
        self.draw_text(high_str, self.medium_font, TEXT_COLOR, 
                    self.sidebar_x + 90, y_pos + 140)
    
    def draw_main_menu(self):
        """
        Dibuja el menú principal del juego.
        """
        # Fondo
        self.window.fill(BG_COLOR)
        
        # Título
        title_text: pygame.Surface = self.title_font.render("TETRIS", True, COLORS["I"])
        title_rect: pygame.Rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        self.window.blit(title_text, title_rect)
        
        # Opciones de menú
        for i, option in enumerate(self.menu_options["main"]):
            # Destacar opción seleccionada
            if i == self.selected_option:
                color: tuple[int, int, int] = COLORS["T"]
                font: Font = self.large_font
            else:
                color = TEXT_COLOR
                font = self.medium_font
                
            # Dibujar opción
            option_text: pygame.Surface = font.render(option, True, color)
            option_rect: pygame.Rect = option_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 50)
            )
            self.window.blit(option_text, option_rect)
            
        # Instrucciones
        instructions = "Usa ↑↓ para seleccionar, ENTER para confirmar"
        inst_text: pygame.Surface = self.small_font.render(instructions, True, TEXT_COLOR)
        inst_rect: pygame.Rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.window.blit(inst_text, inst_rect)
    
    def draw_pause_menu(self):
        """
        Dibuja el menú de pausa.
        """
        # Fondo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negro semi-transparente
        self.window.blit(overlay, (0, 0))
        
        # Título del menú de pausa
        title_text: pygame.Surface = self.large_font.render("PAUSA", True, TEXT_COLOR)
        title_rect: pygame.Rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.window.blit(title_text, title_rect)
        
        # Opciones de menú
        for i, option in enumerate(self.menu_options["pause"]):
            # Destacar opción seleccionada
            if i == self.selected_option:
                color: tuple[int, int, int] = COLORS["O"]
                font: Font = self.large_font
            else:
                color = TEXT_COLOR
                font = self.medium_font
                
            # Dibujar opción
            option_text: pygame.Surface = font.render(option, True, color)
            option_rect: pygame.Rect = option_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 50)
            )
            self.window.blit(option_text, option_rect)
    
    def draw_game_over(self, score, level, lines):
        """
        Dibuja la pantalla de game over.
        
        Args:
            score (int): Puntuación final
            level (int): Nivel alcanzado
            lines (int): Líneas eliminadas
        """
        # Fondo semi-transparente
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Negro más opaco
        self.window.blit(overlay, (0, 0))
        
        # Título
        title_text: pygame.Surface = self.title_font.render("GAME OVER", True, COLORS["Z"])
        title_rect: pygame.Rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        self.window.blit(title_text, title_rect)
        
        # Formatear puntuación
        score_str = self.score_manager.format_score(score)
        
        # Mostrar estadísticas
        stats: list[str] = [
            f"Puntuación: {score_str}",
            f"Nivel: {level}",
            f"Líneas: {lines}"
        ]
        
        # Verificar si es récord
        is_highscore = self.score_manager.is_highscore(score)
        if is_highscore:
            stats.append("¡NUEVO RÉCORD!")
        
        # Dibujar estadísticas
        y_offset = WINDOW_HEIGHT // 2 - 50
        for stat in stats:
            self.draw_text(stat, self.medium_font, TEXT_COLOR, 
                          WINDOW_WIDTH // 2, y_offset, center=True)
            y_offset += 40
        
        # Instrucciones
        if is_highscore:
            self.draw_text("Introduce tu nombre y presiona ENTER", 
                        self.small_font, TEXT_COLOR, 
                          WINDOW_WIDTH // 2, y_offset + 30, center=True)
        else:
            self.draw_text("Presiona ENTER para continuar", 
                        self.small_font, TEXT_COLOR, 
                          WINDOW_WIDTH // 2, y_offset + 30, center=True)
    
    def draw_text(self, text, font, color, x, y, center=False):
        """
        Dibuja texto en la pantalla.
        
        Args:
            text (str): Texto a dibujar
            font (pygame.font.Font): Fuente a utilizar
            color (tuple): Color RGB del texto
            x (int): Posición X
            y (int): Posición Y
            center (bool): Si es True, centra el texto en (x, y)
        """
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.window.blit(text_surface, text_rect)

    def show_score_effect(self, points, level=1):
        """
        Muestra un efecto visual cuando el jugador obtiene puntos.
        
        Args:
            points (int): Puntos obtenidos
            level (int): Nivel actual
        """
        if not points or not pygame.display.get_surface():
            return
            
        # Calcular puntos totales con multiplicador de nivel
        total_points = points * level
        
        # Formatear puntos
        points_str = f"+{self.score_manager.format_score(total_points)}"
        
        # Crear texto
        color = (255, 255, 150)  # Amarillo claro
        points_text = self.large_font.render(points_str, True, color)
        
        # Posición centrada sobre el tablero
        text_rect = points_text.get_rect(
            center=(self.board_x + self.board_width // 2, self.board_y + self.board_height // 3)
        )
        
        # Mostrar efecto por un breve momento
        self.window.blit(points_text, text_rect)
        pygame.display.update(text_rect)
        pygame.time.delay(600)  # 600ms
    
    def flash_lines(self, board, lines_to_clear):
        """
        Crea un efecto visual de destello para las líneas que se van a eliminar.
        
        Args:
            board: Tablero de juego
            lines_to_clear (list): Lista de índices de las líneas a eliminar
        """
        if not lines_to_clear or not pygame.display.get_surface():
            return
            
        # Guardar el estado original de las líneas
        original_grid = board.get_board_state()
        
        # Realizar el efecto de flash (3 destellos)
        flash_colors = [
            (255, 255, 255),  # Blanco
            (220, 220, 100),  # Amarillo claro
            (180, 180, 255)   # Azul claro
        ]
        
        for flash_color in flash_colors:
            # Cambiar el color de las líneas a eliminar
            for y in lines_to_clear:
                for x in range(len(original_grid[y])):
                    if original_grid[y][x] is not None:
                        # Dibujar celda con el color de destello
                        self.draw_cell(x, y, flash_color)
                        
            # Actualizar la pantalla
            pygame.display.update()
            pygame.time.delay(100)  # 100ms entre destellos
            
            # Restaurar el color original
            for y in lines_to_clear:
                for x in range(len(original_grid[y])):
                    if original_grid[y][x] is not None:
                        self.draw_cell(x, y, original_grid[y][x])
                        
            # Actualizar la pantalla
            pygame.display.update()
            pygame.time.delay(50)  # 50ms entre restauraciones
    
    def handle_menu_input(self, event, options):
        """
        Maneja la entrada de teclado en los menús.
        
        Args:
            event (pygame.event.Event): Evento de teclado
            options (list): Lista de opciones del menú actual
            
        Returns:
            str or None: Acción seleccionada o None si no hay selección
        """
        if event.type == pygame.KEYDOWN:
            # Navegación
            if event.key == pygame.K_UP:
                self.selected_option: int = (self.selected_option - 1) % len(options)
                return None
            elif event.key == pygame.K_DOWN:
                self.selected_option: int = (self.selected_option + 1) % len(options)
                return None
            # Selección
            elif event.key == pygame.K_RETURN:
                return options[self.selected_option]
        return None
    
    def draw_background(self):
        """
        Dibuja el fondo general de la pantalla de juego.
        """
        # Fondo principal
        self.window.fill(BG_COLOR)
        
        # Dibujar bordes o elementos decorativos
        # Aquí puedes añadir elementos visuales adicionales como patrones,
        # líneas o formas decorativas en el fondo
        
        # Ejemplo: patrón de cuadrícula tenue en el fondo
        for x in range(0, WINDOW_WIDTH, 40):
            pygame.draw.line(self.window, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.line(self.window, GRID_COLOR, (0, y), (WINDOW_WIDTH, y), 1)
    
    def draw_rankings(self):
        """
        Dibuja la pantalla de rankings.
        """
        # Fondo
        self.window.fill(BG_COLOR)
        
        # Título
        title_text: pygame.Surface = self.large_font.render("MEJORES PUNTUACIONES", True, COLORS["I"])
        title_rect: pygame.Rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.window.blit(title_text, title_rect)
        
        # Obtener rankings
        rankings = self.score_manager.get_rankings()
        
        # Si no hay rankings, mostrar mensaje
        if not rankings:
            self.draw_text("No hay puntuaciones registradas aún", 
                        self.medium_font, TEXT_COLOR, 
                        WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, center=True)
        else:
            # Encabezados
            headers: list[str] = ["Pos", "Jugador", "Puntuación", "Nivel", "Fecha"]
            header_widths: list[int] = [50, 200, 150, 80, 200]
            header_positions: list[int] = []
            
            # Calcular posiciones de encabezados
            x_pos: int = (WINDOW_WIDTH - sum(header_widths)) // 2
            for width in header_widths:
                header_positions.append(x_pos)
                x_pos += width
            
            # Dibujar encabezados
            y_pos = 120
            for i, header in enumerate(headers):
                self.draw_text(header, self.medium_font, COLORS["J"], 
                            header_positions[i], y_pos)
            
            # Dibujar línea separadora
            pygame.draw.line(
                self.window, 
                TEXT_COLOR, 
                (header_positions[0], y_pos + 30), 
                (header_positions[-1] + header_widths[-1], y_pos + 30), 
                1
            )
            
            # Dibujar rankings
            y_pos += 50
            for i, rank in enumerate(rankings):
                # Posición
                self.draw_text(f"{i+1}.", self.medium_font, TEXT_COLOR, 
                            header_positions[0], y_pos)
                
                # Jugador
                self.draw_text(rank["player"], self.medium_font, TEXT_COLOR, 
                            header_positions[1], y_pos)
                
                # Puntuación
                score_str = self.score_manager.format_score(rank["score"])
                self.draw_text(score_str, self.medium_font, TEXT_COLOR, 
                            header_positions[2], y_pos)
                
                # Nivel
                self.draw_text(str(rank["level"]), self.medium_font, TEXT_COLOR, 
                            header_positions[3], y_pos)
                
                # Fecha
                date_str = rank["date"].split()[0]  # Solo la fecha, sin hora
                self.draw_text(date_str, self.medium_font, TEXT_COLOR, 
                            header_positions[4], y_pos)
                
                y_pos += 40
        
        # Instrucciones
        self.draw_text("Presiona ESC para volver", self.small_font, TEXT_COLOR, 
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, center=True)

