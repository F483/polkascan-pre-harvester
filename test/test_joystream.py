from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from unittest import TestCase

from app.settings import DB_CONNECTION_TEST, DEBUG
from app.models.data import Extrinsic

Session = sessionmaker()
engine = create_engine(DB_CONNECTION_TEST, echo=DEBUG, isolation_level="READ_UNCOMMITTED")

# set up sqlalchemy orm events
from app.models.event_listeners import *

class JoystreamTest(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        # attach orm listeners
        event.listen(self.session, 'after_flush', receive_after_flush)

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
