import sys
import os
import re
import keyboard
import time

description = {
    "help": "\nUsage:\n\n> editor file_name [new/open] [file path]\n" + " " * 30 + " ^ W.I.P ^ "
}


try:
    if sys.argv[1] in ["-help", "-h"]:
        print(description["help"])
        exit()
except IndexError:
    print(description["help"])
    exit()


print("Please wait while we set things up for you!")
print("Loading...")


def file_exists(path, file_name):
    return os.path.exists(path + "\\" + file_name)


def get_file_name(file_name):
    return re.compile(r"([a-zA-Z0-9\. \(\)]*)\..*$").search(file_name).group(1)


def get_file_extension(file_name):
    return "." + re.compile(r"\.([a-zA-Z0-9]*)$").search(file_name).group(1)


def insert_to_filename(file_name, insert):
    return get_file_name(file_name) + insert + get_file_extension(file_name)


def get_free_file_number(file_name, path=os.getcwd()):
    if not file_exists(path, file_name):
        available_name = file_name
    else:
        available_name = None
    i = 1
    while available_name is None:
        test_name = insert_to_filename(file_name, " (" + str(i) +")")
        if not file_exists(path, test_name):
            available_name = test_name
        i += 1
    return available_name


def create_new_file_here(file_name):
    file_name = get_free_file_number(file_name)
    with open(file_name, "w") as f:
        f.write("")
    return file_name


def read_file_here(file_name):
    file_content = []
    x = 0
    with open(file_name, "r") as f:
        for line in f:
            x += 1
            file_content.append(line.rstrip())
    if x == 0:
        file_content.append("")
    return file_content


def write_file_here(filename, lines):
    with open(filename, "w") as f:
        f.close()
    with open(filename, "a") as f:
        for line in lines:
            f.write(line + "\n")


class SystemData:
    def __init__(self, argv):
        try:
            self.working_file = argv[1].lower()
        except IndexError:
            self.working_file = "New Text Document.txt"
        try:
            self.working_path = argv[3].lower()
        except IndexError:
            self.working_path = os.getcwd()
        try:
            if not argv[2].lower() in ["new", "open"]:
                print("You must mention what to do with the file\neditor {new/open}{file name} {file path}")
                exit()
            self.order = argv[2].lower()
        except IndexError:
            if file_exists(self.working_path, self.working_file):
                self.order = "open"
            else:
                self.order = "new"

    def get_currently_working_file(self):
        return self.working_file

    def change_currently_working_file(self, new_file):
        self.working_file = new_file

    def get_order(self):
        return self.order

    def get_currently_working_path(self):
        return self.working_path


class File:
    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.lines = read_file_here(self.file)

    def get_line(self, line):
        return self.lines[line]

    def get_lines(self):
        return self.lines

    def new_line_after(self):
        global cursor_place
        left = self.get_line(cursor_place[1])[:cursor_place[0]]
        right = self.get_line(cursor_place[1])[cursor_place[0]:]
        self.lines[cursor_place[1]] = left
        self.lines.insert(cursor_place[1] + 1, right)
        cursor_place[1] += 1
        cursor_place[0] = 0

    def add_character(self, character):
        global cursor_place
        temp_line = list(self.get_line(cursor_place[1]))

        temp_line.insert(cursor_place[0], character)
        self.lines[cursor_place[1]] = "".join(temp_line)
        cursor_place[0] += 1

    def remove_line(self):
        global cursor_place
        if cursor_place[1] != 0:
            self.lines.pop(cursor_place[1])
            cursor_place[1] -= 1
        else:
            self.lines[0] = ""

    def remove_character(self):
        global cursor_place
        if cursor_place[0] != 0:
            temp_line = list(self.get_line(cursor_place[1]))
            temp_line.pop(cursor_place[0]-1)
            self.lines[cursor_place[1]] = "".join(temp_line)
            cursor_place[0] -= 1
        elif cursor_place[0] == 0 and cursor_place[1] != 0:
            temp = self.get_line(cursor_place[1])
            self.lines.pop(cursor_place[1])
            cursor_place[1] -= 1
            cursor_place[0] = opened_file.line_length(cursor_place[1])
            self.lines[cursor_place[1]] += temp

    def line_length(self, line):
        return len(self.lines[line])

class Debug:
    def __init__(self):
        self.enabled = False
        self.feedback = []
    def is_enabled(self):
        return self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled

    def display(self):
        print("Cursor: ({}, {})".format(cursor_place[0], cursor_place[1]))
        print("File name: {}".format(system_data.get_currently_working_file()))
        print("File path: {}".format(system_data.get_currently_working_path()))
        print("\nFeed:")
        for feed in self.feedback:
            print(feed)

    def add_feedback(self, feed):
        self.feedback.append(feed)


def open_editor():
    global opened_file
    opened_file = File(system_data.get_currently_working_file(), system_data.get_currently_working_path())
    editor()


