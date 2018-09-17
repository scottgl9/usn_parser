#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import requests
import sys

class PackageNameParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.last_tag = self.tag
        self.tag = tag

    def handle_data(self, data):
        if self.tag == 'dt':
            if len(data) > 1:
                self.last_version = str(data)
            return

        if self.last_tag != 'dd' or self.tag != 'a':
            return
        if self.ubuntu_version not in self.last_version:
            return

        tag = str(self.get_starttag_text())
        if 'launchpad.net' in tag and len(data) > 3:
            if data not in self.package_list:
                if 'linux-image-' not in data:
                    self.package_list.append(data)

class CVEParser(HTMLParser):
    def handle_data(self, data):
        if data.startswith('CVE-'):
            self.cve_list.append(data)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <usn_list_file> <ubuntu version>".format(sys.argv[0]))
        sys.exit(0)

    print("Getting filtered list of Ubuntu {} packages...".format(sys.argv[2]))

    for line in open(sys.argv[1]):
        usn_name = line.strip().replace('USN-', '')
        #print(usn_name)
        r = requests.get("https://usn.ubuntu.com/{}/".format(usn_name))
        pname_parser = PackageNameParser()
        pname_parser.tag = ''
        pname_parser.last_tag = ''
        pname_parser.ubuntu_version = str(sys.argv[2])
        pname_parser.last_version = ''
        pname_parser.package_list = []
        pname_parser.feed(r.text)
        package_list = pname_parser.package_list
        cve_parser = CVEParser()
        cve_parser.cve_list = []
        cve_parser.feed(r.text) 
        cve_list = ",".join(cve_parser.cve_list)
        
        for package in package_list:
            if package == 'firefox': continue
            print("{}: {}".format(package, cve_list))

