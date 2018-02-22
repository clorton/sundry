#!/usr/bin/python

import argparse
import hashlib
import re
import sys
import urllib.error
import urllib.request


def get_hash(string):
    sha = hashlib.sha1()
    sha.update(string.encode())
    hash = sha.hexdigest()

    return hash


def main(passwords):

    for password in passwords:
        sha = get_hash(password)
        url = 'https://api.pwnedpasswords.com/range/{0}'.format(sha[:5])
        try:
            request = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            with urllib.request.urlopen(request) as response:
                results = str(response.read(), 'utf-8').split()
                suffix = sha[5:].upper()
                found = False
                for entry in results:
                    if entry.startswith(suffix):
                        count = entry.split(':')[1]
                        print('{0}: {1} matches found in the database'.format(password, count))
                        found = True
                if not found:
                    print('{0}: not found in the database'.format(password))

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("{0}: didn't have any matches".format(password))
            else:
                print("{0}: GET for '{1}' returned code {2}".format(password, url, e.code))

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('passwords', nargs='+')
    args = parser.parse_args()
    main(args.passwords)
    sys.exit(0)
