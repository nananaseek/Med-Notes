import ast
import asyncio
import time
from typing import Tuple, Dict, Any

import requests
from bs4 import BeautifulSoup
from telegraph import Telegraph
from telegraph.api import TelegraphException
from telegraph.utils import html_to_content

from app.redis.drug_cache import drug_cache


class ParserService:
    def __init__(self):
        self.telegraph = Telegraph('64f96e893447974b529a263246db44cb8b5260363cd4dac9564c35515792')

    def create_telegraph_page(self, drug_info: dict) -> dict[Any, Any]:
        html_content = html_to_content(drug_info['content'])
        try:
            new_page = self.telegraph.create_page(title=drug_info['title'], content=html_content)
        except TelegraphException as e:
            sleep_time = f'{str(e).split('_')[-1]}'
            time.sleep(int(sleep_time) + 3)
            new_page = self.telegraph.create_page(title=drug_info['title'], content=html_content)

        return {new_page.title: new_page.url}

    @staticmethod
    def _return_content_from_page(url: str):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        drug_title = soup.find("h1", class_='cp-page-title')
        drug_content = soup.find("div", class_='cp-accordion-tab__content cp-reference-content')
        segment_content = drug_content.find_all('div')

        drug_content_dict = {
            'title': drug_title.text,
            'content': []
        }

        # del segment_content[0]
        for segment in segment_content:
            if 'id' in segment.attrs:
                if segment.attrs['id'].startswith('anchor-'):
                    drug_content_dict['content'].append(segment)

        return drug_content_dict

        # drug_composition = soup.find('div', id='anchor-composition')
        # drug_medicinal_form = soup.find('div', id='anchor-medicinalForm')
        # drug_group = soup.find('div', id='anchor-pharmacotherapeuticGroup')
        # pharma_properties = soup.find('div', id='anchor-pharmacologicalProperties')
        # drug_indications = soup.find('div', id='anchor-indications')
        # drug_application = soup.find('div', id='anchor-application')
        # drug_contraindication = soup.find('div', id='anchor-contraindication')
        # drug_contraindications = soup.find('div', id='anchor-contraindications')
        # drug_side_effects = soup.find('div', id='anchor-sideEffects')
        # drug_specific_instructions = soup.find('div', id='anchor-specificInstructions')
        # drug_interactions = soup.find('div', id='anchor-interactions')
        # drug_overdosage = soup.find('div', id='anchor-overdosage')
        # drug_storing_conditions = soup.find('div', id='anchor-storingConditions')
        #
        # id_list = [
        #     'anchor-composition',
        #     'anchor-medicinalForm',
        #     'anchor-pharmacotherapeuticGroup',
        #     'anchor-pharmacologicalProperties',
        #     'anchor-indications',
        #     'anchor-indication',
        #     'anchor-application',
        #     'anchor-contraindication',
        #     'anchor-contraindications',
        #     'anchor-sideEffects',
        #     'anchor-specificInstructions',
        #     'anchor-interactions',
        #     'anchor-overdosage',
        #     'anchor-storingConditions'
        # ]
        #
        # return {
        #     'title': drug_title.text,
        #     'content': [
        #         pharma_properties,
        #         drug_indications,
        #         drug_application,
        #         drug_contraindications,
        #         drug_side_effects,
        #         drug_specific_instructions,
        #         drug_interactions,
        #         drug_overdosage,
        #         drug_storing_conditions
        #     ]
        # }

    def get_drug_page(self, url: str) -> dict:
        drag_page = self._return_content_from_page(url)

        drag_page_content = {'title': drag_page['title']}
        page_content = []

        for content_in in drag_page['content']:
            page_content.append(
                {
                    'id': content_in.attrs['id'],
                    'title': content_in.h2.text,
                    'content': str(content_in.p)
                }
            )

        drag_page_content['content'] = page_content

        return drag_page_content

    @staticmethod
    def _drug_search(search_query: str, ):
        data = []
        search = f'https://compendium.com.ua/result/?term={search_query}'
        search_page = requests.get(search)
        search_soup = BeautifulSoup(search_page.text, "html.parser")
        search_data = search_soup.findAll('div', class_='cp-drug-item cp-card')

        for raw_data in search_data:
            drug_card = {}
            raw_script_with_data: str = raw_data.script.text
            data_dict = ast.literal_eval(raw_script_with_data.replace('true', 'True'))
            try:
                is_image = requests.get(data_dict[0]['image'])
            except requests.exceptions.MissingSchema:
                pass
            else:
                if is_image.status_code == 200:
                    drug_card['image'] = data_dict[0]['image']
                else:
                    if 'image' in drug_card:
                        drug_card.pop('image')

            drug_card['name'] = data_dict[0]['name']

            description = raw_data.find('a', class_='cp-drug-item__description')
            drug_card['description'] = description.text.lstrip()
            drug_card['prescriptionStatus'] = data_dict[0]['prescriptionStatus']
            drug_card['price'] = raw_data.b.text + '₴'
            drug_card['url'] = data_dict[1]['url']
            drug_card['search_query'] = search_query

            data.append(drug_card)

        return data

    async def get_search_drug_data(self, search_query):

        if await drug_cache.is_search_query_in_cache(search_query):
            return await drug_cache.get_all_search_query(search_query)

        search_data = self._drug_search(search_query)
        for data in search_data:
            # data.update(await self.get_link_telegraph_page(data['url']))
            is_save = await drug_cache.save_query_to_cache(**data)

        return search_data

    async def get_drug_page_data(self, url):
        _url: str = url.split(':')[1]
        page_id: str = url.split('/')[-2]

        data = await drug_cache.get_page_query(page_id)

        if data is None:
            data = await self.get_link_telegraph_page(url)
            data.update(page_id=page_id)
            await drug_cache.save_page_to_cache(**data)

        return data

    async def get_link_telegraph_page(self, url):
        telegraph_url = {}
        get_page_data = self.get_drug_page(url)

        for data in get_page_data['content']:
            segment_of_content = self.create_telegraph_page(data)
            telegraph_url.update(**segment_of_content)

        return telegraph_url


parser_service = ParserService()
a = parser_service._return_content_from_page('https://compendium.com.ua/dec/557682/178716/')
print(a)
