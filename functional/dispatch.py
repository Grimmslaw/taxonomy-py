import functools

from sqlite3.dbapi2 import Connection

from model.constants import sql as sql_dict
from model.db_data import Rank, Field, GenusType, Suffix, Ranks, Fields, GenusTypes, Suffixes


@functools.singledispatch
def insert_record(record, conn: Connection) -> None:
    raise NotImplementedError


@insert_record.register(Rank)
def _(record: Rank, conn: Connection) -> None:
    cur = conn.cursor()
    if record.field_id is not None:
        cur.execute(sql_dict['insert']['rank'][1], record.to_namedtuple())
    else:
        cur.execute(sql_dict['insert']['rank'][0], record.to_namedtuple())
    conn.commit()


@insert_record.register(Field)
def _(record: Field, conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute(sql_dict['insert']['field'], record.to_namedtuple())
    conn.commit()


@insert_record.register(GenusType)
def _(record: GenusType, conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute(sql_dict['insert']['genus_type'], record.to_namedtuple())
    conn.commit()


@insert_record.register(Suffix)
def _(record: Suffix, conn: Connection) -> None:
    cur = conn.cursor()
    cur.execute(sql_dict['insert']['suffix'], record.to_namedtuple())
    conn.commit()


@insert_record.register(Ranks)
def _(record: Ranks, conn: Connection) -> None:
    cur = conn.cursor()
    cur.executemany(sql_dict['insert']['rank'][0], record.to_namedtuple_collection())
    conn.commit()


@insert_record.register(Fields)
def _(record: Fields, conn: Connection) -> None:
    cur = conn.cursor()
    cur.executemany(sql_dict['insert']['field'], record.to_namedtuple_collection())
    conn.commit()


@insert_record.register(GenusTypes)
def _(record: GenusTypes, conn: Connection) -> None:
    cur = conn.cursor()
    cur.executemany(sql_dict['insert']['genus_type'], record.to_namedtuple_collection())
    conn.commit()


@insert_record.register(Suffixes)
def _(record: Suffixes, conn: Connection) -> None:
    cur = conn.cursor()
    cur.executemany(sql_dict['insert']['suffix'], record.to_namedtuple_collection())
    conn.commit()
