import sqlalchemy as sa
from test.test_joystream import JoystreamTest
from app.models.data import Extrinsic, Event
from app.models.joystream import Category

import json

class JoystreamExtrinsicTest(JoystreamTest):
    def test_create_extrinsic(self):
        extrinsic = Extrinsic(
            block_id=100,
            extrinsic_idx=1,
            extrinsic_hash="0xbeef",
            signed=10,
            unsigned=20,
            signedby_address=1100,
            signedby_index=1,
            success=1,
            error=0
        )
        self.session.add(extrinsic)
        self.session.commit()
        count = Extrinsic.query(self.session).filter_by(block_id=100).count()
        self.assertEqual(count, 1)

    def test_create_category_extrinsic(self):
        """Assumes that harvester always processes events before processing extrinsics"""
        category_extrinsic_params = [{'name': 'parent', 'type': 'Option<CategoryId>', 'value': None, 'valueRaw': '00'}, {'name': 'title', 'type': 'Bytes', 'value': 'Another category', 'valueRaw': '416e6f746865722063617465676f7279'}, {'name': 'description', 'type': 'Bytes', 'value': 'Need a new category in the db', 'valueRaw': '4e6565642061206e65772063617465676f727920696e20746865206462'}]
        category_event_attributes = [{'type': 'CategoryId', 'value': 3, 'valueRaw': '0300000000000000'}]

        event = Event(
            block_id=100,
            extrinsic_idx=1,
            event_idx=1,
            module_id='forum',
            event_id='CategoryCreated',
            system=0, # this is not a system event
            module=1, # instead, this is a module event
            attributes=category_event_attributes
        )
        self.session.add(event)
        self.session.flush()

        count = Category.query(self.session).filter_by(block_id=100).count()
        self.assertEqual(count, 1)

        extrinsic = Extrinsic(
            block_id=100,
            extrinsic_idx=1,
            extrinsic_hash="0xbeef",
            signed=10,
            unsigned=20,
            signedby_address=1100,
            signedby_index=1,
            success=1,
            error=0,
            module_id='forum',
            call_id='create_category',
            params=category_extrinsic_params
        )
        self.session.add(extrinsic)
        self.session.flush()

        count = Category.query(self.session).filter_by(block_id=100).count()
        self.assertEqual(count, 1)

        category = Category.query(self.session).filter_by(block_id=100).first()
        self.assertEqual(category.title, 'Another category')
        self.assertEqual(category.description, 'Need a new category in the db')

if __name__ == '__main__':
    unittest.main()
