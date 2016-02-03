import logging

def init_logger(logger_name, level, handler):
    log_format = (
        '-' * 80 + '\n' +
        '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
        '%(message)s\n' +
        '-' * 80
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(log_format))

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    del logger.handlers[:]

    # add passing default handler
    logger.addHandler(handler)

    return logger
