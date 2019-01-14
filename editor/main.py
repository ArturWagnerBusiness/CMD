import sys
import os
import re
import keyboard
import time
from _thread import start_new_thread
from KeyCollector import KeyCollector
from colorama import init as colorama
colorama()

class Color:
    black = "30"
    red = "31"
    green = "32"
    yellow = "33"
    blue = "34"
    purple = "35"
    cyan = "36"
    white = "37"


themes = {
    "dark_red": {
        "name": "Dark Red",
        "help_line": [Color.black, Color.black, 1],
        "help_text": [Color.black, Color.black, 1],
        "help_title": [Color.red, Color.black, 1],

        "esc": [Color.red, Color.black, 1],
        "toolbar_line": [Color.black, Color.black, 1],
        "toolbar_text": [Color.black, Color.black, 1],
        "toolbar_title": [Color.red, Color.black, 1],

        "editor_line_number": [Color.red, Color.black, 0],
        "editor_line_side": [Color.red, Color.black, 1],
        "editor_text": [Color.black, Color.black, 1],
        "editor_cursor": [Color.red, Color.black, 1],

        "editor_bottom": [Color.red, Color.black, 1],

        "credits": [Color.black, Color.black, 1],

        "debug": [Color.white, Color.black, 0],
    },
    "dark_cyan": {
        "name": "Dark Cyan",
        "help_line": [Color.black, Color.black, 1],
        "help_text": [Color.cyan, Color.black, 0],
        "help_title": [Color.cyan, Color.black, 1],

        "esc": [Color.cyan, Color.black, 1],
        "toolbar_line": [Color.black, Color.black, 1],
        "toolbar_text": [Color.black, Color.black, 1],
        "toolbar_title": [Color.cyan, Color.black, 1],

        "editor_line_number": [Color.cyan, Color.black, 1],
        "editor_line_side": [Color.blue, Color.black, 1],
        "editor_text": [Color.black, Color.black, 1],
        "editor_cursor": [Color.cyan, Color.black, 0],

        "editor_bottom": [Color.blue, Color.black, 1],

        "credits": [Color.black, Color.black, 1],

        "debug": [Color.white, Color.black, 0],
    }
}
themes_list = []
for name, x in themes.items():
    themes_list.append(name)
for x, name in enumerate(themes_list):
    if name == "dark_red":
        current_theme = themes[themes_list[x]]
        current_theme_id = x

cursor_color = "\033[{}m".format(";".join([
    str(current_theme["editor_cursor"][2]),
    current_theme["editor_cursor"][0],
    str(int(current_theme["editor_cursor"][1])+10)
]))
cursor_color_end = "\033[{}m".format(";".join([
    str(current_theme["editor_text"][2]),
    current_theme["editor_text"][0],
    str(int(current_theme["editor_text"][1])+10)
]))


def next_theme():
    global current_theme, current_theme_id, cursor_color, cursor_color_end
    if current_theme_id == len(themes_list)-1:
        current_theme_id = 0
        current_theme = themes[themes_list[0]]
    else:
        current_theme_id += 1
        current_theme = themes[themes_list[current_theme_id]]

    cursor_color = "\033[{}m".format(";".join([
        str(current_theme["editor_cursor"][2]),
        current_theme["editor_cursor"][0],
        str(int(current_theme["editor_cursor"][1]) + 10)
    ]))
    cursor_color_end = "\033[{}m".format(";".join([
        str(current_theme["editor_text"][2]),
        current_theme["editor_text"][0],
        str(int(current_theme["editor_text"][1]) + 10)
    ]))


