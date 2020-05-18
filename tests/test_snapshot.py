#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only

#
# Copyright (C) 2019 Datto, Inc.
# Additional contributions by Elastio Software, Inc are Copyright (C) 2020 Elastio Software Inc.
#

import errno
import os
import unittest

import elastio-snap
import util
from devicetestcase import DeviceTestCase


class TestSnapshot(DeviceTestCase):
    def setUp(self):
        self.device = "/dev/loop0"
        self.mount = "/tmp/elastio-snap"
        self.cow_file = "cow.snap"
        self.cow_full_path = "{}/{}".format(self.mount, self.cow_file)
        self.minor = 1

        self.snap_mount = "/mnt"
        self.snap_device = "/dev/elastio-snap{}".format(self.minor)

    def test_modify_origin(self):
        testfile = "{}/testfile".format(self.mount)
        snapfile = "{}/testfile".format(self.snap_mount)

        with open(testfile, "w") as f:
            f.write("The quick brown fox")

        self.addCleanup(os.remove, testfile)
        os.sync()
        md5_orig = util.md5sum(testfile)

        self.assertEqual(elastio-snap.setup(self.minor, self.device, self.cow_full_path), 0)
        self.addCleanup(elastio-snap.destroy, self.minor)

        with open(testfile, "w") as f:
            f.write("jumps over the lazy dog")

        os.sync()

        util.mount(self.snap_device, self.snap_mount, opts="ro")
        self.addCleanup(util.unmount, self.snap_mount)

        md5_snap = util.md5sum(snapfile)
        self.assertEqual(md5_orig, md5_snap)

    def test_track_writes(self):
        testfile = "{}/testfile".format(self.mount)

        self.assertEqual(elastio-snap.setup(self.minor, self.device, self.cow_full_path), 0)
        self.addCleanup(elastio-snap.destroy, self.minor)

        os.sync()
        info = elastio-snap.info(self.minor)
        start_nr = info["nr_changed_blocks"]
        self.assertNotEqual(start_nr, 0)

        with open(testfile, "w") as f:
            f.write("The quick brown fox")

        self.addCleanup(os.remove, testfile)
        os.sync()

        info = elastio-snap.info(self.minor)
        end_nr = info["nr_changed_blocks"]
        self.assertGreater(end_nr, start_nr)

    def test_next_available_minor(self):
        self.assertEqual(elastio-snap.get_free_minor(), 0)

        # Explicitly use a minor of 0 for testing this function
        self.assertEqual(elastio-snap.setup(0, self.device, self.cow_full_path), 0)
        self.addCleanup(elastio-snap.destroy, 0)

        self.assertEqual(elastio-snap.get_free_minor(), 1)


if __name__ == "__main__":
    unittest.main()
