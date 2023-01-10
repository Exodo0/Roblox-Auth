import aiohttp, asyncio, json, nest_asyncio

nest_asyncio.apply()

async def c(i: int):
    async with aiohttp.ClientSession() as session:
        async with session.request("GET", f"https://users.roblox.com/v1/users/{i}") as res:
            return await res.content.read(), res.status

class user:
    def __init__(self, userId: int):
        self.i = userId
        
    def desc(self):
        """
        (method) desc
        -------------
        Check's the current description of the given userId, returns the current description as a string.
        """
        res = asyncio.get_event_loop().run_until_complete(c(self.i))
        try:
            return json.loads(res[0].decode("utf-8"))["description"]
        except KeyError:
            raise KeyError("Could not grab description.")
        
    def exists(self):
        """
        (method) exists
        ---------------
        Returns a boolean representing whether or not an account exists
        """
        res = asyncio.get_event_loop().run_until_complete(c(self.i))
        return True if res[1] == 200 else False

    def compare(self, key: str):
        """
        (method) compare
        ----------------
        Compares two strings and returns a boolean.

        ---

        Parameters
        ```
        i : int
            The user Id to pull the description from.
        key : str
            The key to compare to the current description.
        ```
        """
        return True if self.desc() == key else False

    def username(self):
        """
        (method) username
        -----------------
        Gets the username.
        """
        res = asyncio.get_event_loop().run_until_complete(c(self.i))
        return json.loads(res[0].decode("utf-8"))["name"]