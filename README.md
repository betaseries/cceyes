# CCEyes Library

## Introduction

CCEyes is a Python CLI and library for the [CCEyes](https://cceyes.eu) project that allows you to easily access the CCEyes API as a provider.

## Installation

```bash
pip install cceyes
```

## Usage

### CLI

```bash
root@cceyes:~$ cceyes key
Enter your API key:
API key saved! 
root@cceyes:~$ cceyes datasets | jq
{
  "key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "datasets": [
    {
      "provider": "BetaSeries",
      "type": "TV Series"
    }
  ]
}
root@cceyes:~$ cat ~/productions.json | cceyes upsert | jq
{
  "success": true
}
```

### Library

```python
import cceyes
from cceyes.models import Production, ProductionDataset, ProductionMeta

cceyes.config.set_config('api', 'key', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# your ETL logic goes here
# examples are located in examples/ folder
productions = [Production(
    title="The Mandalorian",
    content="The travails of a lone gunfighter in the outer reaches of the galaxy, far from the authority of the New Republic.",
    dataset=ProductionDataset(
        type="TV Series",
        provider="BetaSeries",
    ),
    meta=ProductionMeta(
        id=68726,
        title="The Mandalorian",
        image="https://api.betaseries.com/pictures/shows?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&id=68726",
    ),
)]

cceyes.providers.upsert(productions)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Resources

- [CCEyes Website](https://cceyes.eu)
- [CCEyes Platform](https://platform.cceyes.eu)
- [CCEyes Platform Specs](https://docs.cceyes.eu)
- [CCEyes API Documentation](https://api.cceyes.eu/docs)

## Funding

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or EACEA. Neither the European Union nor the granting authority can be held responsible for them.Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or EACEA. Neither the European Union nor the granting authority can be held responsible for them.