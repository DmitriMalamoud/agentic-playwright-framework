import logging
import sys

class Logger:
    @staticmethod
    def get_logger(name="PlaywrightFramework"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create handler that outputs to stdout
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            
            # Add handler to logger
            logger.addHandler(handler)
        
        return logger

# Create a singleton instance for ease of use
logger = Logger.get_logger()
