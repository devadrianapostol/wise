""" Test dexterity """

import unittest

import lxml.etree

from eea.rdfmarshaller.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.textfield.value import RichTextValue
from zope.component import getMultiAdapter

words = """<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi
ultrices id arcu vitae accumsan. Nam laoreet felis in laoreet maximus. Sed
risus eros, aliquam at purus in, dapibus accumsan turpis. Donec venenatis ac
nisl ac sagittis. Aliquam laoreet diam ipsum, sit amet tempus ex placerat in.
Ut suscipit fermentum tellus, in pharetra erat auctor tincidunt. Curabitur
elementum congue urna, ut hendrerit lectus mattis et. Vestibulum et tristique
eros, et finibus sapien. Mauris sit amet blandit lectus. Sed vitae quam est.
Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi sed tempor
lectus. Morbi facilisis mollis maximus. Nulla at neque mi. Donec tempor tempus
rhoncus. Quisque nec suscipit dui, et posuere est.</p>

<p>Etiam at pretium tortor. Duis eget neque dapibus, aliquet lectus ut,
pharetra dui. Donec venenatis sed nibh at aliquet. Nam non tempor purus.
Phasellus sed nibh ipsum. Aliquam quis rutrum massa, ut vestibulum nunc. Mauris
placerat dignissim lectus et lacinia. Pellentesque at eleifend metus. Ut vitae
massa sed nisi varius pulvinar luctus id leo. Suspendisse varius orci felis,
non sagittis odio lobortis quis. Nulla et mollis urna. Mauris non nunc nisl.
</p>"""

NSMAP = {
    'RDF': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'RDFS': "http://www.w3.org/2000/01/rdf-schema#",
    "dcterms": "http://purl.org/dc/terms/"
}


class TestProgramIntegration(unittest.TestCase):
    """ Integration testing """

    layer = INTEGRATION_TESTING

    def setUp(self):
        """ Setup """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('testpage', 'test-page')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.page = self.portal['test-page']
        self.page.edit(title="Test title", description="Test description")

    def test_rdf_view(self):
        """ test rdf view """
        req = self.portal.REQUEST
        rdf = getMultiAdapter((self.page, req), name="rdf")()

        assert "<dcterms:creator>test_user_1_</dcterms:creator>" in rdf
        assert "<dcterms:description>Test description</dcterms:description>" \
            in rdf
        assert "<dcterms:title>Test title</dcterms:title>" in rdf

    def test_rdfs_view(self):
        """ test rdfs view """
        ptypes = self.portal['portal_types']
        testpage_fti = ptypes['testpage']
        req = self.portal.REQUEST
        view = getMultiAdapter((testpage_fti, req), name="rdf")
        rdf = view()

        if isinstance(rdf, unicode):
            rdf = rdf.encode()
        e = lxml.etree.fromstring(rdf)
        props = e.xpath('//RDFS:Property', namespaces=NSMAP)
        fields = [x.xpath('RDF:id', namespaces=NSMAP)[0].text for x in props]
        assert set([f for f in fields if f in ['description', 'effective',
                                               'expires', 'subjects', 'title']
                    ])

    def test_shorten_description(self):
        """ Test shorten description field """

        from eea.rdfmarshaller.dexterity.fields import ShortenHTMLField2Surf
        from eea.rdfmarshaller.dexterity.interfaces import IDXField2Surf
        from zope.component import getGlobalSiteManager
        from zope.interface import Interface

        req = self.portal.REQUEST

        rdf = getMultiAdapter((self.page, req), name="rdf")()
        e = lxml.etree.fromstring(rdf.encode('utf-8'))

        assert e.xpath('//dcterms:description/text()',
                       namespaces=NSMAP) == ['Test description']

        text = RichTextValue(words, 'text/html', 'text/html')
        self.page.long_description = text
        self.page.edit(description="")

        class DescriptionOverride(ShortenHTMLField2Surf):
            alternate_field = 'long_description'

        gsm = getGlobalSiteManager()
        gsm.registerAdapter(DescriptionOverride,
                            [Interface, Interface, Interface],
                            IDXField2Surf,
                            name="description",)

        view = getMultiAdapter((self.page, req), name="rdf")
        rdf = view()
        e = lxml.etree.fromstring(rdf.encode('utf-8'))

        assert e.xpath('//dcterms:description/text()', namespaces=NSMAP) == \
            ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.']

        gsm.adapters.unregister([Interface, Interface, Interface],
                                IDXField2Surf, 'description')


def test_suite():
    """ test suite """

    return unittest.defaultTestLoader.loadTestsFromName(__name__)
