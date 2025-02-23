import logging

log_file = "app.log"

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)  # You can set the logging level for this handler

logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)

logger.info("Logging setup completed successfully")
