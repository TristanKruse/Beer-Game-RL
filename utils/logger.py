import logging

def setup_logger():
    """
    Sets up the logger with the specified configuration.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(lineno)d - %(message)s')
    return logging.getLogger()