
import logging

LOGGER_NAME = 'icarus_dcc'

def configure_logging(log_level: int = logging.INFO) -> None:
    
    logger = logging.getLogger(LOGGER_NAME)
    
    if not any(type(h) is logging.StreamHandler for h in logger.handlers):
        stream_handler = logging.StreamHandler()
    
        logger.addHandler(stream_handler)

    logger.propagate = False
    _set_log_level(log_level=log_level)

def _build_formatter(*, log_level: int) -> logging.Formatter:
    
    fmt_string = (
        '%(name)s | %(levelname)s | %(message)s'
        if log_level == logging.DEBUG
        else '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )

    return logging.Formatter(fmt=fmt_string)

def _set_log_level(*, log_level: int) -> None:
    
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level)
    
    formatter = _build_formatter(log_level=log_level)
    
    for handler in logger.handlers:
        handler.setLevel(log_level)
        handler.setFormatter(formatter)

def set_level(*, level_name: str) -> None:
    
    try:
        level = getattr(logging, level_name.upper())
    except AttributeError as error:
        raise ValueError(f'Unsupported log level: "{level_name}"') from error
    
    _set_log_level(log_level=level)
