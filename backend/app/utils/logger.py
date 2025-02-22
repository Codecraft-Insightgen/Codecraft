import logging

# Define log file path relative to this file or your project root
log_file = "app.log"

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)  # You can set the logging level for this handler

# Add the file handler to the root logger
logging.getLogger().addHandler(file_handler)

# Optionally, you can also add a stream handler for logging output to the console
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.INFO)
# logging.getLogger().addHandler(stream_handler)

logger = logging.getLogger(__name__)

# Example log message
logger.info("Logging setup completed successfully")
