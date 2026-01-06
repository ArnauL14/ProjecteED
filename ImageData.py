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
import cfg
import os

class ImageData:
    def __init__(self):
        self.database = {}
        self.key_map = {
            "Prompt": "prompt", "Seed": "seed", "CFG_Scale": "cfg_scale",
            "Steps": "steps", "Sampler": "sampler", "Model": "model",
            "Generated": "generated", "Created_Date": "created_date"
        }

    def add_image(self, uuid: str, file: str) -> None:
        if uuid not in self.database:
            self.database[uuid] = {"file_path": file}
            for key in self.key_map.values():
                self.database[uuid][key] = None

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self.database: return
        entry = self.database[uuid]
        
        # El file_path ara és només el nom (ex: "imatge.png")
        # El busquem directament dins del root definit per l'autograder
        full_path = os.path.join(cfg.get_root(), entry["file_path"])

        try:
            png_metadata = cfg.read_png_metadata(full_path)
            if png_metadata:
                for png_key, db_key in self.key_map.items():
                    val = png_metadata.get(png_key)
                    entry[db_key] = str(val) if val is not None else None
            
            w, h = cfg.get_png_dimensions(full_path)
            entry["width"], entry["height"] = w, h
        except: pass

    def get_prompt(self, uuid: str): 
        return self.database.get(uuid, {}).get("prompt")
    
    def get_model(self, uuid: str): 
        return self.database.get(uuid, {}).get("model")
    
    def get_seed(self, uuid: str): 
        return self.database.get(uuid, {}).get("seed")
    
    def get_cfg_scale(self, uuid: str): 
        return self.database.get(uuid, {}).get("cfg_scale")
    
    def get_steps(self, uuid: str): 
        return self.database.get(uuid, {}).get("steps")
    
    def get_sampler(self, uuid: str): 
        return self.database.get(uuid, {}).get("sampler")
    
    def get_created_date(self, uuid: str): 
        return self.database.get(uuid, {}).get("created_date")
    
    def get_all_uuids(self): 
        return list(self.database.keys())
    
    def __len__(self): 
        return len(self.database)
