import logging
import sys
import os
from dotenv import load_dotenv

def setup_logger():
    """Configura o logger com saída para stdout e um arquivo de log."""

    load_dotenv()

    level = logging.DEBUG if os.getenv('API_ENV') == 'development' else logging.INFO

    logger = logging.getLogger()
    logger.setLevel(level)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.dirname(BASE_DIR)

    log_file_path = os.path.join(APP_DIR, 'logs', 'api.log')
    
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Ensure that we don't add duplicate handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
        # Add a handler that writes to stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Add a handler that writes to a file
        file_handler = logging.FileHandler(filename=log_file_path, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)