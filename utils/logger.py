from enum import IntEnum

from utils.console import ConsoleTextStyle, FourBitConsoleColors, color_text


class LogType(IntEnum):
    debug = 0
    info = 1
    warning = 2
    critical = 3


class Logger:

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
    def update_level(cls, new_level: LogType) -> None:
        cls.__level = new_level

    @classmethod
    def log(cls, message: str, log_type: LogType) -> None:
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
        cls.__print(message, log_type)

    @classmethod
    def __print(cls, message: str, log_type: LogType):
        print(color_text(message, cls.__log_styles.get(log_type), reset=True))
