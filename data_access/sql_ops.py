from typing import List, Tuple

import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Connection

from functional.dispatch import insert_record
from model.db_data import Rank, Field, GenusType, Suffix, Record

DB_TABLE_PATH = r'data_access/taxonomy.db'


def create_connection(db_file: str) -> Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn: Connection, sql: str) -> None:
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
    except Error as e:
        print(e)


def _extract_all_of_type(extract_from: list or tuple, extraction_type: type) -> Tuple[list, list]:
    extracted = [x for x in extract_from if isinstance(x, extraction_type)]
    diff = list(set(extract_from) - set(extracted))
    return extracted, diff


def split_list_by_record_type(records: List[Record] or Tuple[Record]) -> Tuple[list, list, list, list]:
    ranks, records = _extract_all_of_type(records, Rank)
    fields, records = _extract_all_of_type(records, Field)
    genus_types, records = _extract_all_of_type(records, GenusType)
    suffixes, _ = _extract_all_of_type(records, Suffix)
    return ranks, fields, genus_types, suffixes


def insert(record, conn: Connection) -> None:
    insert_record(record, conn)


class AutoClosingConn:

    def __enter__(self, db_name: str = DB_TABLE_PATH):
        self.conn = create_connection(db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
