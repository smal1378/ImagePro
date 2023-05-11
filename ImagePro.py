# ImagePro or Image Processor
# by: Esmail Mahjoor - Farahnaz Eslami
# https://t.me/smal1378

from model import Core
from view.main import Application

if __name__ == '__main__':
    core = Core()
    app = Application(core)
    app.exec()