def color_set(setting):
    if setting == "none":
        print("\033[0m", end="")
    else:
        settings = current_theme[setting]
        settings = str(settings[2]) + ";" + settings[0] + ";" + str(int(settings[1])+10)
        print("\033[{}m".format(settings), end='')


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
        global cursor_pos
        left = self.get_line(cursor_pos[1])[:cursor_pos[0]]
        right = self.get_line(cursor_pos[1])[cursor_pos[0]:]
        self.lines[cursor_pos[1]] = left
        self.lines.insert(cursor_pos[1] + 1, right)
        cursor_pos[1] += 1
        cursor_pos[0] = 0

    def add_character(self, character):
        global cursor_pos
        temp_line = list(self.get_line(cursor_pos[1]))

        temp_line.insert(cursor_pos[0], character)
        self.lines[cursor_pos[1]] = "".join(temp_line)
        cursor_pos[0] += 1

    def remove_line(self):
        global cursor_pos
        if cursor_pos[1] != 0:
            self.lines.pop(cursor_pos[1])
            cursor_pos[1] -= 1
        else:
            self.lines[0] = ""

    def remove_character(self):
        global cursor_pos
        if cursor_pos[0] != 0:
            temp_line = list(self.get_line(cursor_pos[1]))
            temp_line.pop(cursor_pos[0] - 1)
            self.lines[cursor_pos[1]] = "".join(temp_line)
            cursor_pos[0] -= 1
        elif cursor_pos[0] == 0 and cursor_pos[1] != 0:
            temp = self.get_line(cursor_pos[1])
            self.lines.pop(cursor_pos[1])
            cursor_pos[1] -= 1
            cursor_pos[0] = opened_file.line_length(cursor_pos[1])
            self.lines[cursor_pos[1]] += temp

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
        color_set("debug")
        print("Debug mode enabled:")
        print("Fps: {}".format(fps))
        print("Cursor: ({}, {})".format(cursor_pos[0], cursor_pos[1]))
        print("Display: ({}, {})".format(display_pos[0], display_pos[1]))
        print("File name: {}".format(system_data.get_currently_working_file()))
        print("File path: {}".format(system_data.get_currently_working_path()))
        if writing:
            print("writing = True")
        else:
            print("writing = False")
        if options[0]:
            print("options = True")
        else:
            print("options = False")
        print("Theme: {} ({})".format(current_theme["name"], current_theme_id))
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
    global cursor_pos
    if direction == "u" and cursor_pos[1] != 0:
        cursor_pos[1] -= 1
        if cursor_pos[0] >= opened_file.line_length(cursor_pos[1]):
            cursor_pos[0] = opened_file.line_length(cursor_pos[1])
    if direction == "d" and cursor_pos[1] != len(opened_file.get_lines()) - 1:
        cursor_pos[1] += 1
        if cursor_pos[0] >= opened_file.line_length(cursor_pos[1]):
            cursor_pos[0] = opened_file.line_length(cursor_pos[1])
    if direction == "l" and cursor_pos[0] != 0:
        cursor_pos[0] -= 1
    elif direction == "l" and cursor_pos[0] == 0 and cursor_pos[1] != 0:
        cursor_pos[1] -= 1
        cursor_pos[0] = opened_file.line_length(cursor_pos[1])
    if direction == "r" and cursor_pos[0] != opened_file.line_length(cursor_pos[1]):
        cursor_pos[0] += 1
    elif direction == "r" and cursor_pos[0] == opened_file.line_length(cursor_pos[1]) and cursor_pos[1] < len(opened_file.get_lines()) - 1:
        cursor_pos[1] += 1
        cursor_pos[0] = 0


def toggle_help():
    global is_toggle_help
    is_toggle_help = not is_toggle_help


def save_document():
    write_file_here(system_data.working_file, opened_file.get_lines())
    debug.add_feedback("File was save successful!")


