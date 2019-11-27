#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-only

#
# Copyright (C) 2019 Datto, Inc.
# Additional contributions by Assurio Software, Inc are Copyright (C) 2019 Assurio Software Inc.
#

import errno
import os
import unittest

import assurio-snap
import util
from devicetestcase import DeviceTestCase


class TestSetup(DeviceTestCase):
    def setUp(self):
        self.device = "/dev/loop0"
        self.mount = "/tmp/assurio-snap"
        self.cow_file = "cow.snap"
        self.cow_full_path = "{}/{}".format(self.mount, self.cow_file)
        self.minor = 1
        self.snap_device = "/dev/assurio-snap{}".format(self.minor)

    def test_setup_invalid_minor(self):
        self.assertEqual(assurio-snap.setup(1000, self.device, self.cow_full_path), errno.EINVAL)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_volume_path_is_dir(self):
        self.assertEqual(assurio-snap.setup(self.minor, self.mount, self.cow_full_path), errno.ENOTBLK)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_cow_file_path_is_dir(self):
        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.mount), errno.EISDIR)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_cow_file_on_wrong_device(self):
        self.assertEqual(assurio-snap.setup(self.minor, self.device, "/tmp/{}".format(self.cow_file)), errno.EINVAL)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_unmounted_volume(self):
        util.unmount(self.mount)
        self.addCleanup(util.mount, self.device, self.mount)

        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.cow_full_path), errno.EINVAL)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_readonly_volume(self):
        util.mount(self.device, self.mount, opts="remount,ro")
        self.addCleanup(util.mount, self.device, self.mount, opts="remount,rw")

        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.cow_full_path), errno.EINVAL)
        self.assertFalse(os.path.exists(self.snap_device))
        self.assertIsNone(assurio-snap.info(self.minor))

    def test_setup_already_tracked_volume(self):
        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.cow_full_path), 0)
        self.addCleanup(assurio-snap.destroy, self.minor)

        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.cow_full_path), errno.EBUSY)
        self.assertTrue(os.path.exists(self.snap_device))
        self.assertIsNotNone(assurio-snap.info(self.minor))

    def test_setup_volume(self):
        self.assertEqual(assurio-snap.setup(self.minor, self.device, self.cow_full_path), 0)
        self.addCleanup(assurio-snap.destroy, self.minor)

        self.assertTrue(os.path.exists(self.snap_device))

        snapdev = assurio-snap.info(self.minor)
        self.assertIsNotNone(snapdev)

        self.assertEqual(snapdev["error"], 0)
        self.assertEqual(snapdev["state"], 3)
        self.assertEqual(snapdev["cow"], "/{}".format(self.cow_file))
        self.assertEqual(snapdev["bdev"], self.device)
        self.assertEqual(snapdev["version"], 1)


if __name__ == "__main__":
    unittest.main()