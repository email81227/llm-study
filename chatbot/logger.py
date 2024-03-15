
import logging
import os
from datetime import datetime

# Define log directory relative to the script location
log_directory = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs"
)

os.makedirs(log_directory, exist_ok=True)

# Set the log file name with the current timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_filename = f"log_{current_time}.log"
log_filepath = os.path.join(log_directory, log_filename)

# Configure the global logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()
    ]
)

# Define the global logger
logger = logging.getLogger(__name__)
