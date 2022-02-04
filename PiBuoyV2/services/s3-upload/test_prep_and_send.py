#!/usr/bin/python3

import os
import subprocess
import tempfile
import unittest
from prep_and_send import tar_dir


class prepsendtest(unittest.TestCase):

    def test_tar_dir(self):

        with tempfile.TemporaryDirectory() as tmpdir:
            tar_file = os.path.join(tmpdir, 'test.tar')
            telem_dir = os.path.join(tmpdir, 'test')
            telem_file = os.path.join(telem_dir, 'blah.json')
            ignored_file = os.path.join(telem_dir, '.ignored_json')
            os.mkdir(telem_dir)
            for test_file in (telem_file, ignored_file):
                with open(test_file, 'w') as f:
                    f.write(test_file)
            tar_dir(telem_dir, tar_file, xz=True)
            self.assertTrue(os.path.exists, tar_file)
            in_tar = set()
            with subprocess.Popen(['/usr/bin/tar', 'Jtvf', tar_file], stdout=subprocess.PIPE) as s:
                for tar_line in s.stdout.readlines():
                    tar_line = tar_line.decode('utf-8').strip().split(' ')
                    in_tar.add(tar_line[-1])
            self.assertTrue(os.path.basename(telem_file) in in_tar)
            self.assertFalse(os.path.basename(ignored_file) in in_tar)


if __name__ == '__main__':
    unittest.main()