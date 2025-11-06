# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""

import cfg  # Per fer servir cfg.get_uuid()

class ImageID:

    def __init__(self):
        """
        Inicialitza el gestor d'IDs.
        Fem servir dos diccionaris per a cerques ràpides en ambdues
        direccions (O(1) de mitjana):
        - path_to_uuid: Mapa de 'path_canonic' -> 'uuid'
        - uuid_to_path: Mapa de 'uuid' -> 'path_canonic'
        """
        self.path_to_uuid = {}
        self.uuid_to_path = {}

    def __len__(self) -> int:
        """Retorna el nombre total d'UUIDs únics actius."""
        return len(self.uuid_to_path) # Retorna el nombre d'entrades UUID -> Path

    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"ImageID (Total: {len(self.uuid_to_path)} UUIDs actius)"

    def generate_uuid(self, file: str) -> str:
        """
        Genera un UUID per a l'arxiu especificat.
        'file' HA DE SER el path canònic (obtingut de ImageFiles).
        
        Comprova col·lisions.
        Aquest mètode només ha de funcionar per a fitxers NOUS.
        Per a consultar existents, s'ha de fer servir get_uuid().
        """
        
        # 1. Comprovem si ja hem generat un UUID per a aquest arxiu
        #    *** INICI DE LA CORRECCIÓ ***
        #    Segons la guia (Func2), hi ha un mètode get_uuid
        #    per a CONSULTAR, i generate_uuid per a GENERAR.
        #    Aquest mètode no hauria de retornar un ID existent.
        #    Si el fitxer ja existeix, retornem None perquè
        #    l'operació correcta seria cridar a get_uuid().
        if file in self.path_to_uuid:
            print(f"ERROR: L'arxiu '{file}' ja té un UUID assignat.")
            print(f"  Feu servir get_uuid() per a consultar-lo.")
            return None # Fallida - el fitxer ja existeix
        #    *** FI DE LA CORRECCIÓ ***

        # 2. Si no existeix, el generem
        #    Fem servir cfg.get_uuid() i el convertim a string
        new_uuid = str(cfg.get_uuid(file))

        # 3. Comprovem col·lisions
        #    Mirem si aquest UUID ja està en ús per un ALTRE arxiu
        if new_uuid in self.uuid_to_path:
            # Cas extremadament improbable
            existing_file = self.uuid_to_path[new_uuid]
            print(f"ERROR: Col·lisió d'UUID detectada!")
            print(f"  L'arxiu '{file}' genera el UUID '{new_uuid}'.")
            print(f"  Aquest UUID ja està en ús per '{existing_file}'.")
            print(f"  L'arxiu '{file}' serà ignorat.")
            return None #

        # 4. Si no hi ha col·lisió, guardem la nova relació
        #    en ELS DOS diccionaris
        self.path_to_uuid[file] = new_uuid
        self.uuid_to_path[new_uuid] = file
        
        # print(f"ImageID: Nou UUID generat per {file} -> {new_uuid}")

        return new_uuid

    def get_uuid(self, file: str) -> str:
        """
        Retorna el UUID associat a l'arxiu (path canònic).
        Retorna None si no existeix.
        """
        # Fem servir .get() que retorna None si la clau no existeix
        return self.path_to_uuid.get(file, None)

    def remove_uuid(self, uuid: str) -> None:
        """
        Elimina el UUID del registre d'identificadors actius.
        Això elimina la relació en ambdues direccions.
        """
        
        # 1. Comprovem si el UUID existeix
        if uuid in self.uuid_to_path:
            
            # 2. Obtenim el path associat
            file_to_remove = self.uuid_to_path[uuid]
            
            # 3. Esborrem l'entrada dels dos diccionaris
            #    Comprovem si el fitxer encara hi és (podria haver
            #    estat eliminat per error en una altra part)
            if file_to_remove in self.path_to_uuid:
                del self.path_to_uuid[file_to_remove]
            
            del self.uuid_to_path[uuid]
            
            # print(f"ImageID: UUID {uuid} (arxiu: {file_to_remove}) eliminat.")
        
        # Si el UUID no existeix, no fem res (tal com demana el mètode)
