import sqlalchemy as sa
from test.test_joystream import JoystreamTest
from app.models.data import Extrinsic, Event
from app.models.joystream import Category, Thread, Post, ModerationAction

import json

class JoystreamForumAssociationTest(JoystreamTest):
    def test_create_category(self):
        category = Category(
            id = 1,
            title = 'A title',
            description = 'A description',
            block_id = 100
        )
        self.session.add(category)
        self.session.commit()

        assert category is not None
        assert len(category.threads) is 0

        thread = Thread(
            id = 1,
            category = category,
            title = "A thread title",
            block_id = 101
        )
        self.session.add(thread)
        self.session.commit()

        assert thread is not None
        assert len(category.threads) is 1


        post = Post(
            id = 1,
            thread = thread,
            current_text = 'Some text',
            block_id = 102
        )

        self.session.add(thread)
        self.session.commit()

        assert post is not None
        assert len(thread.posts) is 1
