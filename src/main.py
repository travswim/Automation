from file_cleanup import file_cleanup
import json


def main():
    with open("directories.json", "r") as config_file:
        dirs = json.load(config_file)
    dirs = dirs["directories"]
    for directory in dirs:
        file_cleanup(directory)


if __name__ == "__main__":
    main()
