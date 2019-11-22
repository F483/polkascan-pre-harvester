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

class Category(BaseModel):
    __tablename__ = 'forum_category'

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=False)
    # extracted from position_in_parent_category
    parent_id = sa.Column(sa.BigInteger())

    title = sa.Column(sa.String(150))
    description = sa.Column(sa.String(150))
    created_at = sa.Column(sa.DateTime())
    deleted = sa.Column(sa.Boolean())
    archived = sa.Column(sa.Boolean())
    num_direct_subcategories = sa.Column(sa.Integer())
    num_direct_unmoderated_threads = sa.Column(sa.Integer())
    num_direct_moderated_threads = sa.Column(sa.Integer())

    # extracted from position_in_parent_category
    position_in_parent_category = sa.Column(sa.Integer())

    account_id = sa.Column(sa.Integer)

# class Post(BaseModel):
#     __tablename__ = 'forum_post'

#     id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=False)
