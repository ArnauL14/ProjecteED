# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mosteig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""

import cfg  # Per llegir metadades i obtenir el ROOT_DIR
import os   # Per construir el path complet de l'arxiu

class ImageData:

    def __init__(self):
        """
        Inicialitza la base de dades.
        self.database serà un diccionari on:
        Clau: uuid (str)
        Valor: diccionari amb les metadades (ex: {"file_path": ..., 
                                                "prompt": ..., 
                                                "seed": ...})
        """
        self.database = {}
        
        # Mapem les claus de les metadades del PNG (com a 'test-images.py')
        # a les claus internes (lowercase) que farem servir.
        self.key_map = {
            "Prompt": "prompt",
            "Seed": "seed",
            "CFG_Scale": "cfg_scale",
            "Steps": "steps",
            "Sampler": "sampler",
            "Model": "model",
            "Generated": "generated",
            "Created_Date": "created_date"
        }

    def __len__(self) -> int:
        """Retorna el nombre total d'imatges amb metadades registrades."""
        return len(self.database)

    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"ImageData (Total: {len(self.database)} imatges registrades)"

    def add_image(self, uuid: str, file: str) -> None:
        """
        Crea una entrada per a la imatge.
        Inicialment les metadades estan buides (valor "None").
        """
        if uuid not in self.database:
            self.database[uuid] = {}

        # Guardem el path canònic
        self.database[uuid]["file_path"] = file
        
        # Inicialitzem tots els camps de metadades a "None"
        for key in self.key_map.values():
            self.database[uuid][key] = "None"
            
        # Inicialitzem les dimensions
        self.database[uuid]["width"] = "None"
        self.database[uuid]["height"] = "None"


    def remove_image(self, uuid: str) -> None:
        """
        Elimina la imatge i totes les seves metadades.
        """
        if uuid in self.database:
            del self.database[uuid]

    def load_metadata(self, uuid: str) -> None:
        """
        Llegeix les metadades de l'arxiu PNG i les emmagatzema.
        """
        if uuid not in self.database:
            print(f"ERROR (ImageData): Intentant carregar metadades d'un UUID desconegut: {uuid}")
            return

        entry = self.database[uuid]
        canonical_path = entry["file_path"]
        
        # Necessitem el path absolut per poder obrir l'arxiu
        full_path = os.path.join(cfg.get_root(), canonical_path)

        # 1. Llegir metadades de text (Prompt, Seed, etc.)
        #    Utilitzem la funció proporcionada a cfg.py
        png_metadata = cfg.read_png_metadata(full_path)
        
        # Reinicialitzem per si l'arxiu s'ha modificat i ha perdut camps
        for key in self.key_map.values():
            entry[key] = "None"

        if png_metadata:
            # Omplim la nostra base de dades interna
            for png_key, db_key in self.key_map.items():
                if png_key in png_metadata:
                    entry[db_key] = png_metadata[png_key]

        # 2. Llegir dimensions (Width, Height)
        #    Utilitzem la funció de cfg.py per a les dimensions
        width, height = cfg.get_png_dimensions(full_path)

        entry["width"] = str(width) if width is not None else "None"
        entry["height"] = str(height) if height is not None else "None"
        
        # Actualitzem l'entrada (tot i que ja ho estem modificant per referència)
        self.database[uuid] = entry

    # --- Mètodes GET ---
    
    def _get_field(self, uuid: str, field: str):
            """ 
            Mètode privat d'ajuda per obtenir un camp. 
            Retorna el valor (string) si existeix, o l'objecte None si no existeix.
            """
            if uuid in self.database:
                # 1. Obtenim el valor: si 'field' no existeix, retorna el string "None" (valor d'inicialització)
                value = self.database[uuid].get(field, "None")
                
                # 2. Si el valor obtingut és el nostre marcador d'absència ("None"),
                #    retornem l'objecte None. Altrament, retornem el valor (string).
                return None if value == "None" else value
            
            # 3. Si el UUID no existeix, retornem l'objecte None
            return None

    def get_prompt(self, uuid: str) -> str:
        return self._get_field(uuid, "prompt")

    def get_model(self, uuid: str) -> str:
        return self._get_field(uuid, "model")

    def get_seed(self, uuid: str) -> str:
        return self._get_field(uuid, "seed")

    def get_cfg_scale(self, uuid: str) -> str:
        return self._get_field(uuid, "cfg_scale")

    def get_steps(self, uuid: str) -> str:
        return self._get_field(uuid, "steps")

    def get_sampler(self, uuid: str) -> str:
        return self._get_field(uuid, "sampler")

    def get_generated(self, uuid: str) -> str:
        return self._get_field(uuid, "generated")

    def get_created_date(self, uuid: str) -> str:
        return self._get_field(uuid, "created_date")

    def get_dimensions(self, uuid: str) -> tuple:
        """
        Retorna una tupla (width, height) amb les dimensions.
        Retorna (None, None) si no es troben.
        """
        if uuid not in self.database:
            return (None, None)
            
        entry = self.database[uuid]
        width_str = entry.get("width", "None")
        height_str = entry.get("height", "None")
        
        # Convertim de string a int (o None)
        width = int(width_str) if width_str != "None" else None
        height = int(height_str) if height_str != "None" else None
            
        return (width, height)
        
    def get_file_path(self, uuid: str) -> str:
        """
        Mètode extra (molt útil) per obtenir el path canònic
        a partir del UUID. El necessitarem per al ImageViewer.
        """
        return self._get_field(uuid, "file_path")
