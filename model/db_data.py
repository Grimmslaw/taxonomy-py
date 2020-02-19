import copy
from collections import namedtuple
from abc import ABC, abstractmethod
from typing import NamedTuple, Union, List, Iterable

from functional.validation import ArgSet

WeakRankNT = namedtuple('WeakRank', ['name', 'label', 'is_main', 'rel_index'])
RankNT = namedtuple('Rank', ['name', 'label', 'is_main', 'rel_index', 'field_id'])
FieldNT = namedtuple('Field', ['name'])
GenusTypeNT = namedtuple('GenusType', ['name'])
SuffixNT = namedtuple('Suffix', ['rank_id', 'genus_type_id', 'suffix'])
WeakEntityNT = namedtuple('WeakEntity', ['name', 'cons_status_id'])
EntityNT = namedtuple('Entity', ['name', 'cons_status_id', 'pop_est'])
ClassificationNT = namedtuple('Classification', ['entity_id', 'rank_id', 'name'])

RecordNT = Union[RankNT, FieldNT, GenusTypeNT, SuffixNT, EntityNT]


def _validate_kwargs(required: set, **kwargs) -> None:
    assert required <= set(kwargs.keys())


def _instance_to_comma_sep_pairs(instance: 'Record') -> str:
    instance_attrs_dict = vars(instance)
    instance_attrs_list = []
    for attr in instance_attrs_dict.keys():
        instance_attrs_list.append(f'attr={instance_attrs_dict[attr]}')
    return ', '.join(instance_attrs_list)


def _iterable_to_comma_sep_strs(some_iterable: Iterable['Record']):
    return ', '.join([str(x) for x in some_iterable])


class Record(ABC):

    @classmethod
    @abstractmethod
    def from_namedtuple(cls, nt: RecordNT):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def build_namedtuple(cls, **kwargs) -> RecordNT:
        raise NotImplementedError

    @abstractmethod
    def to_namedtuple(self) -> NamedTuple:
        raise NotImplementedError


class Records(ABC):

    @abstractmethod
    def to_namedtuple_collection(self) -> List[RecordNT]:
        raise NotImplementedError


class Rank(Record):

    valid_weak = {'value', 'label', 'is_main', 'rel_index', 'field_id'}
    valid_strong = valid_weak | {'field_id'}

    def __init__(self, value: str, label: str, is_main: int, rel_index: int, field_id: int = None):
        self.name = value
        self.label = label
        self.is_main = is_main
        self.rel_index = rel_index
        self.field_id = field_id

    def __str__(self):
        return f'Rank={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: RankNT) -> 'Rank':
        return Rank(nt.name, nt.label, nt.is_main, nt.rel_index, nt.field_id)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> Union[RankNT, WeakRankNT]:
        if 'field_id' in kwargs:
            _validate_kwargs(required=Rank.valid_strong, **kwargs)
            return RankNT(name=kwargs['name'], label=kwargs['label'], is_main=kwargs['is_main'],
                          rel_index=kwargs['rel_index'], field_id=kwargs['field_id'])
        else:
            _validate_kwargs(required=Rank.valid_weak, **kwargs)
            return WeakRankNT(name=kwargs['name'], label=kwargs['label'], is_main=kwargs['is_main'],
                              rel_index=kwargs['rel_index'])

    def to_namedtuple(self) -> RankNT or WeakRankNT:
        if self.field_id:
            return RankNT(name=self.name, label=self.label, is_main=self.is_main,
                          rel_index=self.rel_index, field_id=self.field_id)
        else:
            return WeakRankNT(name=self.name, label=self.label, is_main=self.is_main, rel_index=self.rel_index)


class Ranks(Records):

    def __init__(self, *ranks: Rank):
        self.ranks = ranks

    def __str__(self):
        return f'Ranks=[{_iterable_to_comma_sep_strs(self.ranks)}]'

    def to_namedtuple_collection(self) -> List[RankNT]:
        list_to_return = []
        for rank in self.ranks:
            list_to_return.append(rank.to_namedtuple())
        return list_to_return


class Field(Record):

    valid = {'name'}

    def __init__(self, value: str):
        self.name = value

    def __str__(self):
        return f'Field={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: FieldNT) -> 'Field':
        return Field(nt.name)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> FieldNT:
        _validate_kwargs(required=Field.valid)
        return FieldNT(name=kwargs['name'])

    def to_namedtuple(self) -> FieldNT:
        return FieldNT(name=self.name)


class Fields(Records):

    def __init__(self, *fields: Field):
        self.fields = fields

    def __str__(self):
        return f'Fields=[{_iterable_to_comma_sep_strs(self.fields)}]'

    def to_namedtuple_collection(self) -> List[FieldNT]:
        list_to_return = []
        for field in self.fields:
            list_to_return.append(field.to_namedtuple())
        return list_to_return


