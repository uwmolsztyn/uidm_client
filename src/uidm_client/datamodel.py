from __future__ import annotations
from dataclasses import dataclass
from .const import EMPLOYEE_DOMAIN
import re


unit_pattern = r'\d{2}\.\d{3}\.\d{3}'


@dataclass
class EntityEndpoint:
    id: str
    url: str


@dataclass
class IdentityRole(EntityEndpoint):
    name: str
    type: str|None


@dataclass
class IdentityGroup(EntityEndpoint):
    idn: str
    name: str


@dataclass
class IdentityUnit(EntityEndpoint):
    idn: str
    name: str


@dataclass
class IdentitySupervisor(EntityEndpoint):
    pass


# new

@dataclass
class EntityDatamodel:
    id: str


@dataclass
class HyperlinkedStructureEntity(EntityDatamodel):
    id: str
    url: str
    idn: str
    name: str

# ###


@dataclass
class Identity(EntityDatamodel):
    id: str
    guid: str
    url: str
    active: bool
    firstname: str
    middlename: str|None
    lastname: str
    titles_before: str|None
    titles_after: str|None
    email: str|None
    phone: str|None
    mobile: str|None
    job_position: IdentityRole|None
    roles: list|None
    groups: list|None
    unit: IdentityUnit|None
    supervisor: IdentitySupervisor|None
    domain_meta: list|None

    _endpoints: dict|None

    def is_member(self, id: str) -> bool:
        return len(list(filter(lambda g: g.id, self.groups))) > 0
    
    @property
    def is_employee(self) -> bool:
        return self.is_member('pracownicy')
    
    def vertical_units(self):
        if self.unit and self._endpoints:
            unit = self._endpoints.get('units').get(self.unit)
            if unit and isinstance(unit.branch, list):
                return [*filter(lambda x: re.match(unit_pattern, x.idn), reversed(unit.branch)), unit]
        return []
    
    def vertical_units_names(self):
        units = [*map(lambda u: u.name, self.vertical_units())]
        if len(units):
            return ", ".join(units)
        return None
    
    def domain_login(self, domain:str=EMPLOYEE_DOMAIN):
        if not self.domain_meta:
            return None
        meta = list(filter(lambda x: x['domain_login'].endswith(domain), self.domain_meta))
        if not meta:
            return None
        return meta[0]['domain_login']


def identity_instance(data:dict, endpoints:dict|None = None) -> Identity:
    data = {key: value for key, value in data.items() if key in Identity.__annotations__}
    if data.get('job_position'):
        data['job_position'] = IdentityRole(**data["job_position"])
    if data.get('roles'):
        data['roles'] = [IdentityRole(**role_data) for role_data in data.get('roles')]
    if data.get('groups'):
        data['groups'] = [IdentityGroup(**group_data) for group_data in data.get('groups')]
    if data.get('supervisor'):
        data['supervisor'] = IdentitySupervisor(**data.get('supervisor'))
    if data.get('unit'):
        data['unit'] = IdentityUnit(**data.get('unit'))
    if endpoints:
        data['_endpoints'] = endpoints
    return Identity(**data)


@dataclass
class StructureMembers:
    count: int
    url: str


@dataclass
class StructureEntity(EntityDatamodel):
    id: str
    url: str


@dataclass
class Unit(StructureEntity):
    id: str
    url: str
    slug: str
    idn: str
    path: str
    name: str
    type: str|None
    principal: dict|None
    members: StructureMembers|None
    parent: dict|None
    branch: list|None
    units: list|None


def unit_instance(data:dict) -> Unit:
    data = {key: value for key, value in data.items() if key in Unit.__annotations__}

    if data.get('branch'):
        data['branch'] = list(map(lambda x: HyperlinkedStructureEntity(**x), data.get('branch')))
    elif not data.get('branch'):
        data['branch'] = None
    
    if data.get('units'):
        data['units'] = list(map(lambda x: HyperlinkedStructureEntity(**x), data.get('units')))
    elif not data.get('units'):
        data['units'] = None
    
    if data.get('members'):
        data['members'] = StructureMembers(**data.get('members'))
    return Unit(**data)


@dataclass
class Group(StructureEntity):
    id: str
    url: str
    slug: str
    idn: str
    path: str
    name: str
    type: str|None
    principal: dict|None
    members: StructureMembers|None
    parent: dict|None
    groups: list|None


def group_instance(data:dict) -> Group:
    data = {key: value for key, value in data.items() if key in Group.__annotations__}
    if not data.get('groups'):
        data['groups'] = None
    if data.get('members'):
        data['members'] = StructureMembers(**data.get('members'))
    return Group(**data)
