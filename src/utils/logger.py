import os
import time
import traceback
from datetime import datetime
from functools import wraps
from loguru import logger
import pandas as pd

# Configuração inicial do logger

def call_logger(log_folder):
    """Decorador para capturar logs automaticamente e salvar em uma pasta específica."""
    def decorator(func):
        @wraps(func)  # Preserva os metadados da função original
        def wrapper(*args, **kwargs):
            # Cria a pasta de logs se não existir
            os.makedirs(f"logs/{log_folder}", exist_ok=True)
            log_file = os.path.join(f"logs/{log_folder}", f"{datetime.now().strftime('%Y-%m-%d')}.log")
            logger.add(log_file, rotation="10 MB", level="INFO")

            # Função para substituir DataFrames por uma mensagem genérica
            def sanitize_args(args):
                sanitized_args = []
                for arg in args:
                    if isinstance(arg, pd.DataFrame):
                        sanitized_args.append("<DataFrame>")
                    else:
                        sanitized_args.append(arg)
                return tuple(sanitized_args)

            # Sanitiza os argumentos
            sanitized_args = sanitize_args(args)
            sanitized_kwargs = {k: ("<DataFrame>" if isinstance(v, pd.DataFrame) else v) for k, v in kwargs.items()}

            # Informações sobre a função
            logger.info(f"Descrição da função: {func.__doc__}")
            logger.info(f"Nome da função: {func.__name__}")
            logger.info(f"Argumentos da função (sanitizados): {sanitized_args}")
            logger.info(f"Argumentos nomeados da função (sanitizados): {sanitized_kwargs}")

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time
                logger.success(f"Finalizado: {func.__name__} em {elapsed_time:.4f}s")
                return result
            except Exception as e:
                error_message = f"Erro na função {func.__name__}: {str(e)}"
                stack_trace = traceback.format_exc()
                description = func.__doc__ or "Sem descrição disponível."

                logger.error(error_message)
                logger.error(stack_trace)
                logger.error(f"Descrição da função: {description}")
                raise e  # Relevanta o erro para que o programa não continue silenciosamente

        return wrapper
    return decorator
