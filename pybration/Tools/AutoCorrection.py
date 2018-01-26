# -*- coding: utf-8 -*-
import os


def check_dir_str(dir_str: str):
    dir_str = dir_str.replace("//", "/")
    dir_str = dir_str.replace("~", os.environ['HOME'])
    return dir_str


if __name__ == "__main__":
    test = check_dir_str("~//Data")
    print(test)
