from .endpoints import IdentitiesEndpoint, GroupsEndpoint, RolesEndpoint, UnitsEndpoint, FacultiesEndpoint, DomainEndpoint

_endpoints = {}

identities = IdentitiesEndpoint(endpoints=_endpoints)
groups = GroupsEndpoint()
roles = RolesEndpoint()
units = UnitsEndpoint()
faculties = FacultiesEndpoint()
domain = DomainEndpoint()

_endpoints['units'] = units
_endpoints['domain'] = domain
