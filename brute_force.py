#!/usr/bin/env python3

import os
import sys
import time

import py3270
import tqdm
from lumberjack.lumberjack import Lumberjack


class WrappedEmulator(py3270.Emulator):
    py3270.X3270App.executable = "./bin/x3270"
    py3270.S3270App.executable = "./bin/s3270"


class B_FRAME():
    def __init__(self, ip, port, username, password, debug=True):
        self.debug = debug
        self.log = Lumberjack("brute.log", self.debug)

        # True - x3270; False - s3270
        self.emulator = WrappedEmulator(True)

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        time.sleep(2)

        self.connect()

        self.login()

        if self.debug:
            self.print_screen()


    def connect(self):
        self.log.info("Connecting to {}:{}".format(self.ip, self.port))

        self.emulator.connect("{}:{}".format(self.ip, self.port))
        self.emulator.send_enter()

        if not self.emulator.is_connected():
            self.log.error("Failed to connect")
            sys.exit(1)

        self.log.info("Connected successfully")


    def login(self):
        self.log.info("Loggin as " + self.username)

        self.emulator.move_to(0, 0)
        self.emulator.send_string(self.username)
        self.emulator.move_to(1, 1)
        self.emulator.send_string(self.password)

        self.emulator.send_enter()

        time.sleep(2)


    def get_screen_data(self):
        return self.emulator.exec_command(b'ASCII').data


    def print_screen(self):
        screen_data = self.get_screen_data()

        for line in screen_data:
            self.log.debug(line.decode())


    def disconnect(self):
        self.log.info("Disconnecting...")

        self.emulator.exec_command(b'DISCONNECT')


    def create_html(self, filename):
        self.log.debug("Creating HTML file")

        full_filename = "./html/{}/{}.html".format(self.username, filename)

        if os.path.isfile(full_filename):
            os.remove(full_filename)

        self.emulator.exec_command("PRINTTEXT(HTML, file, {})".format(full_filename).encode())


    def test_command(self, command):
        if self.debug:
            self.log.debug("Testing command: " + command)

        self.emulator.move_to(10, 10)
        self.emulator.send_string(command)

        if self.debug:
            self.print_screen()

        self.emulator.send_enter()

        if self.debug:
            self.print_screen()


    def go_home(self):
        self.emulator.send_pf3()

        screen_data = self.get_screen_data()

        if b'SOME TEXT' not in screen_data[0]:
            self.log.warning("Filed to exit menu")

            self.disconnect()

            time.sleep(2)

            self.connect()
            time.sleep(2)

            self.login()


def main():
    with open(sys.argv[1], "r") as command_file:
        command_list = command_file.readlines()

    b_frame = B_FRAME(
        "127.0.0.1",
        "9999",
        "USER",
        "PASS",
        False
    )

    BLACK_LIST = [
    ]

    START_FROM = ""
    START_FLAG = False

    if not START_FROM:
        START_FLAG = True

    for command in tqdm.tqdm(command_list):
        if not START_FLAG:
            if command.strip() == START_FROM:
                START_FLAG = True
                continue

        else:
            if command.strip() in BLACK_LIST:
                continue

            b_frame.test_command(command.strip())
            time.sleep(1)
            b_frame.create_html(command.strip())
            b_frame.go_home()

    b_frame.disconnect()


if __name__ == "__main__":
    main()
