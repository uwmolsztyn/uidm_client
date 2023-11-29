from .endpoints import IdentitiesEndpoint, GroupsEndpoint, RolesEndpoint, UnitsEndpoint, FacultiesEndpoint, DomainEndpoint

_endpoints = {}


def get_identities():
    return IdentitiesEndpoint(endpoints=_endpoints)


def get_groups():
    return GroupsEndpoint(endpoints=_endpoints)


def get_roles():
    return RolesEndpoint(endpoints=_endpoints)


def get_units():
    return UnitsEndpoint(endpoints=_endpoints)


def get_faculties():
    return FacultiesEndpoint(endpoints=_endpoints)


def get_domain():
    return DomainEndpoint(endpoints=_endpoints)


identities = get_identities()
groups = get_groups()
roles = get_roles()
units = get_units()
faculties = get_faculties()
domain = get_domain()

_endpoints['identities'] = identities
_endpoints['groups'] = groups
_endpoints['roles'] = roles
_endpoints['units'] = units
_endpoints['faculties'] = faculties
_endpoints['domain'] = domain
