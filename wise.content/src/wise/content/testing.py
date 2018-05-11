# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import wise.content


class WiseContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=wise.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'wise.content:default')


WISE_CONTENT_FIXTURE = WiseContentLayer()


WISE_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(WISE_CONTENT_FIXTURE,),
    name='WiseContentLayer:IntegrationTesting'
)


WISE_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(WISE_CONTENT_FIXTURE,),
    name='WiseContentLayer:FunctionalTesting'
)
