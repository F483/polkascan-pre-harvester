from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from unittest import TestCase

from app.settings import DB_CONNECTION_TEST, DEBUG
from app.models.data import Extrinsic

Session = sessionmaker()
engine = create_engine(DB_CONNECTION_TEST, echo=DEBUG, isolation_level="READ_UNCOMMITTED")

class JoystreamExtrinsicTest(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

    def test_create_extrinsic(self):
        self.session.add(Extrinsic(
            block_id=100,
            extrinsic_idx=1,
            extrinsic_hash="0xbeef",
            signed=10,
            unsigned=20,
            signedby_address=1100,
            signedby_index=1,
            success=1,
            error=0
        ))
        self.session.commit()

if __name__ == '__main__':
    unittest.main()
