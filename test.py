# import sys
# import os
# sys.path.append(os.path.abspath('lib\\LibreOffice\\program'))
from functools import partial
import functools

from lib.file_ext._docx import DOCX

import asyncio
import aiohttp

from lib.utils import async_loop


# DOCX(None, r"C:\Users\power\Desktop\English Glossary.docx", 'en', 'ko')


from lib.papagopy.papagopy import Papagopy

p = Papagopy()


a = ['Compound sentences!']*700

async def run(text):
    return p.translate(text, 'ko', 'en')



async def rt():
    s = [asyncio.ensure_future(p.translate) for i in a]
    await asyncio.gather(*s)

k = list(async_loop())

print(k)