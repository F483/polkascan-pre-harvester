import sqlalchemy as sa
from test.test_joystream import JoystreamTest
from app.models.data import Extrinsic, Event
from app.models.joystream import Category, Thread, Post

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

    def test_create_category_thread_post(self):
        """Assumes that harvester always processes events before processing extrinsics"""
        category_extrinsic_params = [{'name': 'parent', 'type': 'Option<CategoryId>', 'value': None, 'valueRaw': '00'}, {'name': 'title', 'type': 'Bytes', 'value': 'Another category', 'valueRaw': '416e6f746865722063617465676f7279'}, {'name': 'description', 'type': 'Bytes', 'value': 'Need a new category in the db', 'valueRaw': '4e6565642061206e65772063617465676f727920696e20746865206462'}]
        category_event_attributes = [{'type': 'CategoryId', 'value': 3, 'valueRaw': '0300000000000000'}]

        category_event = Event(
            block_id=100,
            extrinsic_idx=1,
            event_idx=1,
            module_id='forum',
            event_id='CategoryCreated',
            system=0, # this is not a system event
            module=1, # instead, this is a module event
            attributes=category_event_attributes
        )
        self.session.add(category_event)
        self.session.flush()

        category_count = Category.query(self.session).filter_by(block_id=100).count()
        self.assertEqual(category_count, 1)

        category_extrinsic = Extrinsic(
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
        self.session.add(category_extrinsic)
        self.session.flush()

        count = Category.query(self.session).filter_by(block_id=100).count()
        self.assertEqual(count, 1)

        category = Category.query(self.session).filter_by(block_id=100).first()
        self.assertEqual(category.title, 'Another category')
        self.assertEqual(category.description, 'Need a new category in the db')

        thread_event = Event(
            block_id=101,
            extrinsic_idx=1,
            event_idx=1,
            module_id='forum',
            event_id='ThreadCreated',
            system=0, # this is not a system event
            module=1, # instead, this is a module event
            attributes=[{"type": "ThreadId", "value": 2, "valueRaw": "0200000000000000"}]
        )
        self.session.add(thread_event)
        self.session.flush()

        thread_count = Thread.query(self.session).filter_by(block_id=101).count()
        self.assertEqual(thread_count, 1)

        thread_extrinsic = Extrinsic(
            block_id=101,
            extrinsic_idx=1,
            extrinsic_hash="0xbeef",
            signed=10,
            unsigned=20,
            signedby_address=1100,
            signedby_index=1,
            success=1,
            error=0,
            module_id='forum',
            call_id='create_thread',
            params=[{"name": "category_id", "type": "CategoryId", "value": 3, "valueRaw": "0300000000000000"}, {"name": "title", "type": "Bytes", "value": "a test thread", "valueRaw": "61207465737420746872656164"}, {"name": "text", "type": "Bytes", "value": "here is a test thread", "valueRaw": "686572652069732061207465737420746872656164"}]
         )
        self.session.add(thread_extrinsic)
        self.session.flush()

        thread = Thread.query(self.session).filter_by(block_id=101).first()
        self.assertEqual(thread.title, 'a test thread')
        self.assertEqual(thread.text, 'here is a test thread')
        self.assertEqual(thread.category_id, 3)

        post_event = Event(
            block_id=102,
            extrinsic_idx=1,
            event_idx=1,
            module_id='forum',
            event_id='PostAdded',
            system=0, # this is not a system event
            module=1, # instead, this is a module event
            attributes=[{"type": "PostId", "value": 2, "valueRaw": "0200000000000000"}]
        )
        self.session.add(post_event)
        self.session.flush()

        post = Post.query(self.session).filter_by(block_id=102).first()
        assert post is not None

        post_extrinsic = Extrinsic(
            block_id=102,
            extrinsic_idx=1,
            extrinsic_hash="0xbeef",
            signed=10,
            unsigned=20,
            signedby_address=1100,
            signedby_index=1,
            success=1,
            error=0,
            module_id='forum',
            call_id='add_post',
            params=[{"name": "thread_id", "type": "ThreadId", "value": 2, "valueRaw": "0200000000000000"}, {"name": "text", "type": "Bytes", "value": "Here is a reply to the test thread", "valueRaw": "486572652069732061207265706c7920746f20746865207465737420746872656164"}]
         )
        self.session.add(post_extrinsic)
        self.session.flush()

        post = Post.query(self.session).filter_by(block_id=102).first()
        self.assertEqual(post.current_text, 'Here is a reply to the test thread')
        self.assertEqual(post.thread_id, 2)

if __name__ == '__main__':
    unittest.main()
