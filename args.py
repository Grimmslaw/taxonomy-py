import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='A script for inserting records into taxonomy.db')
    parser.add_argument(
        'type', metavar='TYPE', choices=['RANK', 'FIELD', 'GENUSTYPE', 'SUFFIX', 'ENTITY'], type=str.upper,
        help=('Determines the type of record being inserted;'
              + ' options are ["RANK", "FIELD", "GENUSTYPE", "SUFFIX", "ENTITY"]')
    )
    parser.add_argument(
        'value', metavar='VALUE', type=str.upper,
        help=('Sets the primary value of the record. '
              + '(This is "name" for FIELD, GENUSTYPE, and RANK and "suffix" for SUFFIX.)')
    )
    parser.add_argument(
        '-l', '--label', dest='label', type=str,
        help='Sets the label of the record (for RANK)', metavar='LABEL'
    )
    parser.add_argument(
        '-r', '--rankid', dest='rank_id', type=int,
        help='Sets the rank id of the record (for SUFFIX)', metavar='RANKID'
    )
    parser.add_argument(
        '-g', '--genusid', dest='genus_id', type=int,
        help='Sets the genus type id of the record (for SUFFIX)', metavar='GENUSTYPEID'
    )
    parser.add_argument(
        '-f', '--fieldid', dest='field_id', type=int,
        help='Sets the field id of the record (for RANK)', metavar='FIELDID'
    )
    parser.add_argument(
        '-m', '--ismain', dest='is_main', type=int, choices=[0, 1],
        help='Sets whether this record is one of the main division of life (for RANK)', metavar='ISMAIN'
    )
    parser.add_argument(
        '-i', '--index', dest='rel_index', type=int,
        help=('Sets what the relative index of this record is (for RANK).'
              + 'This allows testing for whether two RANKs are "synonymous"'), metavar='INDEX'
    )
    return parser.parse_args()
