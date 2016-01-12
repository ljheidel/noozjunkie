import collector_config
import logging
import sys
import os

from .stats import Stats
stats = Stats()

log = logging.getLogger(__name__)
log.setLevel(collector_config.LOGLEVEL)
ch = logging.StreamHandler()
ch.setLevel(collector_config.CONSOLELOG_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

if collector_config.LOGFILE:
    fh = logging.FileHandler(collector_config.LOGFILE)
    fh.setLevel(collector_config.LOGFILE_LEVEL)
    fh.setFormatter(formatter)
    log.addHandler(fh)

log.addHandler(ch)


from .restcall import RestCall
try:
    rest = RestCall()
except Exception as e:
    log.critical("ABEND.  Cannot continue.  Shutting down.")
    sys.exit(1)

from .feedmgr import FeedMgr
from .collector import Collector
from .articlemgr import ArticleMgr
