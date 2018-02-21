#!/usr/bin/python

from collections import defaultdict
from pathlib import Path
import argparse
import math
import sys


def main(root, quantum):

    if not root.is_dir():
        raise RuntimeError('{0} is not a directory.'.format(root))

    total_count = 0
    total_bytes = 0
    histogram = defaultdict(int)
    for entry in root.glob('**/*'):
        if entry.is_file():
            total_count += 1
            size = entry.stat().st_size
            total_bytes += size
            histogram[math.ceil(size / quantum)] += 1

    print('File count:  {0}'.format(total_count))
    print('Total bytes: {0}'.format(total_bytes))

    count = 0
    for bucket in sorted(histogram.keys()):
        count += histogram[bucket]
        print('{0:9}: {1:6} {2:3}%'.format(bucket * quantum, histogram[bucket], count * 100 // total_count))

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default=str(Path('.')))
    parser.add_argument('-q', '--quantum', default=1024, type=int)

    args = parser.parse_args()

    main(Path(args.directory), args.quantum)
    sys.exit(0)