#!/usr/bin/python
import json
import curses
import os

AVALIBLE_LANGUAGES_FILE_PATH = os.path.expanduser("~/.config/LCH_languages.json")
LANGUAGES_FILE_PATH = os.path.expanduser("~/.config/hypr/config_files/languages.lua")
UP = [curses.KEY_UP, ord("k")]
DOWN = [curses.KEY_DOWN, ord("j")]
EXIT = [ord("q"), 27]
ENTER = [curses.KEY_ENTER, 10, 13, ord(" ")]

CHECKBOX_ENABLED = "[*] "
CHECKBOX_DISABLED = "[ ] "


def help():
    pass


with open(AVALIBLE_LANGUAGES_FILE_PATH) as file:
    AVALIBLE_LANGUAGES = json.load(file)


def check_files_correction(file_path: str):
    if file_path == AVALIBLE_LANGUAGES_FILE_PATH:
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                exit(f"File: <{file_path}> is not a valid json file")
            else:
                if type(data) is not list:
                    exit(f"File <{file_path}> is not correct, please check")
    elif file_path == LANGUAGES_FILE_PATH:
        with open(file_path, "r") as file:
            content = file.read()
        if (
            content.strip().startswith("return")
            and content.strip().removeprefix("return").strip().startswith('"')
            and content.strip().removeprefix("return").strip().endswith('"')
        ):
            pass
        else:
            exit(f"File <{file_path}> is not correct, please check")


if os.path.exists(LANGUAGES_FILE_PATH):
    check_files_correction(LANGUAGES_FILE_PATH)
else:
    exit(help())
if os.path.exists(AVALIBLE_LANGUAGES_FILE_PATH):
    check_files_correction(AVALIBLE_LANGUAGES_FILE_PATH)
else:
    with open(AVALIBLE_LANGUAGES_FILE_PATH, "w") as file:
        file.write('["en"]')
        exit(
            f"File <{AVALIBLE_LANGUAGES_FILE_PATH}> was created, add needed languages in it"
        )


def parse_languages_lua() -> list:
    check_files_correction(LANGUAGES_FILE_PATH)
    with open(LANGUAGES_FILE_PATH, "r") as file:
        content = (
            file.read()
            .strip()
            .removeprefix("return")
            .strip()
            .removeprefix('"')
            .removesuffix('"')
            .strip()
        )
    content_list = content.split(",")
    output = []
    for record in content_list:
        output.append(record.strip())
    return output


def change_state(language, languages):
    if language in languages:
        languages[language] = not languages[language]


def update_lua_config(LANGUAGES_FILE_PATH, languages):
    activate = []
    for lang in languages:
        if languages[lang]:
            activate.append(lang)
    text = (
        'return "'
        + str(activate).replace("[", "").replace("]", "").replace("'", "")
        + '"'
    )
    with open(LANGUAGES_FILE_PATH, "w") as file:
        file.write(text)


def get_languages():
    languages = {}
    for lang in AVALIBLE_LANGUAGES:
        if lang in parse_languages_lua():
            languages[lang] = True
        else:
            languages[lang] = False
    return languages


def main(stdscr):
    curses.curs_set(0)
    active_selection = 0
    while True:
        stdscr.clear()
        languages = get_languages()
        to_print = {}
        for lang in languages:
            if languages[lang]:
                to_print[lang] = CHECKBOX_ENABLED + lang
            else:
                to_print[lang] = CHECKBOX_DISABLED + lang

        _, max_x = stdscr.getmaxyx()
        y = 0
        x = round(max_x / 2) - 3
        lang_list = {}
        for index, lang in enumerate(to_print):
            text = to_print[lang]
            lang_list[index] = lang
            if index == active_selection:
                stdscr.addstr(y, x, text, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, text)
            y += 1
        stdscr.refresh()
        key = stdscr.getch()
        if key in DOWN:
            if active_selection < len(languages) - 1:
                active_selection += 1
            else:
                active_selection = 0
        if key in UP:
            if active_selection > 0:
                active_selection -= 1
            else:
                active_selection = len(languages) - 1
        if key in EXIT:
            exit(0)
        if key in ENTER:
            change_state(lang_list[active_selection], languages)
            update_lua_config(LANGUAGES_FILE_PATH, languages)


curses.wrapper(main)
