import os
import hashlib
import argparse

from pathlib import Path


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True,
                        help='scanning path')
    parser.add_argument('--fmt', type=str, default='*',
                        help='fmt')
    parser.add_argument('--rm', default=False, action='store_true',
                        help='removes duplicate files automatically')

    args = parser.parse_args()

    hash_db = dict()

    for fpath in Path(args.path).rglob('*.' + args.fmt):
        if not os.path.isfile(fpath):
            continue

        fmd5 = md5(fpath)

        if fmd5 in hash_db:
            print("%s is a duplicate of %s" % (fpath, hash_db[fmd5]))
            if args.rm:
                print("Removing %s" % fpath)
                os.remove(fpath)
        else:
            hash_db[fmd5] = fpath
