# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.
Implementa Func6 (Cerca i Operadors Lògics).

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""

# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.
Implementa Func6 (Cerca i Operadors Lògics).
"""

# -*- coding: utf-8 -*-
from ImageData import ImageData

class SearchMetadata:
    def __init__(self, image_data: ImageData):
        self._image_data = image_data
        self._getter_map = {
            "prompt": self._image_data.get_prompt,
            "model": self._image_data.get_model,
            "seed": self._image_data.get_seed,
            "cfg_scale": self._image_data.get_cfg_scale,
            "steps": self._image_data.get_steps,
            "sampler": self._image_data.get_sampler,
            "date": self._image_data.get_created_date,
        }

    def __len__(self) -> int:
        return len(self._image_data.get_all_uuids())

    def _search_by_field(self, field: str, sub: str) -> list:
        results = []
        getter_func = self._getter_map.get(field)
        if not getter_func: return []

        for uuid in self._image_data.get_all_uuids():
            value = getter_func(uuid)
            # Només cerquem si el valor existeix i és un string
            if value and isinstance(value, str) and sub in value:
                results.append(uuid)
        return results

    def prompt(self, sub: str) -> list: 
        return self._search_by_field("prompt", sub)
    
    def model(self, sub: str) -> list: 
        return self._search_by_field("model", sub)
    
    def seed(self, sub: str) -> list: 
        return self._search_by_field("seed", sub)
    
    def cfg_scale(self, sub: str) -> list: 
        return self._search_by_field("cfg_scale", sub)
    
    def steps(self, sub: str) -> list: 
        return self._search_by_field("steps", sub)
    
    def sampler(self, sub: str) -> list: 
        return self._search_by_field("sampler", sub)
    
    def date(self, sub: str) -> list: 
        return self._search_by_field("date", sub)

    def and_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) & set(list2))

    def or_operator(self, list1: list, list2: list) -> list:
        return list(set(list1) | set(list2))
