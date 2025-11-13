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

import cfg
from ImageData import ImageData

class SearchMetadata:

    # 1. Constructor
    def __init__(self, image_data: ImageData):
        """
        Inicialitza la classe amb la referència al gestor de metadades.
        """
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

    # Mètodes Màgics Obligatoris
    def __len__(self) -> int:
        """Retorna el nombre total d'imatges sobre les quals es pot cercar."""
        # Utilitzem el mètode públic, ja que len() de ImageData és correcte
        return len(self._image_data)

    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"SearchMetadata (Pot cercar sobre {len(self._image_data)} imatges)"
    
    # --- Mètode Auxiliar de Cerca ---
    
    def _search_by_field(self, field: str, sub: str) -> list:
        """
        Mètode auxiliar genèric per cercar una subcadena en un camp específic.
        """
        results = []
        
        getter_func = self._getter_map.get(field)
        
        if not getter_func:
            return []

        # ** CORRECCIÓ 1: Utilitzem el mètode públic **
        all_uuids = self._image_data.get_all_uuids() 
        
        for uuid in all_uuids:
            value = getter_func(uuid)
            
            # CORRECCIÓ 2 (Mantenim la comprovació de tipus per evitar TypeError)
            if isinstance(value, str) and value.find(sub) != -1:
                results.append(uuid)
                
        return results

    # --- Func6: Mètodes de Cerca Específics ---

    def prompt(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Prompt."""
        return self._search_by_field("prompt", sub)

    def model(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Model."""
        return self._search_by_field("model", sub)

    def seed(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Seed."""
        return self._search_by_field("seed", sub)

    def cfg_scale(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp CFG_Scale."""
        return self._search_by_field("cfg_scale", sub)

    def steps(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Steps."""
        return self._search_by_field("steps", sub)

    def sampler(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Sampler."""
        return self._search_by_field("sampler", sub)

    def date(self, sub: str) -> list:
        """Retorna una llista d'UUID de les imatges que contenen 'sub' en el camp Created_Date."""
        return self._search_by_field("date", sub)

    # --- Func6: Operadors Lògics (Es mantenen igual) ---

    def and_operator(self, list1: list, list2: list) -> list:
        """
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)
        """
        set1 = set(list1)
        set2 = set(list2)
        
        intersection = set1.intersection(set2)
        
        return list(intersection)

    def or_operator(self, list1: list, list2: list) -> list:
        """
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats. (Unió de conjunts)
        """
        set1 = set(list1)
        set2 = set(list2)
        
        union = set1.union(set2)
        
        return list(union)
