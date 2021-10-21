# animality-py
A simple API wrapper that generates images & facts of any animal

# Installation
```bash
$ pip install animality-py
```

# Simple Usage
```py
import animality
from asyncio import get_event_loop

async def run():
    animal = await animality.get("dog")
    print(animal.name, animal.image, animal.fact)
    random = await animality.random()
    print(random.name, random.image, random.fact)

get_event_loop().run_until_complete(run())
```

# Using a session
```py
from animality import AnimalityClient
from asyncio import get_event_loop

async def run():
    animality = AnimalityClient()
    
    animal = await animality.get("dog")
    print(animal.name, animal.image, animal.fact)
    
    random = await animality.random()
    print(random.name, random.image, random.fact)

    await animality.close()

get_event_loop().run_until_complete(run())
```

# Using the CLI
Get an animal.
```bash
$ animality cat
```

Get a random animal.
```bash
$ animality random
```

Get multiple animals.
```bash
$ animality cat dog panda bunny
```
