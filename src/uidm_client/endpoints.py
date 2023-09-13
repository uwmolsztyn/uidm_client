import os
import requests
from .datamodel import (EntityEndpoint, Identity, Unit,
                        identity_instance, unit_instance,)


API_ACCESS_TOKEN = os.getenv('UIDM_ACCESS_TOKEN', False)
API_BASE_URL = os.getenv('UIDM_API', False)
API_IDENTITIES_URL = f'{API_BASE_URL}/identities/'
API_UNITS_URL = f'{API_BASE_URL}/units/'
API_FACULTIES_URL = f'{API_BASE_URL}/faculties/'


headers = {
    'Authorization': f'Bearer {API_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}


def param_value(key, value):
    if isinstance(value, list):
        value = ",".join(value)
    return f'{key}={value}'


def dict_to_query_params(params: dict):
    return "&".join([f'{param_value(key, value)}' for key, value in params.items()])


def viewset_request(url):
    # print(f'fetching: {url}')
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    dataset = response.json()
    count = dataset.get('count', 0)
    next_url = dataset.get('next', False)
    results = dataset.get('results', [])
    return count, results, next_url,


class ApiEndpoint:

    API_URL = None

    def client_get_by_guid(self, guid):
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
        response = super().client_get_by_guid(guid=guid)
        return identity_instance(response)
    
    def get_by_field(self, **kwargs) -> Identity:
        query = dict_to_query_params(kwargs)
        if len(query):
            query = '?' + query
        url = f'{self.API_URL}{query}'
        count, results, *_ = viewset_request(url)
        if not count:
            return None
        elif count > 1:
            raise ValueError
        item, *_ = results
        return self.get_by_guid(item.get('id'))
    
    def all(self, limit: int=25):
        return self.filter(limit=limit)

    def filter(self, limit: int=25, **kwargs):
        query = dict_to_query_params({'limit': limit, **kwargs})
        if len(query):
            query = '?' + query
        next_url = f'{self.API_URL}{query}'
        while True:
            if not next_url:
                break
            count, results, next_url = viewset_request(next_url)
            if not count:
                return []
            if not len(results):
                break
            for data in results:
                yield identity_instance(data)

    def members(self, unit: Unit, limit: int=25, **kwargs):
        members = unit.members
        if not members:
            return []
        query = dict_to_query_params({'limit': limit, **kwargs})
        if len(query):
            query = '&' + query
        next_url = f'{members.url}{query}'
        while True:
            if not next_url:
                break
            count, results, next_url = viewset_request(next_url)
            if not count:
                return []
            if not len(results):
                break
            for data in results:
                yield identity_instance(data)


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
                raise None
            if isinstance(guid, EntityEndpoint):
                guid = guid.id
            return self.get_by_guid(guid=guid)
        elif len(kwargs):
            return self.get_by_field(**kwargs)
        raise ValueError

    def get_by_guid(self, guid)-> Unit:
        response = super().client_get_by_guid(guid=guid)
        return unit_instance(response)
    
    def get_by_field(self, **kwargs) -> Unit:
        query = dict_to_query_params(kwargs)
        if len(query):
            query = '?' + query
        url = f'{self.API_URL}{query}'
        count, results, *_ = viewset_request(url)
        if not count:
            return None
        elif count > 1:
            raise ValueError
        item, *_ = results
        return self.get_by_guid(item.get('id'))
    
    def all(self, limit=25):
        return self.filter(limit=limit)

    def filter(self, limit=25, **kwargs):
        query = dict_to_query_params({'limit': limit, **kwargs})
        if len(query):
            query = '?' + query
        next_url = f'{self.API_URL}{query}'
        while True:
            if not next_url:
                break
            count, results, next_url = viewset_request(next_url)
            if not count:
                return []
            if not len(results):
                break
            for data in results:
                yield unit_instance(data)


class FacultiesEndpoint(UnitsEndpoint):

    API_URL = API_FACULTIES_URL
