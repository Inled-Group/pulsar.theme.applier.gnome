#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import gi
import logging
from pathlib import Path

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('macos_theme_applier')

# Importar librerías necesarias de GNOME
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gio', '2.0')
    from gi.repository import Gtk, Gio
except Exception as e:
    logger.error(f"Error al importar bibliotecas GTK: {e}")
    logger.error("Instalando dependencias necesarias...")
    os.system('apt-get update && apt-get install -y python3-gi gir1.2-gtk-3.0')
    logger.error("Por favor, vuelve a ejecutar el script")
    sys.exit(1)

class MacOSThemeApplier:
    def __init__(self):
        # Detectar automáticamente el nombre de usuario
        self.username = os.getenv("USER") or os.getenv("USERNAME")
            
        # Configurar la ruta del directorio home
        self.home_dir = Path.home()
        
        # Rutas de los temas
        self.themes_dir = self.home_dir / ".themes"
        self.icons_dir = self.home_dir / ".icons"
        
        # Nombre de los temas predefinidos (como se solicitaron)
        self.cursor_theme = "Pulsar.cursormac"
        self.icon_theme = "WhiteSur-dark"
        self.shell_theme = "WhiteSur-Dark"
        self.gtk_theme = "WhiteSur-Dark"
        
        # Verificar que los temas existen
        self.check_themes_exist()
        
        # Configurar la interfaz de gsettings
        self.gsettings_interface = Gio.Settings.new("org.gnome.desktop.interface")
        try:
            self.gsettings_shell = Gio.Settings.new("org.gnome.shell.extensions.user-theme")
            self.shell_theme_supported = True
        except Exception:
            logger.warning("La extensión user-theme no está instalada. No se podrá cambiar el tema del shell.")
            self.shell_theme_supported = False
    
    def check_themes_exist(self):
        """Verifica que los temas existen en las carpetas correspondientes"""
        # Verificar cursor
        cursor_path = self.icons_dir / self.cursor_theme
        if not cursor_path.exists():
            logger.warning(f"No se encontró el tema de cursor {self.cursor_theme} en {self.icons_dir}")
            
        # Verificar iconos
        icon_path = self.icons_dir / self.icon_theme
        if not icon_path.exists():
            logger.warning(f"No se encontró el tema de iconos {self.icon_theme} en {self.icons_dir}")
            
        # Verificar tema GTK
        gtk_path = self.themes_dir / self.gtk_theme
        if not gtk_path.exists():
            logger.warning(f"No se encontró el tema GTK {self.gtk_theme} en {self.themes_dir}")
            
        # Verificar tema Shell
        shell_path = self.themes_dir / self.shell_theme
        if not shell_path.exists():
            logger.warning(f"No se encontró el tema Shell {self.shell_theme} en {self.themes_dir}")
    
    def apply_themes(self):
        """Aplica todos los temas configurados"""
        success = True
        
        # Aplicar tema de cursor
        if not self.apply_cursor_theme():
            success = False
        
        # Aplicar tema de iconos
        if not self.apply_icon_theme():
            success = False
        
        # Aplicar tema GTK
        if not self.apply_gtk_theme():
            success = False
        
        # Aplicar tema Shell
        if not self.apply_shell_theme():
            success = False
        
        return success
    
    def apply_cursor_theme(self):
        """Aplica el tema de cursor"""
        try:
            logger.info(f"Aplicando tema de cursor: {self.cursor_theme}")
            self.gsettings_interface.set_string("cursor-theme", self.cursor_theme)
            return True
        except Exception as e:
            logger.error(f"Error al aplicar el tema de cursor: {e}")
            return False
    
    def apply_icon_theme(self):
        """Aplica el tema de iconos"""
        try:
            logger.info(f"Aplicando tema de iconos: {self.icon_theme}")
            self.gsettings_interface.set_string("icon-theme", self.icon_theme)
            return True
        except Exception as e:
            logger.error(f"Error al aplicar el tema de iconos: {e}")
            return False
    
    def apply_gtk_theme(self):
        """Aplica el tema GTK"""
        try:
            logger.info(f"Aplicando tema GTK: {self.gtk_theme}")
            self.gsettings_interface.set_string("gtk-theme", self.gtk_theme)
            return True
        except Exception as e:
            logger.error(f"Error al aplicar el tema GTK: {e}")
            return False
    
    def apply_shell_theme(self):
        """Aplica el tema Shell"""
        if not self.shell_theme_supported:
            logger.warning("No se puede aplicar el tema del shell porque la extensión user-theme no está disponible")
            return False
        
        try:
            logger.info(f"Aplicando tema Shell: {self.shell_theme}")
            self.gsettings_shell.set_string("name", self.shell_theme)
            return True
        except Exception as e:
            logger.error(f"Error al aplicar el tema Shell: {e}")
            return False

def main():
    """Función principal para aplicar los temas automáticamente"""
    # Crear instancia del aplicador de temas con detección automática de usuario
    theme_applier = MacOSThemeApplier()
    
    # Aplicar temas
    if theme_applier.apply_themes():
        logger.info("✅ Temas aplicados correctamente")
        print("✅ Temas de MacOS aplicados correctamente")
        return 0
    else:
        logger.error("❌ Error al aplicar algunos temas")
        print("❌ Error al aplicar algunos temas. Revisa los logs para más información.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
