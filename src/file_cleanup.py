import os
from datetime import datetime
import logging


class FileCleanup:

    def __init__(self):
        today = datetime.today()
        logging.basicConfig(
                filename=f"file_cleanup-{today.strftime('%Y-%m-%d')}.log",
                level=logging.INFO, format="%(asctime)s %(message)s"
            )

    @staticmethod
    def file_cleanup(directory: str):
        """
        Remove files in a directory that are older than 30 days
        """

        today = datetime.today()

        dir_path = os.path.expanduser(directory)
        try:
            files = os.listdir(dir_path)
            logging.info(f"CLEANING: {dir_path.upper()}")
        except FileNotFoundError as err:
            logging.error(err)
            return

        for file in files:
            full_file_path = os.path.join(dir_path, file)
            # Check if it's a file
            if not os.path.isfile(full_file_path):
                continue

            # get the creation time of the file
            creation_time = os.path.getctime(full_file_path)
            formatted_creation_time = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")

            # get the time difference between the creation time and today
            time_difference = today - datetime.fromtimestamp(creation_time)

            # if the file is older than 30 days, delete it
            if time_difference.days > 30:
                try:
                    os.remove(full_file_path)
                    logging.info("{:<20} | {}".format(f"DELETED: {file}", formatted_creation_time + " > 30 days old"))
                except PermissionError as err:
                    logging.error(err)
            else:
                remaining_days = 30 - time_difference.days
                logging.info("{:<20} | {}".format(f"NOT DELETED {file}:", f"will be deleted in {remaining_days} days"))
