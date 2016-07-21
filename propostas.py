#!/usr/bin/env python

# requirements:
#
# beautifulsoup4
# requests
# unidecode
# pandas ...
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from unidecode import unidecode


def ler_propostas():
    res = get('http://speakerfight.com/events/python-brasil12-apresentacoes/')
    soup = BeautifulSoup(res.content, 'html.parser')
    div_event_proposals = soup.find('div', id='event-proposals')
    propostas = div_event_proposals.find_all(attrs={'class': 'panel-body'})
    for p in propostas:
        titulo = p.h3.a.text.strip()
        autor = p.find('p', attrs={'class': 'proposal-metadata'}).a.text
        match = re.findall('(\[ *(.*?) *\])', titulo)
        if match:
            trecho, miolo = match[0]
            titulo = titulo.replace(trecho, '')
            categorias = re.split(' *, *', miolo)
            for cat in categorias:
                yield autor, titulo, cat
        else:
            yield autor, titulo, '???'

propostas = sorted(ler_propostas(), key=lambda x: unidecode(str(x)).lower())


df = pd.DataFrame(propostas, columns=['autor', 'titulo', 'categoria'])
df.set_index(['categoria', 'autor'])

df.groupby(['autor', 'titulo']).agg(lambda x: ', '.join(x))
df.groupby('categoria').count()
