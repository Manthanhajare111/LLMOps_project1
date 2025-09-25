import logging,os
from datetime import datetime

class Customlogger:
    def __init__(self):
        self.logs_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(self.logs_dir, exist_ok=True)

        log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file_path = os.path.join(self.logs_dir, log_filename)

        # Configure logging
        logging.basicConfig(
            filename=log_file_path,
            format='%(asctime)s  %(levelname)s %(name)s (line:%(lineno)d) - %(message)s',
            level=logging.INFO
        )

    def get_logger(self,name=__file__):
        return logging.getLogger(os.path.basename(name))
    
if __name__ == "__main__":
    logger = Customlogger()
    logger=logger.get_logger(__file__)
    logger.info("This is an info message")
    logger.error("This is an error message")