# from flext-oracle-wms/docs/troubleshooting.md:283
from __future__ import annotations
import logging

from flext_core import u

logging.basicConfig(level=logging.DEBUG)

logger = u.fetch_logger(__name__)
logger.debug("Debug message")
