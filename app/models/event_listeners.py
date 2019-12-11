from sqlalchemy import event

from app.models.base import BaseModel
from app.models.data import Block, Event, Extrinsic
from app.models.joystream import Category, Thread, Post

def receive_after_flush(session, flush_context):
    '''This is the SQLAlchemy Listener that handles Joystream data'''
    for record in session.new:
        if record.__class__.__name__ == 'Event':
            handle_event(session, record)
        elif record.__class__.__name__ == 'Extrinsic':
            handle_extrinsic(session, record)


def handle_event(session, record):
    '''Invoked in response to a Joystream SRML event'''
    if record.event_id == 'CategoryCreated':
        create_category(session, record)
    elif record.event_id == 'ThreadCreated':
        create_thread(session, record)
    elif record.event_id == 'PostAdded':
        create_post(session, record)

def handle_extrinsic(session, record):
    '''Invoked in response to a Joystream SRML extrinsic'''
    if record.call_id == 'create_category':
        update_category(session, record)
    elif record.call_id == 'create_thread':
        update_thread(session, record)
    elif record.call_id == 'add_post':
        update_post(session, record)

def create_category(session, record):
    '''Create category in response to Category Event'''
    categoryId = record.attributes[0]['value']
    existing = Category.query(session).filter_by(id=categoryId).count() != 0
    if existing:
        return
    category = Category(
        block_id = record.block_id,
        extrinsic_idx = record.extrinsic_idx,
        event_idx = record.event_idx,
        id = categoryId
    )
    session.add(category)

def update_category(session, record):
    '''Update category in response to Category Extrinsic'''
    category = session.query(Category).filter(Category.block_id==record.block_id, Category.extrinsic_idx==record.extrinsic_idx)
    if category.count() != 1:
        return
    for param in record.params:
        if param['name'] == 'parent':
            category.update({Category.parent_id: param['value']})
        elif param['name'] == 'title':
            category.update({Category.title: param['value']})
        elif param['name'] == 'description':
            category.update({Category.description: param['value']})

def create_thread(session, record):
    '''Create thread in response to Thread Event'''
    threadId = record.attributes[0]['value']
    existing = Thread.query(session).filter_by(id=threadId).count() != 0
    if existing:
        return
    thread = Thread(
        block_id = record.block_id,
        extrinsic_idx = record.extrinsic_idx,
        event_idx = record.event_idx,
        id = threadId
    )
    session.add(thread)

def update_thread(session, record):
    '''Update thread in response to Thread Extrinsic'''
    thread = session.query(Thread).filter(Thread.block_id==record.block_id, Thread.extrinsic_idx==record.extrinsic_idx)
    if thread.count() != 1:
        return
    for param in record.params:
        if param['name'] == 'parent':
            thread.update({Thread.parent_id: param['value']})
        elif param['name'] == 'title':
            thread.update({Thread.title: param['value']})
        elif param['name'] == 'text':
            thread.update({Thread.text: param['value']})
        elif param['name'] == 'category_id':
            thread.update({Thread.category_id: param['value']})

def create_post(session, record):
    '''Create post in response to Post Event'''
    postId = record.attributes[0]['value']
    existing = Post.query(session).filter_by(id=postId).count() != 0
    if existing:
        return
    post = Post(
        block_id = record.block_id,
        extrinsic_idx = record.extrinsic_idx,
        event_idx = record.event_idx,
        id = postId
    )
    session.add(post)

def update_post(session, record):
    '''Update post in response to Post Extrinsic'''
    post = session.query(Post).filter(Post.block_id==record.block_id, Post.extrinsic_idx==record.extrinsic_idx)
    if post.count() != 1:
        return
    for param in record.params:
        if param['name'] == 'parent':
            post.update({Post.parent_id: param['value']})
        elif param['name'] == 'text':
            post.update({Post.current_text: param['value']})
        elif param['name'] == 'thread_id':
            post.update({Post.thread_id: param['value']})
