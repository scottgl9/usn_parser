#!/usr/bin/python

from HTMLParser import HTMLParser
import requests
import sys

package_list = []

class PackageNameParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.last_tag = self.tag
        self.tag = tag

    def handle_data(self, data):
        tag = str(self.get_starttag_text())
        if not tag.startswith('<a') or len(data.strip()) == 0:
            return
        if 'launchpad.net' in tag and self.last_tag == 'dd' and len(data) > 3:
            if data not in package_list:
                package_list.append(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <usn_list_file>".format(sys.argv[0]))
        sys.exit(0)

    for line in open(sys.argv[1]):
        package_list = []
        r = requests.get("https://usn.ubuntu.com/{}/".format(line.strip()))
        pname_parser = PackageNameParser()
        pname_parser.tag = ''
        pname_parser.feed(r.text)
        print(package_list)

