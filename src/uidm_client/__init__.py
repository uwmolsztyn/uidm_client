from .endpoints import IdentitiesEndpoint, GroupsEndpoint, RolesEndpoint, UnitsEndpoint, FacultiesEndpoint

_endpoints = {}

identities = IdentitiesEndpoint(endpoints=_endpoints)
groups = GroupsEndpoint()
roles = RolesEndpoint()
units = UnitsEndpoint()
faculties = FacultiesEndpoint()

_endpoints['units'] = units
