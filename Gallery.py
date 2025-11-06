# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.
Implementa Func5 (Càrrega i Visualització) i Func7 (Manipulació Dinàmica).

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

import cfg                      # Per a ROOT_DIR i altres configuracions
import json                     # Per llegir arxius JSON
import os.path
from ImageID import ImageID     # Necessari per obtenir UUID a partir del path
from ImageData import ImageData # Necessari per obtenir el path canònic a partir de l'UUID
from ImageViewer import ImageViewer # Necessari per a la funció show()

class Gallery:
    # 1. Constructor
    def __init__(self, name: str, image_id: ImageID, image_data: ImageData, image_viewer: ImageViewer):
        """
        Inicialitza la galeria.
        Args:
            name (str): Nom intern de la galeria.
            image_id (ImageID): Referència al gestor d'UUIDs.
            image_data (ImageData): Referència al gestor de metadades.
            image_viewer (ImageViewer): Referència al visualitzador.
        """
        self.name = name
        self.description = ""
        self.created_date = ""
        self.uuids = [] # Llista d'UUIDs que defineixen la galeria
        
        # Dependències
        self._image_id = image_id
        self._image_data = image_data
        self._image_viewer = image_viewer

    # Mètodes Màgics Obligatoris
    def __len__(self) -> int:
        """Retorna el nombre d'imatges actuals a la galeria."""
        return len(self.uuids)

    def __str__(self) -> str:
        """Retorna una representació en text de la galeria."""
        return f"Gallery '{self.name}' ({len(self.uuids)} imatges, Descripció: {self.description})"

    # 2. Func5: Càrrega des de JSON
    def load_file(self, file: str) -> None:
        """
        Llegeix un arxiu JSON amb la definició de la galeria.
        Valida que cada imatge referenciada (path) existeixi i estigui registrada.
        Emmagatzema internament els UUIDs de les imatges vàlides.
        """
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                
            # Actualitzem les metadades de la galeria
            self.name = data.get("gallery_name", self.name)
            self.description = data.get("description", "N/A")
            self.created_date = data.get("created_date", "N/A")
            
            # Processem la llista de paths relatius (Func5)
            image_paths = data.get("images", [])
            self.uuids = [] # Reiniciem la llista d'UUIDs
            
            for relative_path in image_paths:
                # El JSON ja conté paths relatius canònics
                
                # 1. Intentem obtenir el UUID per aquest path
                uuid = self._image_id.get_uuid(relative_path)
                
                if uuid:
                    # 2. Si el UUID existeix, la imatge és vàlida
                    self.uuids.append(uuid)
                    
                    # Opcional, carregar metadades si encara no s'han carregat
                    # (Si no, Gallery.show() fallaria en mostrar Prompt, etc.)
                    # És bona pràctica assegurar que la dada existeix si la necessitarem de seguida
                    if self._image_data.get_prompt(uuid) is None:
                         self._image_data.load_metadata(uuid)

                else:
                    # La imatge no està registrada/no existeix a la col·lecció
                    print(f"WARNING (Gallery): Imatge '{relative_path}' ignorada, no té UUID registrat.")
                    
        except FileNotFoundError:
            print(f"ERROR (Gallery): Arxiu de galeria no trobat: {file}")
        except json.JSONDecodeError:
            print(f"ERROR (Gallery): Format JSON invàlid a l'arxiu: {file}")
        except Exception as e:
            print(f"ERROR (Gallery): Error inesperat carregant {file}: {e}")

    # 3. Func5: Visualització
    def show(self) -> None:
        """
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image() (amb el mode per defecte).
        """
        print(f"\n--- Visualitzant Galeria: {self.name} (Total: {len(self.uuids)} imatges) ---")
        
        if not self.uuids:
            print("La galeria està buida.")
            return

        for i, uuid in enumerate(self.uuids):
            print(f"\n[Mostrant Imatge {i+1}/{len(self.uuids)} de la Galeria '{self.name}']")
            
            # Cridem al visualitzador, que s'encarregarà d'imprimir i mostrar l'arxiu.
            # Utilitzem el mode configurat a cfg.DISPLAY_MODE
            self._image_viewer.show_image(uuid)
            
            # Nota: ImageViewer.show_image ja gestiona la pausa amb input()

        print(f"\n--- Fi de la Galeria: {self.name} ---")

    # 4. Func7: Manipulació Dinàmica
    
    def add_image_at_end(self, uuid: str) -> None:
        """
        Afegeix una imatge (UUID) al final de la galeria.
        Nota: L'enunciat no demana validar si l'UUID existeix a ImageData, 
              però un sistema robust ho faria. Aquí l'afegim directament a la llista.
        """
        self.uuids.append(uuid)
        # print(f"Gallery '{self.name}': UUID {uuid} afegit al final.")

    def remove_first_image(self) -> None:
        """
        Elimina la primera imatge de la galeria (si existeix).
        """
        if self.uuids:
            removed_uuid = self.uuids.pop(0) # pop(0) elimina i retorna el primer element
            # print(f"Gallery '{self.name}': Primera imatge ({removed_uuid}) eliminada.")
        else:
            print(f"WARNING (Gallery): La galeria '{self.name}' està buida. No es pot eliminar el primer element.")

    def remove_last_image(self) -> None:
        """
        Elimina l'última imatge de la galeria (si existeix).
        """
        if self.uuids:
            removed_uuid = self.uuids.pop() # pop() sense índex elimina i retorna l'últim
            # print(f"Gallery '{self.name}': Última imatge ({removed_uuid}) eliminada.")
        else:
            print(f"WARNING (Gallery): La galeria '{self.name}' està buida. No es pot eliminar l'últim element.")
