import logging
import sys
import os
from dotenv import load_dotenv


def setup_logger():
    """
    Configura o sistema de logging da aplicação.

    - Define o nível de log com base na variável de ambiente `API_ENV`:
        - DEBUG se em desenvolvimento.
        - INFO para outros ambientes.
    - Cria dois handlers:
        - Um para saída padrão (stdout).
        - Outro para um arquivo de log em `logs/api.log`.
    - Formato do log: [timestamp] [nível] [nome do logger] mensagem
    """

    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()

    # Define o nível de log com base no ambiente
    level = logging.DEBUG if os.getenv("API_ENV") == "development" else logging.INFO

    # Obtém o logger raiz
    logger = logging.getLogger()
    logger.setLevel(level)

    # Define caminho do arquivo de log (um nível acima de `core/`, na pasta `logs/`)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.dirname(BASE_DIR)
    log_file_path = os.path.join(APP_DIR, "logs", "api.log")

    # Garante que o diretório exista
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Evita adicionar múltiplos handlers se já configurado
    if not logger.handlers:
        # Define o formato dos logs
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )

        # Handler para saída padrão (útil em desenvolvimento ou logs do Docker)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Handler para arquivo de log
        file_handler = logging.FileHandler(filename=log_file_path, mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
