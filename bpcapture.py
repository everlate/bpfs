#!/usr/bin/python3

import pyperclip
import zlib
import base64
import json
import os
import binascii
from argparse import ArgumentParser
import pathlib

KEY_INDEX = "index"
KEY_LABEL = "label"
KEY_BOOK = "blueprint_book"
KEY_BLUEPRINTS = "blueprints"
BP_TYPES = {
    "blueprint_book",
    "blueprint",
    "deconstruction_planner",
    "upgrade_planner"
}


class BpCaptureException(Exception):
    pass


def get_type(root_dict) -> str:
    for entry in root_dict:
        if entry in BP_TYPES:
            return entry
    raise BpCaptureException("Invalid blueprint type")


def is_top_level(root_dict) -> bool:
    return KEY_INDEX not in root_dict


def try_delete_dir(bp_path):
    for json_file in pathlib.Path(bp_path).glob('**/*.json'):
        os.remove(str(json_file))
    for dir_path, _, _ in os.walk(bp_path, topdown=False):
        os.rmdir(dir_path)


def make_clean_bp_path(root_dict, root_path: str) -> str:
    bp_type = get_type(root_dict)
    bp_path = os.path.join(root_path, root_dict[bp_type].get(KEY_LABEL, "blueprint"))
    bp_extension = "" if bp_type == KEY_BOOK else ".json"
    if not is_top_level(root_dict) and os.path.exists(bp_path + bp_extension):
        bp_path += ".{}".format(root_dict[KEY_INDEX])
    bp_path += bp_extension
    if is_top_level(root_dict) and os.path.exists(bp_path):
        try:
            if os.path.isdir(bp_path):
                try_delete_dir(bp_path)
            else:
                os.remove(bp_path)
        except OSError:
            raise BpCaptureException("Failed to delete the existing path: {}".format(bp_path))
    return bp_path


def save_to_fs(root_dict, root_path: str) -> None:
    bp_path = make_clean_bp_path(root_dict, root_path)
    if KEY_BOOK in root_dict:
        try:
            os.mkdir(bp_path)
        except IOError:
            raise BpCaptureException("Failed to create directory: {}".format(bp_path))
        for bp in root_dict[KEY_BOOK].get(KEY_BLUEPRINTS, []):
            save_to_fs(bp, bp_path)
        root_dict[KEY_BOOK].pop(KEY_BLUEPRINTS, None)
        bp_path = os.path.join(bp_path, ".book.json")
        if os.path.exists(bp_path):
            raise BpCaptureException(".book is a reserved name for blueprints. Please rename")
    try:
        with open(bp_path, 'w') as bp_file:
            bp_file.write(json.dumps(root_dict, indent=4, sort_keys=True))
    except IOError:
        raise BpCaptureException("Failed to create file: {}".format(bp_path))


def capture_from_clip(root_path: str) -> None:
    clipboard = pyperclip.paste()
    if (not clipboard) or (clipboard[0] != '0'):
        raise BpCaptureException("Clipboard does not contain a valid blueprint")
    try:
        root_dict = json.loads(zlib.decompress(base64.b64decode(clipboard.encode('ascii')[1:])).decode('utf-8'))
    except (zlib.error, binascii.Error):
        raise BpCaptureException("Clipboard does not contain a valid blueprint")
    save_to_fs(root_dict, root_path)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("root_path", help="Existing directory to save book directory or blueprint into", type=str)
    args = parser.parse_args()
    if not os.path.isdir(args.root_path):
        print("Directory does not exist: {}". format(args.root_path))
        exit(-1)
    root = os.path.abspath(args.root_path)
    try:
        capture_from_clip(root)
        print("Clipboard captured")
        exit(0)
    except BpCaptureException as e:
        print(str(e))
        exit(-1)



