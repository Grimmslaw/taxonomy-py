from box import Box


_create_table_ranks = ''' CREATE TABLE IF NOT EXISTS TAX_RANKS (
                            ID INTEGER PRIMARY KEY,
                            NAME TEXT NOT NULL,
                            LABEL TEXT NOT NULL,
                            IS_MAIN INTEGER NOT NULL,
                            REL_INDEX INTEGER NOT NULL,
                            FIELD_ID INTEGER,
                            FOREIGN KEY (FIELD_ID)
                                REFERENCES FIELDS (ID)
                        ) '''

_create_table_fields = ''' CREATE TABLE IF NOT EXISTS FIELDS (
                            ID INTEGER PRIMARY KEY,
                            NAME TEXT NOT NULL
                        ) '''

_create_table_genus_types = ''' CREATE TABLE IF NOT EXISTS GENUS_TYPES (
                                    ID INTEGER PRIMARY KEY,
                                    NAME TEXT NOT NULL
                                ) '''

_create_table_suffixes = ''' CREATE TABLE IF NOT EXISTS SUFFIXES (
                                RANK_ID INTEGER NOT NULL,
                                GENUS_TYPE_ID INTEGER NOT NULL,
                                SUFFIX TEXT NOT NULL,
                                CONSTRAINT RANK_GENUS_RANK_FK
                                    FOREIGN KEY (RANK_ID)
                                        REFERENCES TAX_RANKS (ID),
                                CONSTRAINT RANK_GENUS_GENUS_FK
                                    FOREIGN KEY (GENUS_TYPE_ID)
                                        REFERENCES GENUS_TYPES (ID),
                                CONSTRAINT RANK_GENUS_PK
                                    PRIMARY KEY (RANK_ID, GENUS_TYPE_ID)
                            ) '''

_create_table_entity = ''' CREATE TABLE IF NOT EXISTS ENTITIES (
                            ID INTEGER PRIMARY KEY,
                            NAME TEXT UNIQUE NOT NULL,
                            CONS_STATUS_ID INTEGER NOT NULL,
                            POP_EST INTEGER
                            ) '''

_insert_rank_no_field = ''' INSERT INTO RANKS(NAME, LABEL, IS_MAIN, REL_INDEX)
                                VALUES(?, ?, ?, ?)
                                ON CONFLICT(NAME) DO UPDATE SET
                                    NAME=excluded.NAME,
                                    LABEL=excluded.LABEL,
                                    IS_MAIN=excluded.IS_MAIN,
                                    REL_INDEX=excluded.REL_INDEX '''

_insert_rank_with_field = ''' INSERT INTO RANKS(NAME, LABEL, IS_MAIN, REL_INDEX, FIELD_ID)
                                VALUES(?, ?, ?, ?, ? )
                                ON CONFLICT(NAME) DO UPDATE SET
                                    NAME=excluded.NAME,
                                    LABEL=excluded.LABEL,
                                    IS_MAIN=excluded.IS_MAIN,
                                    REL_INDEX=excluded.REL_INDEX,
                                    FIELD_ID=excluded.FIELD_ID;'''

_insert_field = ''' INSERT INTO FIELDS(NAME)
                        VALUES(?)
                        ON CONFLICT(NAME) DO UPDATE SET
                            NAME=excluded.NAME '''

_insert_genus_type = ''' INSERT INTO GENUS_TYPES(NAME)
                            VALUES(?)
                            ON CONFLICT(NAME) DO UPDATE SET
                                NAME=excluded.NAME '''

_insert_suffix = ''' INSERT INTO SUFFIXES(RANK_ID, GENUS_TYPE_ID, SUFFIX)
                        VALUES(?, ?, ?)
                        ON CONFLICT(RANK_ID, GENUS_TYPE_ID) DO UPDATE SET
                            RANK_ID=excluded.RANK_ID,
                            GENUS_TYPE_ID=excluded.GENUS_TYPE_ID,
                            SUFFIX=excluded.SUFFIX '''

_insert_entity_with_pop = ''' INSERT INTO ENTITIES(NAME, CONS_STATUS_ID, POP_EST)
                                VALUES (?, ?, ?)
                                ON CONFLICT(NAME) DO UPDATE SET
                                   NAME=excluded.NAME,
                                   CONS_STATUS_ID=excluded.CONS_STATUS_ID,
                                   POP_EST=excluded.POP_EST '''

_insert_entity_no_pop = ''' INSERT INTO ENTITIES(NAME, CONS_STATUS_ID)
                                VALUES(?, ?) 
                                ON CONFLICT(NAME) DO UPDATE SET
                                   NAME=excluded.NAME,
                                   CONS_STATUS_ID=excluded.CONS_STATUS_ID '''

_insert_classification = ''' INSERT INTO CLASSIFICATIONS(ENTITY_ID, RANK_ID, NAME) 
                                VALUES(?, ?, ?)
                                ON CONFLICT(ENTITY_ID, RANK_ID) DO UPDATE SET 
                                    ENTITY_ID=excluded.ENTITY_ID,
                                    RANK_ID=excluded.RANK_ID,
                                    NAME=excluded.NAME '''

# with this, you have to know if it's a disambiguation rank (e.g. DIVISION_B vs DIVISION_Z)
_select_rank_id_by_name = ''' SELECT ID FROM RANKS
                                WHERE NAME = ? '''

_select_rank_id_by_label = ''' SELECT ID FROM RANKS
                                WHERE LABEL = ? '''

_select_conservation_status_codes = ''' SELECT ID, CODE_RL FROM CONSERVATION_STATUSES '''

_select_entity_id_by_name = ''' SELECT ID FROM ENTITIES WHERE NAME = ? '''

sql = Box({
    'create': {
        'table': {
            'rank': _create_table_ranks,
            'field': _create_table_fields,
            'genus_type': _create_table_genus_types,
            'suffix': _create_table_suffixes,
            'entity': _create_table_entity
        }
    },
    'insert': {
        'rank': (_insert_rank_no_field, _insert_rank_with_field),
        'field': _insert_field,
        'genus_type': _insert_genus_type,
        'suffix': _insert_suffix,
        'entity': _insert_entity_with_pop,
        'weak_entity': _insert_entity_no_pop,
        'classification': _insert_classification
    },
    'select': {
        'rank_id_by_name': _select_rank_id_by_name,
        'rank_id_by_label': _select_rank_id_by_label,
        'all_cons_codes': _select_conservation_status_codes,
        'entity_id_by_name': _select_entity_id_by_name
    },
    'update': {},
    'drop': {}
})
