from discord.ext import commands

import socket
import ast
import asyncio
import subprocess

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the or else
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class owner(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
    
    @commands.command(name="ip")
    @commands.is_owner()
    async def check_ip(self, ctx):
        command = "curl ifconfig.me"
        external = subprocess.run([*command.split(" ")], stdout=subprocess.PIPE, timeout=50)
        external = external.stdout.decode('utf-8')
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        await ctx.author.send(f"external IP:\n```{external} ```\nlocal IP:\n```{local_ip}```")

    
    @commands.command(name="bash")
    @commands.is_owner()
    async def run_bash(self, ctx, *, command):
        commandArray = command.split(" ")        
        await ctx.send(f"are you sure you want to run the command `{command}`?")
        try:
            response = await self.bot.wait_for(
                "message", check=lambda m: m.author == ctx.author, timeout=30
            )
        except asyncio.TimeoutError:
            return await ctx.send(f"**Timed out** cancelling")

        confirmations = ["yes", "ye", "y"]
        if response.content not in confirmations:
            return await ctx.send("oh ok")

        output = subprocess.run([*commandArray], stdout=subprocess.PIPE, timeout=50)
        output = output.stdout.decode('utf-8')
        
        
        if len(output) + len(command) < 1975:
            await ctx.send(f"`{command}` returned output:\n```{output} ```")
            return
        
        n = 1994
        split_strings = []
        
        for index in range(0, len(output), n):
            split_strings.append(output[index : index + n])


        for message in split_strings:
            await ctx.send(f"```{message}```")

        
async def setup(bot: commands.bot) -> None:
    await bot.add_cog(owner(bot))
