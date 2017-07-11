# -*- coding: utf-8 -*-
# Luke Jackson

import urllib.request
from bs4 import BeautifulSoup
import argparse
import sys


def get_chapter(url, filename):
    results = []

    with urllib.request.urlopen(url) as response:
        page = response.read()
    soup = BeautifulSoup(page)
    try:
        s = find_all(url, '/')
        chapter_name = url[s[len(s) - 2]+1:s[len(s) - 1]]
        all_text = soup.get_text()
        story = all_text[all_text.index('Next Chapter')+12:all_text.index('Share this:Click to')]

        with open(filename+".txt", "a", encoding='utf-8') as text_file:
            text_file.write(chapter_name+"\n\n")
            text_file.write(story+"\n\n")

    except Exception as e:
        raise
    return results


# used for getting a nice filename
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result


def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('urls_file', type=str, help='text file of all urls to scan')
    parser.add_argument('book_name', type=str, help='name of output file')
    return parser.parse_args(argv)

if __name__ == "__main__":
    arg = parse_arguments(sys.argv[1:])

    f = open(arg.urls_file, 'r')
    raw = f.readlines()
    for each in raw:
        get_chapter(each, arg.book_name)
        print(each + ': done')
    print('all done')
