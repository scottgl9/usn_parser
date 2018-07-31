#!/usr/bin/python

from HTMLParser import HTMLParser
import requests
import sys

cve_list = []

class MyHTMLParser(HTMLParser):
    #def handle_starttag(self, tag, attrs):
    #    print "Encountered a start tag:", tag

    #def handle_endtag(self, tag):
    #    print "Encountered an end tag :", tag

    def handle_data(self, data):
        if data.startswith('CVE-'):
            print(data)
            cve_list.append(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <USN>".format(sys.argv[0]))
        sys.exit(0)

    usn_name = sys.argv[1]
    r = requests.get("https://usn.ubuntu.com/{}/".format(usn_name))

    parser = MyHTMLParser()
    parser.feed(r.text)

    for cve in cve_list:
        r = requests.get("https://nvd.nist.gov/vuln/detail/{}".format(cve))
        print(r.text)
