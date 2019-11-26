from sqlalchemy import event

from app.models.base import BaseModel
from app.models.data import Block, Event, Extrinsic
from app.models.joystream import Category

def receive_after_flush(session, flush_context):
    for record in session.new:
        if record.__class__.__name__ == 'Extrinsic':
            if record.call_id == 'create_category':
                category = session.query(Category).filter(Category.block_id==record.block_id, Category.extrinsic_idx==record.extrinsic_idx)
                if category.count() == 1:
                    for param in record.params:
                        if param['name'] == 'parent':
                            category.update({Category.parent_id: param['value']})
                        elif param['name'] == 'title':
                            category.update({Category.title: param['value']})
                        elif param['name'] == 'description':
                            category.update({Category.description: param['value']})
        elif record.__class__.__name__ == 'Event':
            if record.event_id == 'CategoryCreated':
                categoryId = record.attributes[0]['value']
                existing = Category.query(session).filter_by(id=categoryId).count() != 0
                if not existing:
                    category = Category(
                        block_id = record.block_id,
                        extrinsic_idx = record.extrinsic_idx,
                        event_idx = record.event_idx,
                        id = categoryId
                    )
                    session.add(category)
