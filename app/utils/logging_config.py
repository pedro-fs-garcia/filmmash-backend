import logging
import os

# Cria a pasta logs se ela não existir
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,  # Nível mínimo (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato do log
    handlers=[
        logging.FileHandler("logs/app.log"),  # Log geral
        logging.FileHandler("logs/error.log", mode="a"),  # Log de erros
        logging.StreamHandler()  # Saída para o terminal
    ],
)

# Log específico para erros
error_logger = logging.getLogger("error")
error_logger.setLevel(logging.ERROR)

# Log geral da aplicação
app_logger = logging.getLogger("app")