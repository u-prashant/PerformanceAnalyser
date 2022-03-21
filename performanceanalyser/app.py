from config import Config
from constants import File
from gui import GUI


if __name__ == '__main__':
    config = Config(File.CONFIG_PICKLE_FILE)
    GUI(config)
