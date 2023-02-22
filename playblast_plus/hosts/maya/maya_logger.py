from ...lib import logger

class MayaLogger(logger.Logger):
    
    LOGGER_NAME = "MayaLogger"
    FORMAT_DEFAULT = "[%(levelname)s][%(name)s] %(message)s"
    PROPAGATE_DEFAULT = False

if __name__ == "__main__":
    MayaLogger.set_propagate(MayaLogger.PROPAGATE_DEFAULT)
    MayaLogger.debug("debug message")
    MayaLogger.info("info message")
    MayaLogger.warning("warning message")
    MayaLogger.error("error message")
