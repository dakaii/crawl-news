import logging


def get_logger(logger_name, fname='err.log', level=logging.ERROR):
    logger = logging.getLogger(logger_name)

    f_handler = logging.FileHandler(fname)
    f_handler.setLevel(level)
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(fmt)
    logger.addHandler(f_handler)
    return logger
