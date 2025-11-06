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

import cfg
import json
import os.path
from ImageID import ImageID
from ImageData import ImageData
from ImageViewer import ImageViewer


class Gallery:
    # 1. Constructor
    def __init__(self,
                 name: str = "Unnamed Gallery",
                 image_id: ImageID = None,
                 image_data: ImageData = None,
                 image_viewer: ImageViewer = None):
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
        self.uuids = []

        self._image_id = image_id
        self._image_data = image_data
        self._image_viewer = image_viewer

    # Mètodes màgics
    def __len__(self) -> int:
        return len(self.uuids)

    def __str__(self) -> str:
        return f"Gallery '{self.name}' ({len(self.uuids)} imatges, Descripció: {self.description})"

    # 2. Func5: Càrrega des de JSON
    def load_file(self, file: str) -> None:
        """
        Llegeix un arxiu JSON amb la definició de la galeria.
        Valida que cada imatge referenciada (path) existeixi i estigui registrada.
        Emmagatzema internament els UUIDs de les imatges vàlides.
        """
        if self._image_id is None or self._image_data is None:
            print("ERROR (Gallery): Dependències ImageID o ImageData no inicialitzades. Saltant càrrega.")
            return

        try:
            with open(file, 'r') as f:
                data = json.load(f)

            self.name = data.get("gallery_name", self.name)
            self.description = data.get("description", "N/A")
            self.created_date = data.get("created_date", "N/A")

            image_paths = data.get("images", [])
            self.uuids = []

            for relative_path in image_paths:
                # Path absolut basat en ROOT_DIR
                absolute_path = os.path.join(cfg.ROOT_DIR, relative_path)

                uuid = self._image_id.get_uuid(absolute_path)
                if uuid:
                    self.uuids.append(uuid)
                    if self._image_data.get_prompt(uuid) is None:
                        try:
                            self._image_data.load_metadata(uuid)
                        except Exception as meta_e:
                            print(f"WARNING (Gallery): No s'han pogut carregar metadades per {uuid}: {meta_e}")
                else:
                    print(f"WARNING (Gallery): Imatge '{relative_path}' ignorada, no té UUID registrat.")

        except FileNotFoundError:
            print(f"ERROR (Gallery): Arxiu de galeria no trobat: {file}")
            return
        except json.JSONDecodeError:
            print(f"ERROR (Gallery): Format JSON invàlid a l'arxiu: {file}")
        except Exception as e:
            print(f"ERROR (Gallery): Error inesperat carregant {file}: {e}")

    # 3. Func5: Visualització
    def show(self) -> None:
        """
        Visualitza totes les imatges de la galeria en ordre utilitzant ImageViewer.show_image().
        """
        if self._image_viewer is None:
            print("ERROR (Gallery): Dependència ImageViewer no inicialitzada. Saltant visualització.")
            return

        print(f"\n--- Visualitzant Galeria: {self.name} (Total: {len(self.uuids)} imatges) ---")

        if not self.uuids:
            print("La galeria està buida.")
            return

        for i, uuid in enumerate(self.uuids):
            print(f"\n[Mostrant Imatge {i+1}/{len(self.uuids)} de la Galeria '{self.name}']")
            self._image_viewer.show_image(uuid)

        print(f"\n--- Fi de la Galeria: {self.name} ---")

    # 4. Func7: Manipulació Dinàmica
    def add_image_at_end(self, uuid: str) -> None:
        """Afegeix una imatge (UUID) al final de la galeria, si no hi és ja."""
        if uuid not in self.uuids:
            self.uuids.append(uuid)

    def remove_first_image(self) -> None:
        """Elimina la primera imatge de la galeria (si existeix)."""
        if self.uuids:
            self.uuids.pop(0)

    def remove_last_image(self) -> None:
        """Elimina l'última imatge de la galeria (si existeix)."""
        if self.uuids:
            self.uuids.pop()
