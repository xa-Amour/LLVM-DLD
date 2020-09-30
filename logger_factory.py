import logging.handlers

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    level=logging.DEBUG)
fmt = logging.Formatter(
    "%(asctime)s %(pathname)s %(filename)s %(funcName)s %(lineno)s \
    %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
rht = logging.handlers.TimedRotatingFileHandler('DLD.log')
rht.setFormatter(fmt)
logger.addHandler(rht)
