from enum import IntEnum

from utils.console import ConsoleTextStyle, FourBitConsoleColors, color_text


__all__ = (
    'LogType',
    'Logger'
)


class LogType(IntEnum):
    """
        A type of log message

        :cvar debug: Message useful while debugging, but obnoxious everywhere else
        :cvar info: Info for the user
        :cvar warning: A possible mistake the user made
        :cvar critical: Something that prevents the site from being generated
    """

    debug = 0
    info = 1
    warning = 2
    critical = 3


class Logger:
    """
        Handles logging messages to the console

        :cvar __level: The current log level
        :cvar __log_styles: The `ConsoleTextStyle` to use for each log type
    """

    def __new__(cls, *args, **kwargs):
        print("Logger is a static class!")
        return None

    __level: LogType = LogType.info
    __log_styles: dict[LogType, ConsoleTextStyle] = {
        LogType.debug: ConsoleTextStyle(fg_color=FourBitConsoleColors.CYAN),
        LogType.info: ConsoleTextStyle(fg_color=FourBitConsoleColors.WHITE),
        LogType.warning: ConsoleTextStyle(fg_color=FourBitConsoleColors.YELLOW),
        LogType.critical: ConsoleTextStyle(fg_color=FourBitConsoleColors.RED, bold=True)
    }

    @classmethod
    def update_level_from_string(level_str: str) -> None:
        cls.update_level(['debug', 'info', 'warning', 'critical'].index(level_str.lower()))

    @classmethod
    def update_level(cls, new_level: LogType) -> None:
        cls.__level = new_level

    @classmethod
    def log(cls, message: str, log_type: LogType) -> None:
        """
            Logs a message to the console if the passed type is above the current level

            :param message: Message to print
            :type message: str
            :param log_type: The type of message to log
            :type log_typa: LogType
        """

        # TODO: Log to file eventually
        if int(log_type) >= int(cls.__level):
            cls.__print(message, log_type)

    @classmethod
    def log_error(cls, message: str) -> None:
        cls.log(message, LogType.critical)

    @classmethod
    def log_warning(cls, message: str) -> None:
        cls.log(message, LogType.warning)

    @classmethod
    def log_info(cls, message: str) -> None:
        cls.log(message, LogType.info)

    @classmethod
    def log_debug(cls, message: str) -> None:
        cls.log(message, LogType.debug)
            
    @classmethod
    def force_log(cls, message: str, log_type: LogType):
        """
            Similar to `log()`, but doesn't check against `__level`
        """

        cls.__print(message, log_type)

    @classmethod
    def __print(cls, message: str, log_type: LogType):
        print(color_text(message, cls.__log_styles.get(log_type), reset=True))
