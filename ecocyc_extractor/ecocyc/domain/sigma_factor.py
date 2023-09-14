import re
from .base import Base
from ..utils import constants as EC
from ..utils import utils


class SigmaFactor(Base):
    tags_to_remove = re.compile(
        '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    tags_to_remove = re.compile('<.*?>|;|&')

    def __init__(self, **kwargs):
        super(SigmaFactor, self).__init__(**kwargs)
        self.synnyms = kwargs.get("synonyms", None)
        self.gene = kwargs.get("gene", None)
        self.gene_name = kwargs.pop('gene_name', None)
        self.abbreviated_name = kwargs.get("abbreviated_name", None)
        self.db_links = kwargs.get("dblinks", None)

    @property
    def gene_name(self):
        return self._gene_name

    @gene_name.setter
    def gene_name(self, gene_name):
        gene_name = self.pt_connection.get_name_by_id(self.gene)
        self._gene_name = gene_name

    @property
    def synnyms(self):
        return self._synnyms

    @synnyms.setter
    def synnyms(self, synonyms=None):
        synonyms = self.pt_connection.get_slot_values(
            self.id, EC.SYNONYMS_SLOT)
        clean_synonyms = []
        for synonym in synonyms:
            clean_synonyms.append(SigmaFactor.remove_tags(
                synonym, SigmaFactor.tags_to_remove))
        clean_synonyms = list(set(clean_synonyms))
        self._synonyms = clean_synonyms

    @property
    def abbreviated_name(self):
        return self._abbreviated_name

    @abbreviated_name.setter
    def abbreviated_name(self, abb_name):
        abb_name = self.pt_connection.get_slot_value(
            self.id, EC.ABBREV_NAME_SLOT)
        if abb_name is None:
            shortest_synonyms = []
            synonyms = self.synonyms
            for synonym in synonyms:
                if len(synonym) < 25:
                    if SigmaFactor.contains_number(synonym):
                        shortest_synonyms.append(synonym)
            if shortest_synonyms is not None and shortest_synonyms != []:
                abb_name = min(shortest_synonyms, key=len)
                for synonym in shortest_synonyms:
                    if synonym in abb_name:
                        abb_name = synonym
                        continue
            if abb_name is None and shortest_synonyms is not None and shortest_synonyms != []:
                abb_name = utils.get_similar_string(
                    self.name, shortest_synonyms)
            abb_name = abb_name
        detailed_name = utils.get_similar_string(self.gene_name, synonyms)
        if detailed_name and detailed_name != []:
            detailed_name = detailed_name[0]
        abb_name = abb_name.replace(' factor', '')
        abb_name = abb_name.replace(' ', '')
        self._abbreviated_name = abb_name

    @property
    def gene(self):
        return self._gene

    @gene.setter
    def gene(self, gene=None):
        if isinstance(gene, list):
            self._gene = gene[0]
        else:
            self._gene = gene

    @staticmethod
    def remove_tags(text, tags):
        text = re.sub(';', ' ', text)
        text = re.sub(tags, '', text)
        return text

    @staticmethod
    def contains_number(text):
        text = re.sub('[^\d+]', '', text)
        return text
