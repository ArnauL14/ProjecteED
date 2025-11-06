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
from ImageData import ImageData # Necessari per accedir a totes les metadades

class SearchMetadata:

    # 1. Constructor
    def __init__(self, image_data: ImageData):
        """
        Inicialitza la classe amb la referència al gestor de metadades.
        """
        self._image_data = image_data
        
        # Mapeig de mètodes d'accés a metadades per a una cerca genèrica
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
        """Retorna el nombre total d'imatges sobre les quals es pot cercar (totes les registrades)."""
        return len(self._image_data)

    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"SearchMetadata (Pot cercar sobre {len(self._image_data)} imatges)"
    
    # --- Mètode Auxiliar de Cerca ---
    
    def _search_by_field(self, field: str, sub: str) -> list:
        """
        Mètode auxiliar genèric per cercar una subcadena en un camp específic.
        La cerca és case-sensitive i utilitza str.find().
        """
        results = []
        
        # Obtenir el mètode 'getter' per al camp sol·licitat
        getter_func = self._getter_map.get(field)
        
        if not getter_func:
            print(f"ERROR: Camp de cerca desconegut: {field}")
            return []

        # Iterar sobre tots els UUIDs que tenim registrats (O(N))
        # Utilitzem un mètode intern de ImageData per obtenir tots els UUIDs si cal
        
        # NOTA: Assumim que ImageData té un mètode per retornar tots els seus UUIDs
        # (Si no el tens, hauràs de crear un 'get_all_uuids()' a ImageData, 
        # o iterar sobre les claus del seu diccionari intern si és accessible)
        all_uuids = self._image_data.database.keys() # Utilitzem .keys() si database és accessible
        
        for uuid in all_uuids:
            # Obtenir el valor del camp utilitzant el getter
            value = getter_func(uuid)
            
            # La cerca es fa només si el valor existeix (no és None)
            if value is not None and value.find(sub) != -1:
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

    # --- Func6: Operadors Lògics ---

    def and_operator(self, list1: list, list2: list) -> list:
        """
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)
        """
        # Convertim a set per a fer la intersecció ràpidament (O(N) de mitjana)
        set1 = set(list1)
        set2 = set(list2)
        
        # Intersecció
        intersection = set1.intersection(set2)
        
        # Retornem com a llista (sense ordre garantit, que és acceptable)
        return list(intersection)

    def or_operator(self, list1: list, list2: list) -> list:
        """
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats. (Unió de conjunts)
        """
        # Convertim a set per a fer la unió ràpidament (O(N) de mitjana)
        set1 = set(list1)
        set2 = set(list2)
        
        # Unió
        union = set1.union(set2)
        
        # Retornem com a llista
        return list(union)
