import logging
import coloredlogs
from colorama import Fore, Style, init

init(autoreset=True)


class CustomFormatter(coloredlogs.ColoredFormatter):
    """
    CustomFormatter extends coloredlogs.ColoredFormatter to customize the log format.

    Attributes:
        None

    Methods:
        format(self, record): Formats the log record.

    """
    def format(self, record):
        s = super().format(record)
        s = s.replace(" - ", format_text(" - ", Fore.LIGHTBLACK_EX))
        filename_lineno = format_text(f"{record.filename}-{record.lineno}", Fore.WHITE)
        s = s.replace(f"{record.filename} - {record.lineno}", filename_lineno)
        levelname_color = self.level_styles.get(record.levelname.lower(), {}).get('color', 'white')
        s = s.replace(record.levelname,
                      format_text(record.levelname, getattr(Fore, levelname_color.upper(), Fore.WHITE)))
        s = s.replace(".py:", format_text(".py:", Fore.LIGHTBLACK_EX))
        return s


def format_text(text, fore_color):
    """
    Apply the given fore_color to the provided text.

    :param text: The input text to be formatted.
    :param fore_color: The color to apply to the text.
    :return: The formatted text with the specified color.
    """
    return fore_color + text + Style.RESET_ALL


def config_logger(logger):
    """
    Configure the logger with specific formatting and level settings.

    Parameters:
    - logger (logging.Logger): The logger object to configure.

    Returns:
    - None
    """
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles.update({'name': {'color': 'white'}, 'filename': {'color': 'white'}, 'lineno': {'color': 'white'}})

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


# Initialize and configure logger
logger = logging.getLogger(__name__)
config_logger(logger)
