import logging

logging.basicConfig(
    format="%(levelname)s: %(name)s: %(message)s",
    level=logging.DEBUG,
    force=True
)

def get_logger(name: str = None):
    return logging.getLogger(name or __name__)