def cursor_move(direction):
    global cursor_place
    if direction == "u" and cursor_place[1] != 0:
        cursor_place[1] -= 1
        if cursor_place[0] >= opened_file.line_length(cursor_place[1]):
            cursor_place[0] = opened_file.line_length(cursor_place[1])
    if direction == "d" and cursor_place[1] != len(opened_file.get_lines()) - 1:
        cursor_place[1] += 1
        if cursor_place[0] >= opened_file.line_length(cursor_place[1]):
            cursor_place[0] = opened_file.line_length(cursor_place[1])
    if direction == "l" and cursor_place[0] != 0:
        cursor_place[0] -= 1
    if direction == "r" and cursor_place[0] != opened_file.line_length(cursor_place[1]):
        cursor_place[0] += 1


def add_keyboard_key(combo, key):
    keyboard.add_hotkey(combo, opened_file.add_character, args=key)


def toggle_help():
    global is_toggle_help
    is_toggle_help = not is_toggle_help


def save_document():
    write_file_here(system_data.working_file, opened_file.get_lines())
    debug.add_feedback("File was save successful!")


def setup_editor_controls():
    abc = "abcdefghijklmnopqrstuvwxyz"
    for key in list("1234567890" + abc):
        add_keyboard_key(key, key)

    for key in list(",./`-=[];# "):
        add_keyboard_key(key, key)

    for key in list(abc):
        add_keyboard_key("shift+" + key, key.upper())

    add_keyboard_key("shift+1", "!")
    add_keyboard_key("shift+2", "\"")
    add_keyboard_key("shift+3", "£")
    add_keyboard_key("shift+4", "$")
    add_keyboard_key("shift+5", "%")
    add_keyboard_key("shift+6", "^")
    add_keyboard_key("shift+7", "&")
    add_keyboard_key("shift+8", "*")
    add_keyboard_key("shift+9", "(")
    add_keyboard_key("shift+0", ")")
    add_keyboard_key("shift+;", ":")
    add_keyboard_key("shift+-", "_")
    add_keyboard_key("shift+/", "?")

    keyboard.add_hotkey("enter", opened_file.new_line_after)
    keyboard.add_hotkey("backspace", opened_file.remove_character)
    keyboard.add_hotkey("ctrl+backspace", opened_file.remove_line)
    keyboard.add_hotkey("ctrl+left", cursor_move, args="l")
    keyboard.add_hotkey("ctrl+up", cursor_move, args="u")
    keyboard.add_hotkey("ctrl+down", cursor_move, args="d")
    keyboard.add_hotkey("ctrl+right", cursor_move, args="r")
    keyboard.add_hotkey("esc+2", toggle_help)
    keyboard.add_hotkey("esc+3", save_document)
    keyboard.add_hotkey("esc+4", debug.toggle)


def editor():
    global cursor_visible, opened_file, cursor_place, is_toggle_help
    fps = 30  # FPS
    is_toggle_help = True

    time_stamps = {
        "print_time": 0,
    }

    setup_editor_controls()

    cursor_place = [0, 0]
    cursor_visible = True

    while True:
        if keyboard.is_pressed("esc") and keyboard.is_pressed("1"):
            while True:
                input("Do CTRL+C to close the program! Garbage -[")

        if current_time() - time_stamps["print_time"] > round(1 / fps * 1000):
            time_stamps["print_time"] = current_time()
            display_tick()
            cursor_visible = not cursor_visible


def current_time():
    return int(round(time.time() * 1000))


def display_tick():
    global opened_file, is_toggle_help
    os.system("cls")
    if is_toggle_help:
        print("-"*35 + "[ HELP ]" + "-"*36)

        help = [
            "This is an experimental version 1",
            "You can move with CTRL+ARROW_KEY",
            "You can use ESC as a root with a number to select other options.",
            "For example 2 (ESC+2) to hide this menu. You can pop it up any time you want!"
        ]
        for line in help:
            print("  " + line + " "*(76-len(line)) + " ")
    print("="*34 + "[ Editor ]" + "="*35)
    top_menu = [
        "Root: [ESC] ",
        "1) EXIT (no save) 3) Save",
        "2) Toggle Help    4) Toggle Debug",
    ]
    for line in top_menu:
        print("  " + line + " "*(76-len(line)) + " ")
    print()
    print("#"*79 + "\n")
    for i, line in enumerate(opened_file.get_lines()):
        if cursor_place[1] == i and cursor_visible:
            temp = list(line)
            while True:
                try:
                    temp[cursor_place[0]] = "<"
                    break
                except IndexError:
                    temp.append(" ")
            print("> " + "".join(temp))
        else:
            print("> " + line)
    print("\n" + "#"*79)
    bottom_credits = [
        "CMD text editor developed by Artur Wagner",
        "Jan 2019"
    ]
    print()
    for line in bottom_credits:
        space_right = (79 - len(line))/2
        space_left = space_right - 1
        if isinstance(len(line)/2, float):
            print(round(space_left) * " " + line + " " * round(space_right))
        else:
            print(int(space_left) * " " + line + "" * int(space_right))
    print()
    if debug.is_enabled():
        debug.display()


def main():
    global system_data, debug
    system_data = SystemData(sys.argv)
    debug = Debug()
    order = system_data.get_order()
    if order == "new":
        system_data.change_currently_working_file(
            create_new_file_here(system_data.get_currently_working_file())
        )
    open_editor()


main()
