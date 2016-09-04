__all__ = ['JIMS_1058_URL', 'DATA_DIRS', 'VERSION', 'RAW', 'SCRUB', 'ALL_MODES']

JIMS_1058_URL = 'http://www.jims.hctx.net/jimshome/jimsreports/jims1058.txt'
VERSION = '0.2'
RAW = 'raw'
SCRUB = 'scrub'
ALL_MODES = [RAW, SCRUB]
DATA_DIRS = {RAW: 'raw-data', SCRUB: 'data'}
