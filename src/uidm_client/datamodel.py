from dataclasses import dataclass


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


@dataclass
class IdentityUnit(EntityEndpoint):
    idn: str


@dataclass
class IdentitySupervisor(EntityEndpoint):
    pass


@dataclass
class EntityDatamodel:
    id: str


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

    def is_member(self, id: str) -> bool:
        return len(list(filter(lambda g: g.id, self.groups))) > 0
    
    @property
    def is_employee(self) -> bool:
        return self.is_member('pracownicy')



def identity_instance(data:dict) -> Identity:
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
    return Identity(**data)


@dataclass
class Unit(EntityDatamodel):
    id: str
    url: str
    slug: str
    idn: str
    path: str
    name: str
    type: str|None
    principal: dict|None
    members: dict|None
    parent: dict|None
    branch: list|None
    units: list|None


def unit_instance(data:dict) -> Unit:
    data = {key: value for key, value in data.items() if key in Unit.__annotations__}
    if not data.get('branch'):
        data['branch'] = None
    if not data.get('units'):
        data['units'] = None
    return Unit(**data)
