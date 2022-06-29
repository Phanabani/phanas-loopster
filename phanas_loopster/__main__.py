import logging
import sys

from phanas_loopster import main

logger = logging.getLogger("phanas_loopster")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
)
logger.addHandler(handler)

main()
