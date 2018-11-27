#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import requests
import sys
import re

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


# <td>Fixed by <a href="http://git.kernel.org/linus/7992c18810e568b95c869b227137a2215702a805">7992c18810e568b95c869b227137a2215702a805</a></td>

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <cve_list_file>".format(sys.argv[0]))
        sys.exit(0)

    for cveline in open(sys.argv[1]):
        cve_name = cveline.strip()
        cve_year = cve_name.split('-')[1]
        r = requests.get("https://people.canonical.com/~ubuntu-security/cve/{}/{}.html".format(cve_year, cve_name))

        m = re.search("Fixed by <a href=\"http://git.kernel.org/(\S)+", r.text)
        line = m.group(0).replace("Fixed by ", "").replace("</td></tr>", "")
        print("{}: {}".format(cve_name, line))
