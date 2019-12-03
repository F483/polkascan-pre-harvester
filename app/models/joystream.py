#  Polkascan PRE Harvester
#
#  Copyright 2018-2019 openAware BV (NL).
#  This file is part of Polkascan.
#
#  Polkascan is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Polkascan is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Polkascan. If not, see <http://www.gnu.org/licenses/>.
#
#  data.py

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.data import Block, Extrinsic

# Captures the Forum Category
# indexes on id, parent_id, title, description, created_at and account_id
class Category(BaseModel):
    __tablename__ = 'joystream_forum_category'

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=False, index=True)
    # extracted from position_in_parent_category
    parent_id = sa.Column(sa.BigInteger(), index=True)

    title = sa.Column(sa.String(150), index=True)
    description = sa.Column(sa.String(150), index=True)

    created_at_block_number = sa.Column(sa.Integer())
    created_at_moment = sa.Column(sa.BigInteger())

    deleted = sa.Column(sa.Boolean())
    archived = sa.Column(sa.Boolean())

    num_direct_subcategories = sa.Column(sa.Integer())
    num_direct_unmoderated_threads = sa.Column(sa.Integer())
    num_direct_moderated_threads = sa.Column(sa.Integer())

    # extracted from position_in_parent_category
    position_in_parent_category = sa.Column(sa.Integer())

    account_id = sa.Column(sa.String(64))

    # block and extrinsic index
    block_id = sa.Column(sa.Integer(), primary_key=True, index=True)
    block = relationship(Block, foreign_keys=[block_id], primaryjoin=block_id == Block.id)
    extrinsic_idx = sa.Column(sa.Integer())
    event_idx = sa.Column(sa.Integer())

    threads = relationship('Thread', backref='category')

thread_moderation_association = sa.Table('joystream_forum_thread_moderation', BaseModel.metadata,
                                         sa.Column('thread_id', sa.BigInteger(), sa.ForeignKey('joystream_forum_thread.id')),
                                         sa.Column('moderation_action_id', sa.BigInteger(), sa.ForeignKey('joystream_forum_moderation_action.id')),
)

class Thread(BaseModel):
    __tablename__ = 'joystream_forum_thread'

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=False, index=True)

    title = sa.Column(sa.String(150), index=True)
    text = sa.Column(sa.Text())

    category_id = sa.Column(sa.BigInteger(), sa.ForeignKey('joystream_forum_category.id'))

    nr_in_category = sa.Column(sa.Integer())
    num_unmoderated_posts = sa.Column(sa.Integer())
    num_moderated_posts = sa.Column(sa.Integer())

    created_at_block_number = sa.Column(sa.Integer())
    created_at_moment = sa.Column(sa.BigInteger())

    author_id = sa.Column(sa.String(64))

    posts = relationship('Post', backref='thread')

    moderations = relationship('ModerationAction', secondary=thread_moderation_association, backref='thread')

    # block and extrinsic index
    block_id = sa.Column(sa.Integer(), primary_key=True, index=True)
    block = relationship(Block, foreign_keys=[block_id], primaryjoin=block_id == Block.id)
    extrinsic_idx = sa.Column(sa.Integer())
    event_idx = sa.Column(sa.Integer())

class ModerationAction(BaseModel):
    __tablename__ = 'joystream_forum_moderation_action'

    # The id doesn't come from substrate, but is autoincremented here to
    # provide the ModerationAction - ModerationRationale relationship
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True, index=True)

    moderator_id = sa.Column(sa.String(64))
    moderation_rationales = relationship('ModerationRationale', backref='moderation_action')

    moderated_at_block_number = sa.Column(sa.Integer())
    moderated_at_moment = sa.Column(sa.BigInteger())

class ModerationRationale(BaseModel):
    __tablename__ = 'joystream_forum_moderation_rationale'

    # The id doesn't come from substrate, but is autoincremented here to
    # provide the ModerationAction - ModerationRationale relationship
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True, index=True)

    moderation_action_id = sa.Column(sa.BigInteger(), sa.ForeignKey('joystream_forum_moderation_action.id'))
    rationale = sa.Column(sa.Integer())

class Post(BaseModel):
    __tablename__ = 'joystream_forum_post'

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=False, index=True)

    # Don't set up fk or relationship
    thread_id = sa.Column(sa.BigInteger(), sa.ForeignKey('joystream_forum_thread.id'))
    author_id = sa.Column(sa.String(64))

    nr_in_thread = sa.Column(sa.Integer())
    current_text = sa.Column(sa.Text())

    post_text_change_history = relationship('PostTextChangeHistory', backref='post')

    created_at_block_number = sa.Column(sa.Integer())
    created_at_moment = sa.Column(sa.BigInteger())

    # block and extrinsic index
    block_id = sa.Column(sa.Integer(), primary_key=True, index=True)
    block = relationship(Block, foreign_keys=[block_id], primaryjoin=block_id == Block.id)
    extrinsic_idx = sa.Column(sa.Integer())
    event_idx = sa.Column(sa.Integer())

class PostTextChangeHistory(BaseModel):
    __tablename__ = 'joystream_forum_post_text_change_history'

        # The id doesn't come from substrate, but is autoincremented here to
    # provide the ModerationAction - ModerationRationale relationship
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True, index=True)

    expired_at_block_number = sa.Column(sa.Integer())
    expired_at_moment = sa.Column(sa.BigInteger())
    text = sa.Column(sa.Text())

    post_id = sa.Column(sa.BigInteger(), sa.ForeignKey('joystream_forum_post.id'))

    author_id = sa.Column(sa.String(64))

post_moderation_association = sa.Table('joystream_forum_post_moderation', BaseModel.metadata,
                                       sa.Column('post_id', sa.BigInteger(), sa.ForeignKey('joystream_forum_post.id')),
                                       sa.Column('moderation_action_id', sa.BigInteger(), sa.ForeignKey('joystream_forum_moderation_action.id')),
)
