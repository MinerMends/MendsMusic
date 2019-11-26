from urllib.parse import quote

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cat"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def meow(self, ctx):
        """
        Random cat pic.

        API from random.cat, more coming soon!
        """
        async with self.bot.session.get("http://aws.random.cat/meow") as r:
            cat = (await r.json())["file"]
        embed = discord.Embed(title=":cat: ~meow~")
        embed.set_image(url=cat)
        return await ctx.channel.send(embed=embed)

    @commands.group(aliases=["dog"], invoke_without_command=True)
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def woof(self, ctx, *, breed=None):
        """
        Random dog pic.

        You may specify a dog breed, see `{prefix}woof breeds` to find all supported breeds.

        API from dog.ceo!
        """
        if breed is not None:
            *sub_breed, breed = breed.split()
            if sub_breed:
                url = f"https://dog.ceo/api/breed/{quote(breed, safe='')}/{quote(sub_breed[0], safe='')}/images/random"
            else:
                url = f"https://dog.ceo/api/breed/{quote(breed, safe='')}/images/random"
        else:
            url = "https://dog.ceo/api/breeds/image/random"

        async with self.bot.session.get(url) as r:
            dog = (await r.json())["message"]
            breed, *sub_breed = dog.split('/')[-2].split('-')
            if sub_breed:
                breed = sub_breed[0] + " " + breed

        embed = discord.Embed(title=":dog: ~woof~")
        embed.set_image(url=dog)
        embed.set_footer(text=breed)
        return await ctx.channel.send(embed=embed)

    @woof.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def breeds(self, ctx):
        """
        Fetch a list of dog breeds.
        """
        async with self.bot.session.get("https://dog.ceo/api/breeds/image/random") as r:
            dog = (await r.json())["message"]

        async with self.bot.session.get("https://dog.ceo/api/breeds/list/all") as r:
            dogs = (await r.json())["message"]
            breeds = []
            for breed, sub_breeds in dogs.items():
                breeds.append(breed)
                for sub_breed in sub_breeds:
                    breeds.append(sub_breed + " " + breed)

        embed = discord.Embed(title=":dog: ~woof~", description=", ".join(breeds))
        embed.set_image(url=dog)
        return await ctx.channel.send(embed=embed)

    @commands.command(aliases=["fox"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def floof(self, ctx):
        """
        Random fox pic.

        API from randomfox.ca!
        """
        async with self.bot.session.get("https://randomfox.ca/floof/") as r:
            fox = (await r.json())["image"]
        embed = discord.Embed(title=":fox: Here come's floofy")
        embed.set_image(url=fox)
        return await ctx.channel.send(embed=embed)

    @commands.command(aliases=["shiba"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def shibe(self, ctx):
        """
        Random Shiba Inu pic.

        API from shibe.online!
        """
        async with self.bot.session.get("http://shibe.online/api/shibes") as r:
            shiba = (await r.json())[0]
        embed = discord.Embed(title=":dog2: Peekaboo Shiba's here!")
        embed.set_image(url=shiba)
        return await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Animals(bot))