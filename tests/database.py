
global DATABASE
DATABASE = {}


def get_db():
    global DATABASE
    return DATABASE


def update_db(new_db):
    global DATABASE
    DATABASE = new_db


def clear_db():
    global DATABASE
    DATABASE = {}
