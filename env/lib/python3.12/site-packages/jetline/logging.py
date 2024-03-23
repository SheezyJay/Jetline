import logging
import coloredlogs
from colorama import Fore, Style, init


init(autoreset=True)

class CustomFormatter(coloredlogs.ColoredFormatter):
    """
    Log message formatter to apply custom color rules.
    """

    def format(self, record):
        # Apply standard formatting first
        s = super().format(record)


        s = s.replace(" - ", Fore.LIGHTBLACK_EX + " - " + Style.RESET_ALL)

        # Coloring filename and lineno together for consistency
        filename_lineno = f"{Fore.WHITE}{record.filename}-{record.lineno}{Style.RESET_ALL}"
        s = s.replace(f"{record.filename} - {record.lineno}", filename_lineno)

        # Applying color to levelname according to the level_styles
        levelname_color = self.level_styles.get(record.levelname.lower(), {}).get('color', 'white')
        s = s.replace(record.levelname, getattr(Fore, levelname_color.upper(), Fore.WHITE) + record.levelname + Style.RESET_ALL)

        # Ensuring date is colored the same as filename
        s = s.replace(".py:", Fore.LIGHTBLACK_EX + ".py:" + Style.RESET_ALL)

        return s

# Initialize logger
logger = logging.getLogger(__name__)

field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
field_styles['name'] = {'color': 'white'}
field_styles['filename'] = {'color': 'white'}
field_styles['lineno'] = {'color': 'white'}

# Set colors for different log levels
level_styles = {
    'debug': {'color': 'green'},
    'info': {'color': 'blue'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True},
}

fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d'
datefmt = '%Y-%m-%d %H:%M:%S'

coloredlogs.install(level='DEBUG',
                    logger=logger,
                    fmt=fmt,
                    datefmt=datefmt,
                    level_styles=level_styles,
                    field_styles=field_styles)

for handler in logger.handlers:
    handler.setFormatter(CustomFormatter(fmt, datefmt, level_styles=level_styles, field_styles=field_styles))

handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter(fmt, datefmt, level_styles=level_styles, field_styles=field_styles))
logger.addHandler(handler)
