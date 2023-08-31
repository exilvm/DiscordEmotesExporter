import os
import discord
from slugify import slugify
import asyncio

TOKEN = os.environ['TOKEN']

async def to_slug(name):
    return slugify(name, entities=False, decimal=False, hexadecimal=False, max_length=0, word_boundary=False, separator='_', save_order=False, stopwords=(), regex_pattern=None, lowercase=True, replacements=(), allow_unicode=False)


class ClientInstance(discord.Client):
    async def on_ready(self):
        skipped_lotties = 0
        print('Logged on as', self.user)
        tasks = []
        for guild in client.guilds:
            guild_dir = f'exports/{await to_slug(guild.name)}'
            emotes_dir = f'{guild_dir}/emotes/'
            stickers_dir = f'{guild_dir}/stickers/'
            os.makedirs(f'{guild_dir}', exist_ok=True)
            os.makedirs(emotes_dir, exist_ok=True)
            os.makedirs(stickers_dir, exist_ok=True)
            tasks.append(asyncio.create_task(self._download_emotes(guild, emotes_dir)))
            tasks.append(asyncio.create_task(self._download_stickers(guild, stickers_dir)))
        await asyncio.gather(*tasks)
        print(f'Skipped {skipped_lotties} unsupported stickers (lottie format).')
        await client.close()

    async def _download_emotes(self, guild, emotes_dir):
        for emote in guild.emojis:
            emote_ext = os.path.splitext(emote.url)[1]
            emote_file = f'{emotes_dir}{await to_slug(emote.name) + emote_ext}'
            with open(emote_file, 'wb') as file:
                await emote.save(file)
                print(f'Exported emote {emote.name} from {guild.name}')

    async def _download_stickers(self, guild, stickers_dir):
        for sticker in guild.stickers:
            if sticker.format.name == 'lottie':
                skipped_lotties = skipped_lotties + 1
                continue
            sticker_ext = os.path.splitext(sticker.url)[1]
            sticker_file = f'{stickers_dir}/{await to_slug(sticker.name) + sticker_ext}'
            with open(sticker_file, 'wb') as file:
                await sticker.save(file)
                print(f'Exported sticker {sticker.name} from {guild.name}')

client = ClientInstance()
client.run(TOKEN)
