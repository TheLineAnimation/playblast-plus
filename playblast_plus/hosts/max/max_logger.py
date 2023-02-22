from ...lib import logger

class MaxLogger(logger.Logger):
    
    LOGGER_NAME = "MaxLogger"
    FORMAT_DEFAULT = "[%(levelname)s][%(name)s] %(message)s"
    PROPAGATE_DEFAULT = False

if __name__ == "__main__":
    MaxLogger.set_propagate(MaxLogger.PROPAGATE_DEFAULT)
    MaxLogger.debug("debug message")
    MaxLogger.info("info message")
    MaxLogger.warning("warning message")
    MaxLogger.error("error message")
