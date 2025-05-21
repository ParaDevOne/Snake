# score.py
# Módulo para manejar el sistema de puntuación y récords del Tetris
# Autor: [ParaDevOne]
# Fecha: Mayo 2025
# Licencia: Simplified Open License (SOL) v1.0

import json
import os
import datetime
import logging

class ScoreManager:
    """
    Clase que gestiona el sistema de puntuación y récords del juego.
    Maneja la carga, guardado y actualización de puntuaciones.
    """
    
    def __init__(self, highscore_file="highscores.json", max_records=10):
        """
        Inicializa el gestor de puntuaciones.
        
        Args:
            highscore_file (str): Nombre del archivo donde se guardan las puntuaciones
            max_records (int): Número máximo de récords a mantener
        """
        self.highscore_file = highscore_file
        self.max_records = max_records
        self.current_score = 0
        self.highscores = []
        
        # Cargar puntuaciones previas
        self.load_highscores()
    
    def load_highscores(self):
        """
        Carga las puntuaciones máximas desde el archivo JSON.
        Si el archivo no existe o está corrupto, inicializa una lista vacía.
        """
        try:
            if os.path.exists(self.highscore_file):
                with open(self.highscore_file, 'r') as file:
                    self.highscores = json.load(file)
                    # Verificar estructura
                    if not isinstance(self.highscores, list):
                        self.highscores = []
            else:
                self.highscores = []
                
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error al cargar puntuaciones: {e}")
            self.highscores = []
    
    def save_highscores(self):
        """
        Guarda las puntuaciones máximas en el archivo JSON.
        Maneja errores de escritura y permisos.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.highscore_file, 'w') as file:
                json.dump(self.highscores, file, indent=4)
            return True
        except (IOError, OSError) as e:
            logging.error(f"Error al guardar puntuaciones: {e}")
            return False
    
    def update_score(self, points):
        """
        Actualiza la puntuación actual del juego.
        
        Args:
            points (int): Puntos a añadir
            
        Returns:
            int: Puntuación actualizada
        """
        self.current_score += points
        return self.current_score
    
    def reset_score(self):
        """
        Reinicia la puntuación actual a cero.
        """
        self.current_score = 0
    
    def get_current_score(self):
        """
        Obtiene la puntuación actual.
        
        Returns:
            int: Puntuación actual
        """
        return self.current_score
    
    def get_highscore(self):
        """
        Obtiene la puntuación más alta registrada.
        
        Returns:
            int: Puntuación más alta o 0 si no hay récords
        """
        if not self.highscores:
            return 0
        return max(entry["score"] for entry in self.highscores)
    
    def is_highscore(self, score=None):
        """
        Verifica si una puntuación es récord.
        
        Args:
            score (int, opcional): Puntuación a verificar. Si es None, se usa la puntuación actual.
            
        Returns:
            bool: True si es récord, False en caso contrario
        """
        if score is None:
            score = self.current_score
            
        # Si no hay suficientes récords, cualquier puntuación es récord
        if len(self.highscores) < self.max_records:
            return True
            
        # Verificar si la puntuación supera el récord más bajo
        lowest_score = min(entry["score"] for entry in self.highscores)
        return score > lowest_score
    
    def add_highscore(self, player_name, score=None, level=1, lines=0):
        """
        Añade una nueva puntuación al ranking.
        
        Args:
            player_name (str): Nombre del jugador
            score (int, opcional): Puntuación. Si es None, se usa la puntuación actual.
            level (int): Nivel alcanzado
            lines (int): Líneas eliminadas
            
        Returns:
            bool: True si se añadió como récord, False en caso contrario
        """
        if score is None:
            score = self.current_score
            
        # Verificar si es récord
        if not self.is_highscore(score) and len(self.highscores) >= self.max_records:
            return False
            
        # Crear entrada de récord
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "player": player_name,
            "score": score,
            "level": level,
            "lines": lines,
            "date": timestamp
        }
        
        # Añadir a la lista
        self.highscores.append(new_entry)
        
        # Ordenar y limitar
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        if len(self.highscores) > self.max_records:
            self.highscores = self.highscores[:self.max_records]
            
        # Guardar
        self.save_highscores()
        return True
    
    def get_rankings(self):
        """
        Obtiene la lista de rankings ordenada por puntuación.
        
        Returns:
            list: Lista de diccionarios con las puntuaciones
        """
        return sorted(self.highscores, key=lambda x: x["score"], reverse=True)
    
    def format_score(self, score=None):
        """
        Formatea una puntuación para mostrar en pantalla.
        
        Args:
            score (int, opcional): Puntuación a formatear. Si es None, se usa la puntuación actual.
            
        Returns:
            str: Puntuación formateada
        """
        if score is None:
            score = self.current_score
            
        # Formatear con separadores de miles
        return f"{score:,}".replace(",", ".")

