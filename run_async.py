import asyncio
import logging
import os

from app import CommandLine
from app.host import Host

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main_async():
    try:
        args = CommandLine.parse_arguments()
        # Create an instance of Host with parsed arguments
        instance = Host(args)

        # Ensure output folder exists
        os.makedirs(args.output_folder, exist_ok=True)

        # Run the async main function with the parsed arguments
        await instance.run_async()
    except ValueError as e:
        logging.error("Error: %s", e)

if __name__ == '__main__':
    asyncio.run(main_async())
