#!/usr/bin/env python3

import argparse

from sqlite3.dbapi2 import Connection

from data_access.sql_ops import AutoClosingConn
from model.constants import sql as sql_queries
from model.db_data import Entity, Classification


def parse_args():
    argparser = argparse.ArgumentParser(description='A tool for inserting taxonomy information on an entity to a db')
    argparser.add_argument(
        'name', type=str, metavar='NAME', help='The entity\'s common name (if any, otherwise its genus-species name)'
    )
    argparser.add_argument(
        '-p', '--pop', type=int, dest='pop_est', metavar='POPEST', help='The estimated population of this entity'
    )
    argparser.add_argument(
        '-c', '-conservation', type=str, dest='cons_cd', metavar='CONS_CD',
        help='This entity\'s conservation status, as a 2-character code'
    )
    argparser.add_argument(
        '-t', '--taxonomy', type=str.upper, nargs='+', dest='taxonomy', metavar='TAXONOMY',
        help='The entity\'s taxonomy, with each rank and that rank\'s value joined by an equals (=) sign'
    )
    return argparser.parse_args()


def get_cons_status_codes(conn: Connection) -> dict:
    status_codes = {}
    cur = conn.cursor()
    for row in cur.execute(sql_queries['select']['all_cons_codes']):
        status_codes[row[1]] = row[0]
    return status_codes


def get_entity_id(conn: Connection, name: str) -> int:
    cur = conn.cursor()
    cur.execute(sql_queries['select']['entity_id_by_name'], (name,))
    return cur.fetchone()


def get_rank_id(conn: Connection, rank: str):
    cur = conn.cursor()
    cur.execute(sql_queries['select']['rank_id_by_label'], (rank.lower(),))
    return cur.fetchone()


def main(args):
    with AutoClosingConn() as conn:
        cons_codes = get_cons_status_codes(conn)
        entity_cur = conn.cursor()
        if args.pop_est is not None:
            pop_est = args.pop_est
            entity_type = 'entity'
        else:
            pop_est = None
            entity_type = 'weak_entity'
        entity_to_insert = Entity.build_namedtuple(name=args.name,
                                                   cons_status_id=cons_codes[args.cons_cd],
                                                   pop_est=pop_est)
        entity_cur.execute(sql_queries['insert'][entity_type], entity_to_insert)

        entity_id = entity_cur.lastrowid

        pairs_list = []
        for _p in args.taxonomy:
            label, classification = _p.split('=')
            rank_id = get_rank_id(conn, label.lower())
            pairs_list.append(Classification.build_namedtuple(entity_id=entity_id, rank_id=rank_id[0], name=label))
        entity_cur.executemany(sql_queries['insert']['classification'], pairs_list)


if __name__ == '__main__':
    argv = parse_args()
    main(argv)
