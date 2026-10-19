from datetime import datetime
import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"playwright_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
#create log file
logger = logging.getLogger("playwright")
logger.setLevel(logging.DEBUG)
logger.propagate = False

#
if not logger.handlers:
    formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    #2 sections :--> print logs in console / file
    # Console
    cons_hand = logging.StreamHandler()
    cons_hand.setLevel(logging.DEBUG)
    cons_hand.setFormatter(formatter)

    #file

    fh = logging.FileHandler(LOG_FILE,encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(cons_hand)
    logger.addHandler(fh)
logger.info("Login initilize")
logger.info("Log file : %s",LOG_FILE)