# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""

import os
import cfg  # Importem cfg per fer servir get_canonical_pathfile

class ImageFiles:

    def __init__(self):
        """
        Inicialitza el gestor d'arxius.
        'current_files' guarda l'estat de l'últim escaneig.
        'previous_files' guarda l'estat de l'escaneig anterior per
        poder calcular les diferències.
        """
        self.current_files = set()
        self.previous_files = set()

    def __len__(self) -> int:
        """Retorna el nombre total d'arxius PNG actuals a la col·lecció."""
        return len(self.current_files) # Retorna la longitud del set actual

    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"ImageFiles (Total: {len(self.current_files)} arxius únics)"

    def reload_fs(self, path: str) -> None:
        """
        Recorre el directori especificat (recursivament) i actualitza 
        la llista interna d'arxius PNG.
        """
        
        # 1. L'estat actual passa a ser l'estat anterior
        #    (permet calcular els canvis)
        self.previous_files = self.current_files

        # 2. Creem un nou set buit per als resultats d'aquest escaneig
        new_files_set = set()

        # 3. Escanegem el directori recursivament
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    # 4. Comprovem que sigui .png (case-insensitive)
                    if file.lower().endswith('.png'):
                        
                        # 5. Obtenim el path complet per poder processar-lo
                        full_path = os.path.join(root, file)
                        
                        # 6. El convertim al path canònic (relatiu)
                        #    Això és un requisit clau
                        canonical_path = cfg.get_canonical_pathfile(full_path)
                        
                        # 7. L'afegim al nostre nou set
                        new_files_set.add(canonical_path)

        except FileNotFoundError:
            print(f"ERROR: El directori {path} no existeix.")
        except Exception as e:
            print(f"ERROR: Ha ocorregut un error durant l'escaneig: {e}")

        # 8. Actualitzem el set 'current' amb els resultats
        self.current_files = new_files_set
        # print(f"ImageFiles: Escaneig completat. Trobats {len(self.current_files)} arxius.")

    def files_added(self) -> list:
        """
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().
        """
        # Fem servir la diferència de conjunts:
        # (elements que estan a 'current' però NO a 'previous')
        added_set = self.current_files - self.previous_files
        return list(added_set)

    def files_removed(self) -> list:
        """
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().
        """
        # Fem servir la diferència de conjunts a la inversa:
        # (elements que estan a 'previous' però NO a 'current')
        removed_set = self.previous_files - self.current_files
        return list(removed_set)
