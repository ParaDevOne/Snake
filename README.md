# Tetris

> **Aviso:** Este juego está optimizado y ha sido probado principalmente en Windows. Más información **abajo**.

![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)
![License](https://img.shields.io/badge/license-SOL%201.0-brightgreen.svg)
![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)

Un juego clásico de Tetris implementado en Python usando Pygame, con una arquitectura modular y características modernas.

![Tetris Screenshot](./content/images/tetris_screenshot.png)

## Descripción

Esta implementación del clásico juego Tetris incluye todas las funcionalidades originales: siete piezas estándar, sistema de rotación, incremento de dificultad por niveles y sistema de puntuación. Además, incorpora funciones adicionales como previsualización de próximas piezas, guardado de récords y una interfaz de usuario intuitiva.

**Versión 1.2 del juego**

## Requisitos del Sistema

- Python 3.7 o superior
- Sistema operativo: Windows, Linux o MacOS
> **Aviso:** Aunque está optimizado para Windows y ha sido probado en este sistema, puede funcionar en otros sistemas operativos (como Linux o MacOS), pero no se garantiza la misma experiencia de usuario. Es necesario ejecutarlo desde el código fuente para asegurar la compatibilidad. En Windows, puedes descargar el ejecutable en la sección de [releases](https://github.com/ParaDevOne/Tetris/releases).
- Espacio en disco: ~30 MB
- Memoria RAM: 100 MB o más (sin contar la que usa el sistema operativo)

## Instalación

1. Clona o descarga este repositorio.
2. Asegúrate de tener Python instalado en tu sistema o descárgalo desde la sección de releases.
3. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   ```
4. Activa el entorno virtual:
   - En Windows:
     ```
     .\venv\Scripts\activate
     ```
   - En Linux/MacOS:
     ```
     source venv/bin/activate
     ```
5. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Cómo Jugar

Para iniciar el juego, ejecuta:
```
python main.py
```

### Controles

- **Flechas izquierda/derecha**: Mover la pieza horizontalmente
- **Flecha arriba**: Rotar la pieza
- **Flecha abajo**: Caída acelerada (soft drop)
- **Espacio**: Caída instantánea (hard drop)
- **P**: Pausar el juego
- **ESC**: Volver al menú principal

## Características Principales

- **7 Piezas Clásicas**: I, O, T, S, Z, J, L con sus rotaciones correspondientes
- **Previsualización**: Muestra las siguientes 3 piezas
- **Sistema de Puntuación**:
  - Puntos por pieza colocada
  - Bonificación por líneas eliminadas (especialmente por Tetris - 4 líneas)
  - Puntos extra por hard drop
- **Dificultad Progresiva**: La velocidad aumenta con cada nivel
- **Récords**: Almacena las mejores puntuaciones con nombre del jugador
- **Interfaz Moderna**: Menús intuitivos y diseño visual atractivo

## Estructura del Proyecto

El juego está estructurado de forma modular para facilitar su mantenimiento y extensibilidad:

- **main.py**: Punto de entrada y bucle principal del juego
- **board.py**: Lógica del tablero y gestión de colisiones
- **pieces.py**: Definición y comportamiento de las piezas
- **score.py**: Sistema de puntuación y récords
- **ui.py**: Interfaz gráfica
- **constants.py**: Configuraciones y constantes

## Licencia

Este proyecto está disponible bajo la **Simplified Open License (SOL) versión 1.0**.

Esta licencia permite:
- Uso libre del software para cualquier propósito, incluyendo comercial
- Modificación y distribución del código
- Creación de trabajos derivados sin obligación de hacerlos open source

Con la única condición de mantener la atribución al autor original.

Para más detalles, consulta el archivo [LICENSE](LICENSE) incluido en este repositorio.

## Compatibilidad y plataforma

- Aunque el juego está optimizado para Windows, se han realizado esfuerzos para soportar Linux y MacOS de forma básica.
- Algunas funciones avanzadas pueden no estar disponibles o no funcionar correctamente fuera de Windows debido a dependencias específicas de drivers y librerías.
- Se recomienda usar Windows para la mejor experiencia.

## Créditos

Desarrollado por ParaDevOne. ¡Gracias por jugar y contribuir con sugerencias o reportes de errores!
