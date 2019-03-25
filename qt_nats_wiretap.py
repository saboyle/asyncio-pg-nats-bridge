#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import asyncio

from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication, QPlainTextEdit)
from PyQt5.QtCore import QDateTime
from quamash import QEventLoop
from nats.aio.client import Client as NATS


class QtWiretap(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        self.txt = QPlainTextEdit()
        self.txt.setReadOnly(True)
        self.txt.setStyleSheet("background-color: #003366; color: #CCFFCC")
        # self.txt.setStyleSheet("background-color: #BE2625; color: #CCFFCC")

        grid.addWidget(self.txt)

        self.move(300, 150)
        self.setWindowTitle(f"Qt Nats Wiretap - {sys.argv[3]}")
        self.show()

    def insertText(self, new_text):
        self.txt.insertPlainText(f'{QDateTime.currentDateTime().toString()} {new_text} \n')
        self.txt.moveCursor(1)


def wire_tap(msg):
    ex.insertText(msg.data.decode())


def main(loop, subject):
    nc = NATS()
    yield from nc.connect(f"{sys.argv[1]}:{sys.argv[2]}", loop=loop)

    async def mh_s1(msg):
        await wire_tap(msg)

    yield from nc.subscribe(subject, cb=wire_tap)


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: python nats_scrolling_plaintext_edit.py [host] [port] [queue]")
    else:
        app = QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        loop.run_until_complete(main(loop, subject=sys.argv[3]))

        ex = QtWiretap()
        loop.run_forever()
