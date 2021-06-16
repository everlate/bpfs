#!/usr/bin/python3

import pyperclip
import zlib
import base64
import json
import os
from argparse import ArgumentParser

KEY_BOOK = "blueprint_book"
KEY_BLUEPRINTS = "blueprints"


class BpDeployException(Exception):
    pass


def load_from_fs(root_path: str):
    if os.path.isfile(root_path):
        try:
            with open(root_path) as bp_file:
                return json.load(bp_file)
        except IOError:
            raise BpDeployException("Failed to read file: {}".format(root_path))
        except json.JSONDecodeError as e:
            raise BpDeployException("Invalid format of the file {}".format(root_path))

    if os.path.isdir(root_path):
        book_bp_path = os.path.join(root_path, ".book.json")
        if not os.path.isfile(book_bp_path):
            raise BpDeployException("Book file not found: {}".format(book_bp_path))
        try:
            with open(book_bp_path) as bp_file:
                root_dict = json.load(bp_file)
        except IOError:
            raise BpDeployException("Failed to read book file: {}".format(book_bp_path))
        except json.JSONDecodeError as e:
            raise BpDeployException("Invalid format of the book file {}".format(book_bp_path))

        root_dict[KEY_BOOK][KEY_BLUEPRINTS] = list()
        for entry in os.listdir(root_path):
            if entry == ".book.json":
                continue
            root_dict[KEY_BOOK][KEY_BLUEPRINTS].append(load_from_fs(os.path.join(root_path, entry)))
        return root_dict

    raise BpDeployException("Symlinks are not supported")


def deploy_to_clip(root_path: str) -> None:
    root_dict = load_from_fs(root_path)
    pyperclip.copy('0' + base64.b64encode(zlib.compress(json.dumps(root_dict, sort_keys=True).encode('utf-8'))).decode('ascii'))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("bp_path", help="Path to book directory or blueprint file", type=str)
    args = parser.parse_args()
    if not os.path.exists(args.bp_path):
        print("Path does not exist: {}". format(args.bp_path))
        exit(-1)
    root = os.path.abspath(args.bp_path)
    try:
        deploy_to_clip(root)
        print("Deployed to clipboard")
        exit(0)
    except BpDeployException as e:
        print(str(e))
        exit(-1)

