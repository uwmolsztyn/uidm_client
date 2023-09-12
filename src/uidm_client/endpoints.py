import os
import requests
from .datamodel import (EntityEndpoint, Identity, Unit,
                        identity_instance, unit_instance,)


API_ACCESS_TOKEN = os.getenv('UIDM_ACCESS_TOKEN', False)
API_BASE_URL = os.getenv('UIDM_API', False)
API_IDENTITIES_URL = f'{API_BASE_URL}/identities/'
API_UNITS_URL = f'{API_BASE_URL}/units/'

headers = {
    'Authorization': f'Bearer {API_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}


class ApiEndpoint:

    API_URL = None

    def get_by_guid(self, guid):
        response = requests.get(f'{self.API_URL}{guid}/', headers=headers)
        response.raise_for_status()
        return response.json()


class IdentitiesEndpoint(ApiEndpoint):
    
    API_URL = API_IDENTITIES_URL
    
    def get(self, *args, **kwargs) -> Identity:
        if len(args):
            guid, *_ = args
            if not guid:
                raise ValueError
            if isinstance(guid, EntityEndpoint):
                guid = guid.id
            return self.get_by_guid(guid=guid)
        elif len(kwargs):
            return self.get_by_field(**kwargs)
        raise ValueError
    
    def get_by_guid(self, guid) -> Identity:
        response = requests.get(f'{API_IDENTITIES_URL}{guid}/', headers=headers)
        response.raise_for_status()
        return identity_instance(response.json())
    
    def get_by_field(self, **kwargs) -> Identity:
        query = [f'{key}={value}' for key, value in kwargs.items()]
        query = "&".join(query)
        response = requests.get(f'{API_IDENTITIES_URL}?{query}', headers=headers)
        response.raise_for_status()
        result = response.json()
        count = result.get('count', 0)
        if not count:
            return None
        elif count > 1:
            raise ValueError
        results = result.get('results', None)
        item, *_ = results
        return self.get_by_guid(item.get('id'))


class GroupsEndpoint(ApiEndpoint):
    pass


class RolesEndpoint(ApiEndpoint):
    pass


class UnitsEndpoint(ApiEndpoint):

    API_URL = API_UNITS_URL

    def get(self, *args, **kwargs) -> Unit:
        if len(args):
            guid, *_ = args
            if not guid:
                raise ValueError
            if isinstance(guid, EntityEndpoint):
                guid = guid.id
            return self.get_by_guid(guid=guid)
        # elif len(kwargs):
        #     return self.get_by_field(**kwargs)
        raise ValueError

    def get_by_guid(self, guid)-> Unit:
        response = super().get_by_guid(guid=guid)
        return unit_instance(response)


class FacultiesEndpoint(UnitsEndpoint):
    pass
