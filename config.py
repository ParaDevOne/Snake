# config.py
# Módulo para manejar la configuración del juego Tetris

import json
import os
import logging
import pygame
from typing import Dict, Any, Optional, Tuple, List, Literal

# Configuración por defecto
DEFAULT_CONFIG = {
    # Ajustes de juego
    "game": {
        "initial_fall_speed": 150,  # Velocidad inicial (frames por caída)
        "fall_speed_decrement": 5,  # Disminución de velocidad por nivel
        "min_fall_speed": 1,        # Velocidad mínima (más rápido)
        "next_pieces_preview": 3,   # Número de piezas en vista previa
    },
    
    # Ajustes visuales
    "visual": {
        "window_width": 800,
        "window_height": 600,
        "cell_size": 25,
        "show_grid": True,           # Mostrar cuadrícula en el tablero
        "show_ghost_piece": True,    # Mostrar pieza fantasma (vista previa de caída)
        "show_score_effects": True,  # Mostrar efectos visuales al puntuar
        "theme": "default",          # Tema de colores (default, dark, light, retro)
    },
    
    # Teclas de control
    "controls": {
        "move_left": pygame.K_LEFT,
        "move_right": pygame.K_RIGHT,
        "move_down": pygame.K_DOWN,
        "rotate": pygame.K_UP,
        "hard_drop": pygame.K_SPACE,
        "pause": pygame.K_p,
        "exit": pygame.K_ESCAPE,
    },
    
    # Temas de colores
    "themes": {
        "default": {
            "bg_color": (10, 10, 30),            # Fondo general
            "grid_color": (60, 60, 70),          # Líneas de cuadrícula
            "text_color": (240, 240, 255),       # Texto general
            "ui_bg_color": (25, 25, 40),         # Fondos de interfaz
            "border_color": (100, 100, 120),     # Bordes
            "piece_colors": {
                "I": (0, 240, 240),   # Cian
                "O": (240, 240, 0),   # Amarillo
                "T": (160, 0, 240),   # Púrpura
                "S": (0, 240, 0),     # Verde
                "Z": (240, 0, 0),     # Rojo
                "J": (0, 0, 240),     # Azul
                "L": (240, 160, 0),   # Naranja
            }
        },
        "dark": {
            "bg_color": (5, 5, 15),              # Fondo más oscuro
            "grid_color": (40, 40, 50),          # Líneas de cuadrícula
            "text_color": (200, 200, 220),       # Texto menos brillante
            "ui_bg_color": (15, 15, 25),         # Fondos de interfaz
            "border_color": (70, 70, 90),        # Bordes
            "piece_colors": {
                "I": (0, 180, 180),   # Cian más oscuro
                "O": (180, 180, 0),   # Amarillo más oscuro
                "T": (120, 0, 180),   # Púrpura más oscuro
                "S": (0, 180, 0),     # Verde más oscuro
                "Z": (180, 0, 0),     # Rojo más oscuro
                "J": (0, 0, 180),     # Azul más oscuro
                "L": (180, 120, 0),   # Naranja más oscuro
            }
        },
        "light": {
            "bg_color": (230, 230, 250),         # Lavanda claro
            "grid_color": (180, 180, 210),       # Líneas de cuadrícula
            "text_color": (40, 40, 60),          # Texto oscuro
            "ui_bg_color": (210, 210, 230),      # Fondos de interfaz
            "border_color": (150, 150, 180),     # Bordes
            "piece_colors": {
                "I": (0, 200, 200),   # Cian
                "O": (220, 220, 0),   # Amarillo
                "T": (180, 0, 220),   # Púrpura
                "S": (0, 200, 0),     # Verde
                "Z": (220, 0, 0),     # Rojo
                "J": (0, 0, 200),     # Azul
                "L": (220, 140, 0),   # Naranja
            }
        },
        "retro": {
            "bg_color": (0, 0, 0),                # Negro puro
            "grid_color": (50, 50, 50),           # Gris oscuro
            "text_color": (0, 255, 0),            # Verde terminal
            "ui_bg_color": (20, 20, 20),          # Gris muy oscuro
            "border_color": (0, 200, 0),          # Verde oscuro
            "piece_colors": {
                "I": (0, 255, 255),   # Cian brillante
                "O": (255, 255, 0),   # Amarillo brillante
                "T": (255, 0, 255),   # Magenta brillante
                "S": (0, 255, 0),     # Verde brillante
                "Z": (255, 0, 0),     # Rojo brillante
                "J": (0, 0, 255),     # Azul brillante
                "L": (255, 165, 0),   # Naranja brillante
            }
        }
    }
}

