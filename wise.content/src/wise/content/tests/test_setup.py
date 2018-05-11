# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from wise.content.testing import WISE_CONTENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that wise.content is properly installed."""

    layer = WISE_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if wise.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'wise.content'))

    def test_browserlayer(self):
        """Test that IWiseContentLayer is registered."""
        from wise.content.interfaces import (
            IWiseContentLayer)
        from plone.browserlayer import utils
        self.assertIn(IWiseContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = WISE_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['wise.content'])

    def test_product_uninstalled(self):
        """Test if wise.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'wise.content'))

    def test_browserlayer_removed(self):
        """Test that IWiseContentLayer is removed."""
        from wise.content.interfaces import \
            IWiseContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(IWiseContentLayer, utils.registered_layers())
