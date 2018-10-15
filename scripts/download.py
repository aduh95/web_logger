#!/usr/bin/env python3

from os import path

WWW_FOLDER = path.join(path.realpath(path.dirname(__file__)), "..", "www")


def write_menu(outputFile, table_headers):
    outputFile.write("\t<main>\n")
    outputFile.write("\t\t<!-- Customize table headers here -->\n")
    for header in table_headers:
        outputFile.write("\t\t<h3></h3>\n".format(header))
    outputFile.write("\t\t<!-- ---------------------------- -->\n")


if __name__ == "__main__":
    table_headers = input(
        "Enter a comma separated list of the table header of your logger [Date,Time,Object,Message]:"
    )
    if table_headers:
        table_headers = table_headers.split(",")
    else:
        table_headers = ["Date", "Time", "Object", "Message"]

    with open(path.join(WWW_FOLDER, "index.html"), "rt", encoding="utf8") as inputFile:
        with open(path.join(".", "index.html"), "w", encoding="utf8") as outputFile:
            for line in inputFile.readline():
                if line.trim() == "<main>":
                    write_menu(outputFile, table_headers)
                    while inputFile.readline().trim() != "</main>":
                        pass
                else:
                    outputFile.write(line)

