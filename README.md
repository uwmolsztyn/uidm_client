# A Very Simple UIDM Client

## Installation
```bash
pip install git+https://github.com/uwmolsztyn/uidm_client.git@0.3
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

for identity in identities.filter(email__contains="anna", limit=15):
    print(f'{identity.firstname} {identity.lastname} ({identity.email})')
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


### Units

How to get unit object:

```python
from uidm_client import units

# get by unit ID
unit = units.get("00-000-000")
print(f'{unit.name}')

# get by unit IDN
unit = units.get(idn="00.000.000")
print(f'{unit.name}')

# get by unit path
unit = units.get(path="/path/to/unit")
print(f'{unit.name}')
```

How to filter units:

You can filter by fields:
* id (exact, in)
* idn (exact, notequals, contains, notcontains, startswith, endswith, in)
* path (exact, notequals, contains, notcontains', startswith, notstartswith, endswith, in)
* name (exact, notequals, contains, notcontains', startswith, endswith)
* type (exact, notequals, contains, notcontains', startswith, endswith, in)
* parent (exact)
* principal (exact, in)

```python
from uidm_client import units
for unit in units.filter(name__contains="Wydział", limit=20):
    print(f'{unit.name}')

for unit in units.filter(name__startswith="Wydział"):
    print(f'{unit.name}')

for unit in units.filter(idn__in=['idn1', 'idn2', 'idn3', ...]):
    print(f'{unit.name}')
```

How to ordering units:

You can order by fields: name, idn, path

```python
from uidm_client import units

# ascending
for unit in units.filter(name__contains="Wydział", ordering="name"):
    print(f'{unit.name}')

# descending
for unit in units.filter(name__startswith="Wydział", ordering="-name"):
    print(f'{unit.name}')
```


### Faculties

Faculties endpoint is a collection of Units and it has the same methods as units endpoint.

```python
from uidm_client import faculties
for unit in faculties.all():
    print(f'{unit.name}')
```
