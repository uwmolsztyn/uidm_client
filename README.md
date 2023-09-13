# A Very Simple UIDM Client

## Installation
```bash
pip install git+https://github.com/uwmolsztyn/uidm_client.git@0.2
```

## Examples

To use the UIDM Client you have to provide two environment variables:

```bash
export UIDM_API=_uidm_url_
export UIDM_ACCESS_TOKEN=__access_token__
```

### Identities

How to get identity object:

```python
from uidm_client import identities

# get by identity ID
identity = identities.get("0352a24c-afc1-4867-913e-8fd85ea7191d")
print(f'{identity.firstname} {identity.lastname}')

# get by upn
identity = identities.get(upn="identity_upn_value")
print(f'{identity.firstname} {identity.lastname}')

# get by email
identity = identities.get(email="identity_email@example.com")
print(f'{identity.firstname} {identity.lastname}')
```

How to filter identities:

```python
from uidm_client import identities
for identity in identities.filter(firstname__startswith="Anna"):
    print(f'{identity.firstname} {identity.lastname}')
```

You can use multiple filters:

```python
from uidm_client import identities
for identity in identities.filter(firstname="Anna", lastname="Kowalska"):
    print(f'{identity.firstname} {identity.lastname}')

for identity in identities.filter(firstname__contains="Anna", lastname__startswith="Kowalska"):
    print(f'{identity.firstname} {identity.lastname}')
```

How to get identity unit:

```python
from uidm_client import identities, units
identity = identities.get("0352a24c-afc1-4867-913e-8fd85ea7191d")
unit = units.get(instance.unit)
print(f'{instance.firstname} {instance.lastname} - {unit.name}')
```

How to get identity supervisor:

```python
from uidm_client import identities
identity = identities.get("0352a24c-afc1-4867-913e-8fd85ea7191d")
supervisor = identities.get(instance.supervisor)
print(f'{instance.firstname} {instance.lastname} - supervisor: {supervisor.firstname} {supervisor.lastname}')
```
