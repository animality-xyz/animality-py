from random import choice
from aiohttp import ClientSession
from io import TextIOWrapper, BytesIO
from re import compile

version = '0.1.4'
animals = [
    "cat", "dog", "bird", "panda",
    "redpanda", "koala", "fox", "whale",
    "kangaroo", "bunny", "lion", "bear",
    "frog", "duck", "penguin"
]

get_animal_name = compile('/img/([a-z]+)/').findall
get_file_name = compile('/img/([a-z]+)/([0-9]+.[a-z]+)').findall
get_file_extension = compile('[0-9]+.([a-z]+)').findall

class AnimalityResponse:
    __slots__ = ('fact', 'image', '_image_bytes', '_request_image')

    def __init__(self, fact: str, image: str, request):
        self.fact = fact
        self.image = image
        self._image_bytes = None
        self._request_image = lambda: None if self._image_bytes else request(get_file_name(self.image)[0])
    
    def __repr__(self) -> str:
        return f"<Animal[{self.name.upper()}] fact='{self.fact}' image='{self.image}'>"

    @property
    def name(self) -> str:
        """ Returns the animal name. """
        return get_animal_name(self.image)[0]

    async def get_image(self) -> bytes:
        """ Downloads the image from the API. """
        try:
            response = await self._request_image()
            self._image_bytes = await response.read()
            return self._image_bytes
        except AttributeError:
            return self._image_bytes
        except:
            raise Exception("Client already closed.")

    async def save_image(self, data: "io.TextIOWrapper | io.BytesIO | str") -> None:
        """ Writes the animal image to a file. """
        if isinstance(data, TextIOWrapper):
            if data.mode != 'wb':
                raise TypeError(f"Invalid mode. Try 'open(\"{data.name}\", \"wb\")'.")
            
            file_extension = get_file_extension(self.image)[0]
            if data.name[-len(file_extension):] != file_extension:
                raise IOError(f"Invalid file extension. It must be .{file_extension}")

            return data.write(await self.get_image()) and None
        elif isinstance(data, BytesIO):
            return data.write(await self.get_image()) and None
        elif isinstance(data, str):
            file_extension = get_file_extension(self.image)[0]
            if data[-len(file_extension):] != file_extension:
                data += f".{file_extension}"

            with open(data, "wb") as f:
                f.write(await self.get_image())
                return f.close()

        raise TypeError(f"Expected io.TextIOWrapper, io.BytesIO, or str. got {data.__class__.__name__}")

class AnimalityClient:
    __slots__ = ('_request', '_close')

    def __init__(self, session: "ClientSession" = None):
        if session and not (isinstance(session, ClientSession) and not session.closed):
            raise TypeError("Invalid client session. A session must be an instance of aiohttp.ClientSession and it must not be closed.")
        else:
            session = ClientSession()

        self._request = lambda path: session.get(f'https://{"" if path[5:] == "/img/" else "api."}animality.xyz{path}')
        self._close = lambda: None if session.closed else session.close

    @property
    def closed(self) -> bool:
        """ Returns true if the client is closed. """
        return self._close is None

    def __repr__(self) -> str:
        return f"<AnimalityClient closed={self.closed}>"

    async def get(self, animal: str) -> "AnimalityResponse":
        """ Fetches random image and fact for a specific animal. """
        animal = animal.strip(' ').lower() if isinstance(animal, str) else ''
        if animal not in animals:
            raise FileNotFoundError(f"The animal: '{animal}' is not supported yet.")
        
        try:
            fact = await self._request(f'/fact/{animal}')
            fact = await fact.json()
            image = await self._request(f'/img/{animal}')
            image = await image.json()

            return AnimalityResponse(fact['fact'], image['link'], self._request)
        except:
            raise Exception("An error occurred while requesting to the API. Please try again later.")
    
    async def random(self) -> "AnimalityResponse":
        """ Does the same as get() function except it uses a random animal. """
        return await self.get(choice(animals))

    async def test(self) -> bool:
        """ Tests if the API is working or not. Returns a boolean regardless of errors. """
        try:
            response = await self._request('/')
            response = await response.json()
            return response['success'] == 'API is ACTIVE'
        except:
            return False

    async def close(self) -> None:
        """ Closes the client. """
        try:
            await self._close()()
        except:
            return

async def get(animal: str, *, session: "aiohttp.ClientSession | AnimalityClient" = None) -> "ClientResponse":
    """ Fetches random image and fact for a specific animal. """
    client = AnimalityClient(session if session and not isinstance(session, AnimalityClient) else None)
    ret, error = None, None
    try:
        ret = await client.get(animal)
    except Exception as e:
        error = e
    await client.close()
    if error:
        raise error
    return ret

async def random(*, session: "aiohttp.ClientSession | AnimalityClient" = None) -> "ClientResponse":
    """ Fetches random image and fact for a random animal. """
    client = AnimalityClient(session if session and not isinstance(session, AnimalityClient) else None)
    ret, error = None, None
    try:
        ret = await client.random()
    except Exception as e:
        error = e
    await client.close()
    if error:
        raise error
    return ret
