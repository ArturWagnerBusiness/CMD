import keyboard
from msvcrt import getch
from key_definition import key_definition, key_definition_special


class KeyCollector:
    def __init__(self):
        self.combos = []
        self.read_permission = True

    def get_next_combo(self):
        if len(self.combos) != 0:
            combo = self.combos[0]
            self.combos.pop(0)
            return combo
        return ""

    def clear_combo(self):
        self.combos = []

    def start_recording(self):
        # This is to be run as a separate thread!
        while True:
            if not self.read_permission:
                continue
            key = ord(getch())
            if key == 224 or key == 0:
                key2 = ord(getch())
            else:
                key2 = "X"

            combo = ""

            # Key is special
            if str(key2) != "X":
                combo = key_definition_special[key2]

            # Key is normal
            else:
                combo = key_definition[key]

            # Key is unknown
            if isinstance(combo, list):
                self.combos.append(combo)
                # print("Action> " + combo[0])
            else:
                if combo == "":
                    if str(key2) == "X":
                        pass # print("Unknown action: " + str(key))
                    else:
                        pass # print("Unknown action: " + str(key) + " " + str(key2))

                # Key is known
                else:
                    self.combos.append(combo)
                    # print(combo)
    def toggle_reading(self):
        self.read_permission = not self.read_permission


def main():
    key = KeyCollector()
    key.start_reading()


if __name__ == '__main__':
    main()
