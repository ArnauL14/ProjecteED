# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.
Actua com a nexe entre ImageData i la visualització al sistema operatiu.
NO guarda informació interna.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""

# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.
"""

import cfg
import os.path
from PIL import Image
from ImageID import ImageID
from ImageData import ImageData

class ImageViewer:

    # 1. Constructor
    def __init__(self, image_data: ImageData):
        """
        Inicialitza la classe amb les dependències necessàries.
        """
        self._image_data = image_data

    # Mètodes Màgics Obligatoris
    def __len__(self) -> int:
        """
        Retorna la quantitat d'elements gestionats.
        """
        return len(self._image_data)
    
    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"ImageViewer (Connectat a {len(self._image_data)} imatges)"
    
    # 2. Funcions d'Accés
    
    def print_image(self, uuid: str) -> None:
        """
        Imprimeix per pantalla totes les metadades de la imatge.
        """
        # Obtenim les dades bàsiques (poden ser string o None objecte)
        prompt = self._image_data.get_prompt(uuid)
        model = self._image_data.get_model(uuid)
        seed = self._image_data.get_seed(uuid)
        cfg_scale = self._image_data.get_cfg_scale(uuid)
        steps = self._image_data.get_steps(uuid)
        sampler = self._image_data.get_sampler(uuid)
        generated = self._image_data.get_generated(uuid)
        created_date = self._image_data.get_created_date(uuid)
        
        width, height = self._image_data.get_dimensions(uuid)
        file_path = self._image_data.get_file_path(uuid)
        
        # Format per a la sortida
        print("\n" + "="*50)
        print(f"Metadades de la imatge [{uuid}]")
        print("="*50)
        
        # ** CORRECCIÓ CLAU **: Tractament de 'None' i truncament del prompt
        display_prompt = prompt if isinstance(prompt, str) else "N/A"
        if len(display_prompt) > 100 and display_prompt != "N/A":
             display_prompt = display_prompt[:100] + "..."
             
        # Funció auxiliar per imprimir "N/A" si el valor és None objecte
        def format_field(value):
            return str(value) if value is not None else 'N/A'

        # Mostrar les dades
        print(f" Dimensions: {format_field(width)}x{format_field(height)} pixels" if width is not None else " Dimensions: N/A")
        print(f" Prompt:     {display_prompt}")
        print(f" Model:      {format_field(model)}")
        print(f" Seed:       {format_field(seed)}")
        print(f" CFG Scale:  {format_field(cfg_scale)}")
        print(f" Steps:      {format_field(steps)}")
        print(f" Sampler:    {format_field(sampler)}")
        print(f" Generated:  {format_field(generated)}")
        print(f" Created:    {format_field(created_date)}")
        print(f" UUID:       {uuid}")
        print(f" Arxiu:      {format_field(file_path)}")
        print("="*50)


    def show_file(self, file: str) -> None:
        """
        Mostra la imatge especificada utilitzant PIL.
        """
        # Construïm el path absolut
        full_path = os.path.join(cfg.get_root(), file)
        
        if not os.path.isfile(full_path):
             print(f"ERROR: No es pot mostrar l'arxiu. Path inexistent: {full_path}")
             return
             
        print(f"\n[Image Viewer] Mostrant imatge: {full_path}")
        try:
            img = Image.open(full_path)
            img.show()
        except Exception as e:
            print(f"ERROR: No es pot mostrar la imatge: {e}")
            print("Potser necessiteu instal·lar un visualitzador d'imatges o configurar PIL.")

    
    def show_image(self, uuid: str, mode: int = None) -> None:
        """
        Combina la impressió de metadades i la visualització de l'arxiu
        segons el mode.
        """
        display_mode = mode if mode is not None else cfg.DISPLAY_MODE
        
        # Obtenim el path de l'arxiu (pot ser string o None objecte)
        file_path = self._image_data.get_file_path(uuid)
        
        # 1. Mode 0 o 1: Imprimir Metadades
        if display_mode == 0 or display_mode == 1:
            self.print_image(uuid)
        
        # 2. Mode 1 o 2: Mostrar Imatge
        if (display_mode == 1 or display_mode == 2) and isinstance(file_path, str):
            # Utilitzem show_file
            self.show_file(file_path)
            
            # 3. Esperar confirmació (Només si s'ha mostrat la imatge)
            print("\nImatge mostrada. Premi Enter per continuar...")
            try:
                input() 
            except EOFError:
                pass
        elif file_path is None:
             print(f"ERROR: No es pot visualitzar la imatge amb UUID {uuid}. Path canònic no trobat.")