def editor():
    global cursor_visible, opened_file, cursor_pos, is_toggle_help, writing, options
    global display_height, display_width, display_pos, fps
    fps = 10  # FPS
    is_toggle_help = False

    display_height = 50
    display_width = 190
    display_pos = [0, 0]

    time_stamps = {
        "print_time": 0,
    }
    key_collector = KeyCollector()
    start_new_thread(key_collector.start_recording, ())

    cursor_pos = [0, 0]
    cursor_visible = True
    writing = True
    options = [False, "0"]

    while True:
        combo = key_collector.get_next_combo()
        if options[0]:
            if not isinstance(combo, list):
                if combo in list("1234567"):
                    options[1] = combo
            else:
                action = combo[0]
                if action == "ESC":
                    writing = True
                    options = [False, "0"]
                if action == "DOWN_ARROW" and int(options[1]) < 7:
                    options[1] = str(int(options[1]) + 1)
                if action == "UP_ARROW" and int(options[1]) > 1:
                    options[1] = str(int(options[1]) - 1)
                if action == "ENTER":
                    if options[1] == "1":
                        color_set("none")
                        os.system("mode con: cols=81 lines=81")
                        exit()
                    if options[1] == "2":
                        save_document()
                    if options[1] == "3":
                        toggle_help()
                    if options[1] == "4":
                        debug.toggle()
                    if options[1] == "5":
                        if fps < 60:
                            fps += 1
                    if options[1] == "6":
                        if fps > 1:
                            fps -= 1
                    if options[1] == "7":
                        next_theme()

        elif writing:
            # If key stroke
            if not isinstance(combo, list):
                if combo != "":
                    opened_file.add_character(combo)
            # If action request
            else:
                action = combo[0]
                if action == "F1":
                    debug.toggle()
                if action == "ENTER":
                    opened_file.new_line_after()

                # "ctrl+backspace" should do opened_file.remove_line() <-- Add it later
                if action == "BACKSPACE":
                    opened_file.remove_character()

                if action == "ESC":
                    writing = False
                    options = [True, 0]

                for arrow_key in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    if action == "{}_ARROW".format(arrow_key):
                        cursor_move(arrow_key[:1].lower())

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
        color_set("help_line")
        print("-"*96, end="")
        color_set("help_title")
        print("[ HELP ]", end="")
        color_set("help_line")
        print("-"*96, end="")

        help_pop_up = [
            "Opened a help section!"
        ]
        color_set("help_text")
        for line in help_pop_up:
            print("  " + line + " "*(76-len(line)) + " ")
        print()
    color_set("esc")
    print("[ESC]", end="")
    color_set("toolbar_line")
    print("="*90, end="")
    color_set("toolbar_title")
    print("[ Editor ]", end="")
    color_set("toolbar_line")
    print("="*95)
    top_menu = [
        "1) EXIT (no save)   4) Toggle Debug   7) Next Theme",
        "2) Save             5) Increase fps",
        "3) Toggle Help      6) Decrease fps"

    ]
    color_set("toolbar_text")
    if options[0]:
        print()
        selected_top_menu = []
        for line in top_menu:
            selected_top_menu.append(line.replace(str(options[1])+")", "->"))
        for line in selected_top_menu:
            print("  " + line + " "*(76-len(line)) + " ")
        print("_"*200)
    print()

    # Display adjustment
    # <- width check ->
    if display_pos[0] == 0 and cursor_pos[0] == 0:
        pass
    elif cursor_pos[0] >= display_pos[0] + display_width:
        display_pos[0] = cursor_pos[0] - display_width
    elif cursor_pos[0] <= display_pos[0]:
        display_pos[0] = cursor_pos[0]
    # /\ height check \/
    if display_pos[1] == 0 and cursor_pos[1] == 0:
        pass
    elif cursor_pos[1] >= display_pos[1] + display_height:
        display_pos[1] = cursor_pos[1] - display_height
    elif cursor_pos[1] <= display_pos[1]:
        display_pos[1] = cursor_pos[1]

    for i, line in enumerate(opened_file.get_lines()):
        if i < display_pos[1]:
            continue
        if i > display_pos[1] + display_height:
            continue
        line = line[display_pos[0]:]
        if display_width < len(line):
            line = line[:display_width]

        number_index_width = 5
        number_index = str(i) + " " * (number_index_width - len(str(i)))
        if cursor_pos[1] == i and cursor_visible:
            temp = list(line)
            if writing:
                while True:
                    try:
                        temp[cursor_pos[0]-display_pos[0]] = cursor_color + "<" + cursor_color_end
                        break
                    except IndexError:
                        temp.append(" ")
            color_set("editor_line_number")
            print(number_index, end="")
            color_set("editor_line_side")
            print("> ", end="")
            color_set("editor_text")
            print("".join(temp))
        else:
            color_set("editor_line_number")
            print(number_index, end="")
            color_set("editor_line_side")
            print("> ", end="")
            color_set("editor_text")
            print(line)
    fill_lines = (display_height-len(opened_file.get_lines()))
    if fill_lines > 0:
        print("\n" * fill_lines)
    color_set("editor_bottom")
    print("\n" + "#"*200)

    bottom_credits = [
        "CMD text editor developed by Artur Wagner",
        "Jan 2019"
    ]
    color_set("credits")
    print()
    for line in bottom_credits:
        space_right = (201 - len(line))/2
        space_left = space_right - 1
        if isinstance(len(line)/2, float):
            print(round(space_left) * " " + line + " " * round(space_right))
        else:
            print(int(space_left) * " " + line + "" * int(space_right))
    color_set("debug")
    print()
    if debug.is_enabled():
        debug.display()
    color_set("none")

def main():
    global system_data, debug
    os.system("mode con: cols=201 lines=81")
    system_data = SystemData(sys.argv)
    debug = Debug()
    order = system_data.get_order()
    if order == "new":
        system_data.change_currently_working_file(
            create_new_file_here(system_data.get_currently_working_file())
        )
    open_editor()


main()
