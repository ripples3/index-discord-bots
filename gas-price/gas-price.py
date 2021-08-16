"""
Run a Discord sidebar bot that shows gas price of the Ethereum blockchain
"""
# Example:
# python3 gas_run.py -s etherscan &

from typing import Tuple

def get_gas_from_gasnow(verbose: bool = False) -> Tuple[int]:
    """
    Fetch gas from Gasnow API
    """
    import requests
    import time
    r = requests.get('https://www.gasnow.org/api/v3/gas/price')
    if r.status_code == 200:
        if verbose:
            print('200 OK')
        data = r.json()['data']
        return int(data['slow']//1e9), int(data['standard']//1e9), int(data['fast']//1e9), int(data['rapid']//1e9)
    else:
        if verbose:
            print(r.status_code)
        time.sleep(10)

def main(source, verbose=False):
   ## import yaml
    import discord
    import asyncio
    import os

    # 1. Load config
   # filename = 'gas_config.yaml'
  #  with open(filename) as f:
  #      config = yaml.load(f, Loader=yaml.Loader)

    # 2. Connect w the bot
    client = discord.Client()

    async def send_update(slow, standard, fast, rapid):
       # nickname = f'Fast: {fast} gwei'
        status = f'🚀{rapid}  🚶{standard} 🐌{slow}'
      #  await client.get_guild(config['guildId']).me.edit(nick=nickname)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=status))

        for guild in client.guilds:
        #    guser = guild.get_member(bot.user.id);
            await guild.me.edit(nick=f'Fast: {fast} gwei');

        await asyncio.sleep(10) # in seconds

    @client.event
    async def on_ready():
        """
        When discord client is ready
        """
        while True:
            # 3. Fetch gas
            if source == 'gasnow':
                gweiList = get_gas_from_gasnow(verbose=verbose)
            else:
                raise NotImplemented('Unsupported source')
            # 4. Feed it to the bot
            await send_update(*gweiList)

    client.run(os.environ['BOT_TOKEN_GAS_PRICE'])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source',
                        choices=['gasnow', 'gasnow'],
                        default='gasnow',
                        help='select API')

    parser.add_argument('-v', '--verbose',
                        action='store_true', # equiv. default is False
                        help='toggle verbose')
    args = parser.parse_args()
    main(source=args.source,
         verbose=args.verbose)