#!/usr/bin/python

from HTMLParser import HTMLParser
import requests
import sys

cve_list = []
cve_score_list = {}
cve_sev_list = {}

class CVEParser(HTMLParser):
    def handle_data(self, data):
        if data.startswith('CVE-'):
            cve_list.append(data)

class CVSSParser(HTMLParser):
    cve=''
    #def handle_starttag(self, tag, attrs):
    #    print "Encountered a start tag:", tag

    def handle_data(self, data):
        tag = str(self.get_starttag_text())
        if not tag.startswith('<span') or len(data.strip()) == 0:
            return
        if 'vuln-cvssv3-base-score-severity' in tag:
            cve_sev_list[cve] = data
        elif 'vuln-cvssv3-base-score' in tag:
            cve_score_list[cve] = data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <USN>".format(sys.argv[0]))
        sys.exit(0)

    usn_name = sys.argv[1]
    r = requests.get("https://usn.ubuntu.com/{}/".format(usn_name))

    cveparser = CVEParser()
    cveparser.feed(r.text)

    cvssparser = CVSSParser()

    for cve in cve_list:
        r = requests.get("https://nvd.nist.gov/vuln/detail/{}".format(cve))
        cvssparser.cve = cve
        cvssparser.feed(r.text)

    for key, value in sorted(cve_score_list.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print("{}: {} {}".format(key, value, cve_sev_list[key]))

