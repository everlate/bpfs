# Converter from Factorio book/blueprint in the clipboard to the directory tree of JSONs and back
## Rationale
Factorio blueprint libraries are difficult to edit in text mode and maintain in version control systems
partly due to the large size of the single JSON exported from the game.

This project allows to parse the decoded JSON into the directory structure of individual blueprints.
Such structure is good for version control and manual editing.

## Directory structure
- dir: [book label]
  - file: .book.json
  - file: [blueprint1 label].json
  - dir: [nested book label]
    - file: .book.json
    - file: [blueprint2 label].json

## Usage:
bpcapture.py decodes clipboard contents into directory tree. Given you initialized blueprint repository in blueprint-repo directory:

    python3 bpcapture.py blueprint-repo

bpdeploy.py encodes the selected directory or blueprint into the clipboard string. For example

    python3 bpdeploy.py blueprint-repo/mining
    
 or
 
    python3 bpdeploy.py blueprint-repo/mining/drill-field-efficiency.json
    
## Installation
Python >= 3.5 is required.
The project uses pyperclip as a cross-platform clipboard library. 
Under Linux it additionally needs xclip or xsel installed.

Pyperclip can be installed via PyPI

    pip3 install pyperclip
    
The project was not yet tested under Windows.

## Testing
    cd bpfs
    python3 -m unittest discover tests
