import logging
import coloredlogs

# Logger initialisieren
logger = logging.getLogger(__name__)

# Farben für verschiedene Protokollarten festlegen
level_styles = {
    'debug': {'color': 'white'},
    'info': {'color': 'blue'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True}
}

# Einstellungen für coloredlogs installieren
coloredlogs.install(level='DEBUG', logger=logger, fmt='%(message)s', level_styles=level_styles)
