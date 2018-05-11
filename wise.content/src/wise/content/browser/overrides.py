from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.section.folder import Body as PDFBody
from eea.pdf.themes.page.body import Body as PDFPageBody
from eea.pdf.themes.manual.manual import get_node_html


class FolderBody(PDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("pt/folder.body.pt")

    @property
    def pdfs(self):
        """ Section children
        """
        self._depth += 1
        if self.depth > self.maxdepth:
            return

        ajax_load = self.request.get('ajax_load', False)
        self.request.form['ajax_load'] = True

        parent_brains = self.context.aq_parent.getFolderContents()
        print len(parent_brains)
        for brain in parent_brains:
            if brain.getObject() == self.context:
                node_object = brain.getObject()
                html = get_node_html(node_object=node_object)
                yield html
        self.request.form['ajax_load'] = ajax_load


class PageBody(PDFPageBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile('pt/page.body.pt')
