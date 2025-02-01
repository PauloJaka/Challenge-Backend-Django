from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def parse_date(date_str: str) -> datetime:
    try:
        if len(date_str) == 4:  # Apenas ano (YYYY)
            return datetime.strptime(date_str, "%Y")
        elif len(date_str) == 7:  # Ano e mês (YYYY-MM)
            return datetime.strptime(date_str, "%Y-%m")
        elif len(date_str) == 10:  # Data completa (YYYY-MM-DD)
            return datetime.strptime(date_str, "%Y-%m-%d")
        else:
            raise ValueError(
                "Formato de data inválido. Use YYYY, YYYY-MM, ou YYYY-MM-DD"
            )
    except ValueError as e:
        logger.error(f"Erro ao analisar data: {date_str} - {str(e)}")
        raise
