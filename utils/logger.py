import logging
import sys
import os

class Logger:
    @staticmethod
    def get_logger(name="PlaywrightFramework"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # Create handler that outputs to file
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(os.path.join(log_dir, "test.log"), mode='w')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger

# Create a singleton instance for ease of use
logger = Logger.get_logger()
