#!/usr/bin/env python3

from argparse import Namespace

from args import parse_args
from data_access.sql_ops import AutoClosingConn, insert_record
from model.db_data import construct_record


def main(cli_args: Namespace):
    with AutoClosingConn() as conn:
        record = construct_record(**vars(cli_args))
        insert_record(record, conn)


if __name__ == '__main__':
    argv = parse_args()
    main(argv)
