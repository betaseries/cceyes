# CCEyes Library

## Introduction

CCEyes is a Python CLI and library for the [CCEyes](https://cceyes.eu) project that allows you to easily access the CCEyes API.

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
root@cceyes:~$ cceyes me | jq
{
  "key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "providers": [
    {
      "name": "BetaSeries",
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

cceyes.config.set_config('api', 'key', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

productions = []
# your ETL logic goes here
# examples are located in examples/ folder

cceyes.providers.upsert(productions)
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Resources

- [CCEyes Website](https://cceyes.eu)
- [CCEyes Platform](https://platform.cceyes.eu)
- [CCEyes Platform Specs](https://docs.cceyes.eu)
- [CCEyes API Documentation](https://api.cceyes.eu/docs)
