from Products.Five.browser import BrowserView
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.interface import Interface
from zope.schema import TextLine
from zope.sqlalchemy import register

DB = "mssql+pymssql://SA:bla3311!@msdb/MarineDB"        # MarineDB

metadata = MetaData()


def _make_session():
    engine = create_engine(DB)
    Session = scoped_session(sessionmaker(bind=engine))
    register(Session, keep_session=True)

    return Session()


class IMainArticle8910(Interface):
    pass


class SearchDemo(BrowserView):
    """ MSFD search demo page
    """

    def __init__(self, context, request):
        super(SearchDemo, self).__init__(context, request)
        session = _make_session()
        self.conn = session.connection()

    @property
    def report_types(self):
        res = self.conn.execute('SELECT ReportType from MSFD13_ReportingInfo')

        return set([r['ReportType'].strip() for r in res])
