import logging
import os
from app import CommandLine
from app.host import Host

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    try:
        args = CommandLine.parse_arguments()
        # Create an instance of Host with parsed arguments
        instance = Host(args)

        # Ensure output folder exists
        os.makedirs(args.output_folder, exist_ok=True)

        # Run the main function with the parsed arguments
        instance.run()
    except ValueError as e:
        logging.error("Error: %s", e)


if __name__ == '__main__':
    main()
