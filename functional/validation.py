import copy


_attr_sets_dict = {
    'RANK': {'value', 'label', 'is_main', 'rel_index', 'field_id'},
    'WEAKRANK': {'value', 'label', 'is_main', 'rel_index'},
    'FIELD': {'value'},
    'GENUSTYPE': {'value'},
    'SUFFIX': {'value', 'rank_id', 'genus_type_id'},
    'ENTITY': {}
}


class ArgSet:

    def __init__(self, **kwargs):
        args_to_pass = copy.deepcopy(kwargs)
        args_to_pass.pop('type')
        self.type, self.attrs = _filter_argset(kwargs['type'], filter_nones=True, **args_to_pass)


def _delegate_rank_arg(record_type: str, **kwargs):
    if record_type.upper() != 'RANK' or 'field_id' in kwargs:
        return record_type.upper()
    else:
        return 'WEAKRANK'


def _filter_argset(record_type: str, filter_nones: bool = None, **kwargs):
    if filter_nones:
        kwargs = {k: v for (k, v) in kwargs.items() if k is not None and v is not None}

    filter_on = _attr_sets_dict[_delegate_rank_arg(record_type, **kwargs)]
    filtered_keys = set(kwargs) & filter_on
    type_to_pass = record_type if record_type != 'WEAKRANK' else 'RANK'
    new_dict = {
        'value': kwargs['value']
    }

    for _key in filtered_keys:
        new_dict[_key] = kwargs[_key]

    return type_to_pass, new_dict


def filter_args(filter_nones: bool = None, **kwargs):
    if filter_nones:
        kwargs = {k: v for (k, v) in kwargs.items() if k is not None and v is not None}

    filter_on = _attr_sets_dict[kwargs['type']]
    filtered_keys = set(kwargs) & filter_on
    new_dict = {
        'type': kwargs['type'],
        'value': kwargs['value']
    }
    for _key in filtered_keys:
        new_dict[_key] = kwargs[_key]
    return new_dict


def validate_args(**kwargs):
    # 'type' arg exists
    assert 'type' in kwargs, f'No "type" in arguments={kwargs}'

    args = filter_args(filter_nones=True, **kwargs)
    # required args for appropriate 'type' are present
    assert set(args.keys()) >= _attr_sets_dict[args['type']], \
        f'Expected args={_attr_sets_dict[args["type"]]}, Received args={set(args.keys())}'
    # there are no values that are None
    assert not [x for x in args.values() if x is None]
