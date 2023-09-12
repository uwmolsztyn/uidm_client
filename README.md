# very simple uidm client

## Examples
### Identities

How to get identity object:

```python
from uidm_client import identities

# get by identity ID
identity = identities.get("0352a24c-afc1-4867-913e-8fd85ea7191d")
print(f'{instance.firstname} {instance.lastname}')

# get by upn
identity = identities.get(upn="identity_upn_value")
print(f'{instance.firstname} {instance.lastname}')

# get by email
identity = identities.get(email="identity_email@example.com")
print(f'{instance.firstname} {instance.lastname}')
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
