from ...lib import logger

class MayaLogger(logger.Logger):
    """_summary_

    Args:
        logger (_type_): _description_
    """
    
    LOGGER_NAME = "MayaLogger"
    FORMAT_DEFAULT = "[%(name)s][%(levelname)s] %(message)s"
    PROPAGATE_DEFAULT = False

if __name__ == "__main__":
    MayaLogger.set_propagate(MayaLogger.PROPAGATE_DEFAULT)
    MayaLogger.debug("debug message")
    MayaLogger.info("info message")
    MayaLogger.warning("warning message")
    MayaLogger.error("error message")
