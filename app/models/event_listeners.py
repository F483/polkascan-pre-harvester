from sqlalchemy import event

from app.models.base import BaseModel
from app.models.data import Block, Event, Extrinsic
from app.models.joystream import Category

def create_category(session, record):
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

def update_category(session, record):
    category = session.query(Category).filter(Category.block_id==record.block_id, Category.extrinsic_idx==record.extrinsic_idx)
    if category.count() == 1:
        for param in record.params:
            if param['name'] == 'parent':
                category.update({Category.parent_id: param['value']})
            elif param['name'] == 'title':
                category.update({Category.title: param['value']})
            elif param['name'] == 'description':
                category.update({Category.description: param['value']})

def create_thread(session, record):
    pass

def update_thread(session, record):
    pass

def create_post(session, record):
    pass

def update_post(session, record):
    pass

def receive_after_flush(session, flush_context):
    for record in session.new:
        if record.__class__.__name__ == 'Event':
            if record.event_id == 'CategoryCreated':
                create_category(session, record)
            elif record.event_id == 'ThreadCreated':
                create_thread(session, record)
            elif record.event_id == 'PostAdded':
                create_post(session, record)
        elif record.__class__.__name__ == 'Extrinsic':
            if record.call_id == 'create_category':
                update_category(session, record)
            elif record.call_id == 'create_thread':
                update_thread(session, record)
            elif record.call_id == 'add_post':
                update_post(session, record)