class ConfigManager:
    """
    Clase que gestiona la configuración del juego.
    Maneja la carga, guardado y modificación de la configuración.
    """
    
    def __init__(self, config_file="config.json"):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_file (str): Ruta al archivo de configuración
        """
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        
        # Cargar configuración existente
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Carga la configuración desde el archivo JSON.
        Si el archivo no existe, se crea con la configuración por defecto.
        
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as file:
                    loaded_config = json.load(file)
                    
                    # Actualizar configuración, manteniendo valores por defecto
                    # para cualquier opción que no esté en el archivo
                    self._update_config_recursive(self.config, loaded_config)
                    
                logging.info("Configuración cargada correctamente")
                return True
            else:
                # Si no existe el archivo, lo creamos con la configuración por defecto
                self.save_config()
                logging.info("Archivo de configuración creado con valores por defecto")
                return True
                
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error al cargar configuración: {e}")
            # Si hay error, mantener la configuración por defecto
            return False
    
    # Definición de rangos válidos para validación
    _CONFIG_RANGES = {
        "game": {
            "initial_fall_speed": {"min": 10, "max": 300},
            "fall_speed_decrement": {"min": 1, "max": 20},
            "min_fall_speed": {"min": 1, "max": 10},
            "next_pieces_preview": {"min": 1, "max": 5}
        },
        "visual": {
            "window_width": {"min": 640, "max": 1920},
            "window_height": {"min": 480, "max": 1080},
            "cell_size": {"min": 15, "max": 40}
        }
    }
    
    def _validate_value(self, section, key, value):
        """
        Valida un valor según su tipo y rango si aplica.
        
        Args:
            section (str): Sección de la configuración
            key (str): Clave del valor
            value: Valor a validar
            
        Returns:
            tuple: (bool, str) - (es_válido, mensaje_error)
        """
        # Validar tipo
        default_value = DEFAULT_CONFIG.get(section, {}).get(key)
        if default_value is not None and not isinstance(value, type(default_value)):
            return False, f"Tipo incompatible para {section}.{key}: esperado {type(default_value).__name__}, recibido {type(value).__name__}"
        
        # Validar rango para valores numéricos
        if isinstance(value, (int, float)) and section in self._CONFIG_RANGES and key in self._CONFIG_RANGES[section]:
            range_info = self._CONFIG_RANGES[section][key]
            if value < range_info["min"] or value > range_info["max"]:
                return False, f"Valor fuera de rango para {section}.{key}: debe estar entre {range_info['min']} y {range_info['max']}"
        
        # Validar tema
        if section == "visual" and key == "theme" and value not in DEFAULT_CONFIG["themes"]:
            return False, f"Tema no válido: {value}. Temas disponibles: {', '.join(DEFAULT_CONFIG['themes'].keys())}"
        
        # Validar controles (asegurar que son códigos de tecla válidos)
        if section == "controls" and not isinstance(value, int):
            return False, f"Código de tecla no válido para {key}: debe ser un entero"
        
        return True, ""
    
    def _update_config_recursive(self, default_dict, update_dict, path=""):
        """
        Actualiza recursivamente el diccionario de configuración, 
        manteniendo la estructura y valores por defecto cuando sea necesario.
        Incluye validación de tipos y rangos.
        
        Args:
            default_dict (dict): Diccionario con valores por defecto
            update_dict (dict): Diccionario con nuevos valores
            path (str): Ruta actual en la jerarquía de configuración (para mensajes de error)
        """
        for key, value in update_dict.items():
            current_path = f"{path}.{key}" if path else key
            
            if key in default_dict:
                if isinstance(value, dict) and isinstance(default_dict[key], dict):
                    # Recursión para diccionarios anidados
                    self._update_config_recursive(default_dict[key], value, current_path)
                else:
                    # Validar y actualizar valor
                    section = path if path else key
                    subkey = key if path else None
                    
                    if subkey:
                        is_valid, error_msg = self._validate_value(section, subkey, value)
                    else:
                        # Si es un diccionario de primer nivel, no necesita validación específica
                        is_valid, error_msg = True, ""
                    
                    if is_valid:
                        try:
                            # Manejo especial para convertir listas a tuplas (para colores)
                            if isinstance(default_dict[key], tuple) and isinstance(value, list):
                                # Convertir lista a tupla si los tipos internos coinciden
                                try:
                                    default_dict[key] = tuple(value)
                                    logging.debug(f"Lista convertida a tupla en: {current_path}")
                                except (TypeError, ValueError) as e:
                                    logging.warning(f"No se pudo convertir lista a tupla en: {current_path} - {e}")
                            # Manejar el caso especial de colores anidados en piece_colors
                            elif isinstance(default_dict[key], dict) and isinstance(value, dict) and "piece_colors" in current_path:
                                # Convertir todas las listas de colores en pieza a tuplas
                                for piece, color in value.items():
                                    if isinstance(color, list) and piece in default_dict[key]:
                                        default_dict[key][piece] = tuple(color)
                                        logging.debug(f"Color de pieza convertido a tupla: {current_path}.{piece}")
                            # Verificar tipo compatible para otros casos
                            elif isinstance(value, type(default_dict[key])) or isinstance(default_dict[key], type(value)):
                                default_dict[key] = value
                                logging.debug(f"Configuración actualizada: {current_path} = {value}")
                            else:
                                logging.warning(f"Tipo incompatible en configuración: {current_path} (esperado {type(default_dict[key]).__name__}, recibido {type(value).__name__})")
                        except TypeError:
                            # Para tipos que no se pueden comparar directamente
                            default_dict[key] = value
                            logging.debug(f"Configuración actualizada (sin validación de tipo): {current_path} = {value}")
                    else:
                        logging.warning(f"Valor de configuración inválido ignorado: {current_path} - {error_msg}")
            else:
                logging.warning(f"Clave de configuración desconocida ignorada: {current_path}")
    
    def save_config(self) -> bool:
        """
        Guarda la configuración actual en el archivo JSON.
        Valida todos los valores antes de guardar.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        # Validar configuración antes de guardar
        self._validate_config()
        
        try:
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file, indent=4)
            logging.info("Configuración guardada correctamente")
            return True
        except (IOError, OSError) as e:
            logging.error(f"Error al guardar configuración: {e}")
            return False
    
    def _validate_config(self):
        """
        Valida toda la configuración y ajusta valores fuera de rango.
        Registra advertencias para valores inválidos.
        """
        # Validar configuración de juego
        for section in ["game", "visual"]:
            if section in self._CONFIG_RANGES:
                for key, range_info in self._CONFIG_RANGES[section].items():
                    if key in self.config[section]:
                        value = self.config[section][key]
                        if isinstance(value, (int, float)):
                            if value < range_info["min"]:
                                logging.warning(f"Valor fuera de rango para {section}.{key}: {value} < {range_info['min']}. Ajustando al mínimo.")
                                self.config[section][key] = range_info["min"]
                            elif value > range_info["max"]:
                                logging.warning(f"Valor fuera de rango para {section}.{key}: {value} > {range_info['max']}. Ajustando al máximo.")
                                self.config[section][key] = range_info["max"]
        
        # Validar tema
        if "theme" in self.config["visual"]:
            theme = self.config["visual"]["theme"]
            if theme not in self.config["themes"]:
                logging.warning(f"Tema no válido: {theme}. Cambiando al tema por defecto.")
                self.config["visual"]["theme"] = "default"
        
        # Asegurar que todos los controles son únicos
        control_values = list(self.config["controls"].values())
        if len(control_values) != len(set(control_values)):
            logging.warning("Se detectaron teclas de control duplicadas. Esto puede causar comportamientos inesperados.")
    
    def get_value(self, section, key, default=None):
        """
        Obtiene un valor de configuración.
        
        Args:
            section (str): Sección de la configuración
            key (str): Clave del valor
            default: Valor por defecto si no se encuentra
            
        Returns:
            El valor de configuración o el valor por defecto
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set_value(self, section, key, value):
        """
        Establece un valor de configuración.
        
        Args:
            section (str): Sección de la configuración
            key (str): Clave del valor
            value: Nuevo valor
            
        Returns:
            bool: True si se estableció correctamente, False en caso contrario
        """
        try:
            self.config[section][key] = value
            return True
        except KeyError:
            return False
    
    def get_theme(self):
        """
        Obtiene el tema de colores actual.
        
        Returns:
            dict: Diccionario con los colores del tema
        """
        theme_name = self.get_value("visual", "theme", "default")
        return self.config["themes"].get(theme_name, self.config["themes"]["default"])
    
    def get_available_themes(self):
        """
        Obtiene la lista de temas disponibles.
        
        Returns:
            list: Lista de nombres de temas
        """
        return list(self.config["themes"].keys())
    
    def reset_to_defaults(self):
        """
        Restablece la configuración a los valores por defecto.
        
        Returns:
            bool: True si se restableció correctamente
        """
        self.config = DEFAULT_CONFIG.copy()
        return self.save_config()

class ConfigUI:
    """
    Clase que maneja la interfaz de usuario para la configuración.
    """
    
    def __init__(self, window, config_manager, ui_manager):
        """
        Inicializa la interfaz de configuración.
        
        Args:
            window (pygame.Surface): Superficie de la ventana
            config_manager (ConfigManager): Gestor de configuración
            ui_manager (GameUI): Gestor de interfaz principal
        """
        self.window = window
        self.config_manager = config_manager
        self.ui_manager = ui_manager
        
        # Estado de la interfaz de configuración
        self.current_section = "general"  # Sección actual
        self.sections = ["general", "visual", "controls", "themes"]
        self.selected_option = 0  # Opción seleccionada
        self.is_editing = False   # Si se está editando un valor
        
        # Opciones por sección
        self.options = {
            "general": [
                {"name": "Velocidad inicial", "key": ["game", "initial_fall_speed"], "type": "int", "min": 10, "max": 300},
                {"name": "Decremento velocidad", "key": ["game", "fall_speed_decrement"], "type": "int", "min": 1, "max": 20},
                {"name": "Velocidad mínima", "key": ["game", "min_fall_speed"], "type": "int", "min": 1, "max": 10},
                {"name": "Vista previa piezas", "key": ["game", "next_pieces_preview"], "type": "int", "min": 1, "max": 5},
            ],
            "visual": [
                {"name": "Ancho ventana", "key": ["visual", "window_width"], "type": "int", "min": 640, "max": 1920},
                {"name": "Alto ventana", "key": ["visual", "window_height"], "type": "int", "min": 480, "max": 1080},
                {"name": "Tamaño celda", "key": ["visual", "cell_size"], "type": "int", "min": 15, "max": 40},
                {"name": "Mostrar cuadrícula", "key": ["visual", "show_grid"], "type": "bool"},
                {"name": "Mostrar pieza fantasma", "key": ["visual", "show_ghost_piece"], "type": "bool"},
                {"name": "Efectos puntuación", "key": ["visual", "show_score_effects"], "type": "bool"},
                {"name": "Tema", "key": ["visual", "theme"], "type": "theme"},
            ],
            "controls": [
                {"name": "Mover izquierda", "key": ["controls", "move_left"], "type": "key"},
                {"name": "Mover derecha", "key": ["controls", "move_right"], "type": "key"},
                {"name": "Mover abajo", "key": ["controls", "move_down"], "type": "key"},
                {"name": "Rotar", "key": ["controls", "rotate"], "type": "key"},
                {"name": "Caída rápida", "key": ["controls", "hard_drop"], "type": "key"},
                {"name": "Pausa", "key": ["controls", "pause"], "type": "key"},
                {"name": "Salir", "key": ["controls", "exit"], "type": "key"},
            ],
            "themes": [
                {"name": "Restablecer ajustes", "action": "reset", "type": "action"},
                {"name": "Guardar y salir", "action": "save", "type": "action"},
                {"name": "Cancelar", "action": "cancel", "type": "action"},
            ]
        }
    
    def draw(self):
        """
        Dibuja la interfaz de configuración.
        """
        # Fondo
        self.window.fill(self.config_manager.get_theme()["bg_color"])
        
        # Título
        title_text = self.ui_manager.title_font.render("CONFIGURACIÓN", True, self.config_manager.get_theme()["text_color"])
        title_rect = title_text.get_rect(center=(self.window.get_width() // 2, 50))
        self.window.blit(title_text, title_rect)
        
        # Pestañas de secciones
        tab_width = self.window.get_width() // len(self.sections)
        for i, section in enumerate(self.sections):
            # Color y fuente según si está seleccionada
            if section == self.current_section:
                color = self.config_manager.get_theme()["piece_colors"]["T"]
                font = self.ui_manager.medium_font
                # Dibujar fondo de pestaña seleccionada
                pygame.draw.rect(
                    self.window,
                    self.config_manager.get_theme()["ui_bg_color"],
                    (i * tab_width, 100, tab_width, 40)
                )
            else:
                color = self.config_manager.get_theme()["text_color"]
                font = self.ui_manager.small_font
            
            # Dibujar nombre de sección
            section_text = font.render(section.capitalize(), True, color)
            section_rect = section_text.get_rect(center=(i * tab_width + tab_width // 2, 120))
            self.window.blit(section_text, section_rect)
        
        # Separador
        pygame.draw.line(
            self.window,
            self.config_manager.get_theme()["border_color"],
            (0, 140),
            (self.window.get_width(), 140),
            2
        )
        
        # Opciones de la sección actual
        y_pos = 180
        for i, option in enumerate(self.options[self.current_section]):
            # Destacar opción seleccionada
            if i == self.selected_option:
                color = self.config_manager.get_theme()["piece_colors"]["O"]
                # Fondo para la opción seleccionada
                pygame.draw.rect(
                    self.window,
                    tuple(max(0, c - 160) for c in self.config_manager.get_theme()["bg_color"]),  # Más oscuro
                    (100, y_pos - 5, self.window.get_width() - 200, 40)
                )
            else:
                color = self.config_manager.get_theme()["text_color"]
            
            # Nombre de la opción
            option_text = self.ui_manager.medium_font.render(option["name"], True, color)
            self.window.blit(option_text, (120, y_pos))
            
            # Valor actual
            if "action" not in option:
                value = self._get_option_value(option)
                value_text = self._format_option_value(option, value)
                value_surface = self.ui_manager.medium_font.render(value_text, True, color)
                self.window.blit(value_surface, (self.window.get_width() - 300, y_pos))
            
            y_pos += 50
        
        # Instrucciones
        instructions = "↑↓: Navegar  ←→: Cambiar sección  ENTER: Seleccionar  ESC: Volver"
        if self.is_editing:
            instructions = "←→: Ajustar valor  ENTER: Confirmar  ESC: Cancelar"
            
        inst_text = self.ui_manager.small_font.render(instructions, True, self.config_manager.get_theme()["text_color"])
        inst_rect = inst_text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() - 30))
        self.window.blit(inst_text, inst_rect)
    
    def handle_input(self, event):
        """
        Maneja la entrada de usuario para la configuración.
        
        Args:
            event (pygame.event.Event): Evento de teclado
            
        Returns:
            str or None: Acción a realizar o None
        """
        if self.is_editing:
            return self._handle_editing_input(event)
        else:
            return self._handle_navigation_input(event)
    
    def _handle_navigation_input(self, event):
        """
        Maneja la navegación por el menú de configuración.
        
        Args:
            event (pygame.event.Event): Evento de teclado
            
        Returns:
            str or None: Acción a realizar o None
        """
        if event.type == pygame.KEYDOWN:
            # Navegación vertical (opciones)
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options[self.current_section])
                return None
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options[self.current_section])
                return None
                
            # Navegación horizontal (secciones)
            elif event.key == pygame.K_LEFT:
                current_index = self.sections.index(self.current_section)
                self.current_section = self.sections[(current_index - 1) % len(self.sections)]
                self.selected_option = 0
                return None
            elif event.key == pygame.K_RIGHT:
                current_index = self.sections.index(self.current_section)
                self.current_section = self.sections[(current_index + 1) % len(self.sections)]
                self.selected_option = 0
                return None
                
            # Selección
            elif event.key == pygame.K_RETURN:
                selected = self.options[self.current_section][self.selected_option]
                
                # Si es una acción
                if "action" in selected:
                    if selected["action"] == "reset":
                        self.config_manager.reset_to_defaults()
                        return "reset"
                    elif selected["action"] == "save":
                        self.config_manager.save_config()
                        return "save"
                    elif selected["action"] == "cancel":
                        return "cancel"
                else:
                    # Iniciar edición
                    self.is_editing = True
                    return None
                    
            # Volver
            elif event.key == pygame.K_ESCAPE:
                return "cancel"
                
        return None
    
    def _handle_editing_input(self, event):
        """
        Maneja la edición de un valor de configuración.
        
        Args:
            event (pygame.event.Event): Evento de teclado
            
        Returns:
            str or None: Acción a realizar o None
        """
        if event.type == pygame.KEYDOWN:
            selected = self.options[self.current_section][self.selected_option]
            
            # Confirmar
            if event.key == pygame.K_RETURN:
                self.is_editing = False
                return None
                
            # Cancelar
            elif event.key == pygame.K_ESCAPE:
                self.is_editing = False
                return None
                
            # Ajustar valor según tipo
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and "key" in selected:
                section, key = selected["key"]
                current_value = self.config_manager.get_value(section, key)
                
                if selected["type"] == "int":
                    # Incrementar/decrementar valor numérico
                    step = 5 if key in ["window_width", "window_height"] else 1
                    min_val = selected.get("min", 0)
                    max_val = selected.get("max", 1000)
                    
                    if event.key == pygame.K_LEFT:
                        new_value = max(min_val, current_value - step)
                    else:
                        new_value = min(max_val, current_value + step)
                        
                    self.config_manager.set_value(section, key, new_value)
                    
                elif selected["type"] == "bool":
                    # Alternar valor booleano
                    self.config_manager.set_value(section, key, not current_value)
                    
                elif selected["type"] == "theme":
                    # Cambiar tema
                    themes = self.config_manager.get_available_themes()
                    current_index = themes.index(current_value) if current_value in themes else 0
                    
                    if event.key == pygame.K_LEFT:
                        new_index = (current_index - 1) % len(themes)
                    else:
                        new_index = (current_index + 1) % len(themes)
                        
                    self.config_manager.set_value(section, key, themes[new_index])
                    
                elif selected["type"] == "key":
                    # Para teclas, cambiar a modo de captura
                    return "capture_key"
            
            # Capturar tecla
            elif "key" in selected and selected["type"] == "key":
                section, key = selected["key"]
                self.config_manager.set_value(section, key, event.key)
                self.is_editing = False
                
        return None
    
    def _get_option_value(self, option):
        """
        Obtiene el valor actual de una opción.
        
        Args:
            option (dict): Opción de configuración
            
        Returns:
            El valor actual
        """
        if "key" in option:
            section, key = option["key"]
            return self.config_manager.get_value(section, key)
        return None
    
    def _format_option_value(self, option, value):
        """
        Formatea el valor de una opción para mostrar.
        
        Args:
            option (dict): Opción de configuración
            value: Valor a formatear
            
        Returns:
            str: Valor formateado
        """
        if option["type"] == "bool":
            return "Activado" if value else "Desactivado"
        elif option["type"] == "key":
            # Convertir código de tecla a nombre
            try:
                return pygame.key.name(value).upper()
            except:
                return "INDEFINIDA"
        elif option["type"] == "theme":
            return value.capitalize()
        else:
            return str(value)