class GenusType(Record):

    def __init__(self, value: str):
        self.name = value

    def __str__(self):
        return f'GenusType={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: GenusTypeNT) -> 'GenusType':
        return GenusType(nt.name)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> GenusTypeNT:
        return GenusTypeNT(name=kwargs['name'])

    def to_namedtuple(self) -> GenusTypeNT:
        return GenusTypeNT(name=self.name)


class GenusTypes(Records):

    def __init__(self, *genus_types: GenusType):
        self.genus_types = genus_types

    def __str__(self):
        return f'GenusTypes=[{_iterable_to_comma_sep_strs(self.genus_types)}]'

    def to_namedtuple_collection(self) -> List[GenusTypeNT]:
        list_to_return = []
        for genus_type in self.genus_types:
            list_to_return.append(genus_type.to_namedtuple())
        return list_to_return


class Suffix(Record):

    def __init__(self, rank_id: int, genus_type_id: int, value: str):
        self.rank_id = rank_id
        self.genus_type_id = genus_type_id
        self.suffix = value

    def __str__(self):
        return f'Suffix={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: SuffixNT) -> 'Suffix':
        return Suffix(nt.rank_id, nt.genus_type_id, nt.suffix)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> SuffixNT:
        return SuffixNT(rank_id=kwargs['rank_id'], genus_type_id=kwargs['genus_type_id'], suffix=kwargs['suffix'])

    def to_namedtuple(self) -> SuffixNT:
        return SuffixNT(rank_id=self.rank_id, genus_type_id=self.genus_type_id, suffix=self.suffix)


class Suffixes(Records):

    def __init__(self, *suffixes: Suffix):
        self.suffixes = suffixes

    def __str__(self):
        return f'Suffixes=[{_iterable_to_comma_sep_strs(self.suffixes)}]'

    def to_namedtuple_collection(self) -> List[SuffixNT]:
        list_to_return = []
        for suffix in self.suffixes:
            list_to_return.append(suffix.to_namedtuple())
        return list_to_return


class Entity(Record):

    def __init__(self, name: str, cons_status_id: int, pop_est: int = None):
        self.name = name
        self.cons_status_id = cons_status_id
        self.pop_est = pop_est

    def __str__(self):
        return f'Entity={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: EntityNT) -> 'Entity':
        return Entity(nt.name, nt.cons_status_id, nt.pop_est)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> Union[EntityNT, WeakEntityNT]:
        if 'pop_est' in kwargs:
            return EntityNT(name=kwargs['name'], cons_status_id=kwargs['cons_status_id'],
                            pop_est=kwargs['pop_est'])
        else:
            return WeakEntityNT(name=kwargs['name'],
                                cons_status_id=kwargs['cons_status_id'])

    def to_namedtuple(self) -> EntityNT or WeakEntityNT:
        if self.pop_est:
            return EntityNT(name=self.name, cons_status_id=self.cons_status_id,
                            pop_est=self.pop_est)
        else:
            return WeakEntityNT(name=self.name, cons_status_id=self.cons_status_id)


class Entities(Records):

    def __init__(self, *entities: Entity):
        self.entities = entities

    def __str__(self):
        return f'Entities=[{_iterable_to_comma_sep_strs(self.entities)}]'

    def to_namedtuple_collection(self) -> List[EntityNT]:
        list_to_return = []
        for entity in self.entities:
            list_to_return.append(entity.to_namedtuple())
        return list_to_return


class Classification(Record):

    def __init__(self, entity_id: int, rank_id: int, name: str):
        self.entity_id = entity_id
        self.rank_id = rank_id
        self.name = name

    def __str__(self):
        return f'Classification={{{_instance_to_comma_sep_pairs(self)}}}'

    @classmethod
    def from_namedtuple(cls, nt: ClassificationNT) -> 'Classification':
        return Classification(nt.entity_id, nt.rank_id, nt.name)

    @classmethod
    def build_namedtuple(cls, **kwargs) -> RecordNT:
        return ClassificationNT(entity_id=kwargs['entity_id'], rank_id=kwargs['rank_id'], name=kwargs['name'])

    def to_namedtuple(self) -> NamedTuple:
        return ClassificationNT(entity_id=self.entity_id, rank_id=self.rank_id, name=self.name)


class Classifications(Records):

    def __init__(self, *classifications: Classification):
        self.classifications = classifications

    def __str__(self):
        return f'Classification=[{_iterable_to_comma_sep_strs(self.classifications)}]'

    def to_namedtuple_collection(self) -> List[ClassificationNT]:
        list_to_return = []
        for classification in self.classifications:
            list_to_return.append(classification.to_namedtuple())
        return list_to_return


RecordType = Union[Rank, Field, GenusType, Suffix, Entity]

_type_dict = {
    'RANK': Rank,
    'FIELD': Field,
    'GENUSTYPE': GenusType,
    'SUFFIX': Suffix,
    'ENTITY': Entity,
    'CLASSIFICATION': Classification
}


# kwargs are assumed to have already been validated
def construct_record(**kwargs) -> RecordType:
    new_args = copy.deepcopy(kwargs)
    argset = ArgSet(**new_args)
    return _type_dict[argset.type](**argset.attrs)
