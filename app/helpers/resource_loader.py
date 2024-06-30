import os
import logging

# Initialize the logger for this module
logger = logging.getLogger(__name__)


class ResourceLoader:
    @staticmethod
    def load_resource_file_by_key(key):
        return ResourceLoader.load_resource_file(os.getenv(key))

    @staticmethod
    def load_resource_file(filename):
        file_path = os.path.join(filename)
        try:
            with open(file_path, 'r', encoding='UTF-8') as file:
                content = file.read()
                logger.info("Successfully loaded resource file: %s", filename)
                return content
        except FileNotFoundError:
            logger.error("Resource file not found: %s", filename)
            return None
        except Exception as e:
            logger.exception(
                "Failed to load resource file %s: %s", filename, e)
            return None
