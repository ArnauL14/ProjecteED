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

import cfg                      # Per a DISPLAY_MODE
import os.path
from PIL import Image           # Per a la funció show_file
from ImageID import ImageID     # Encara que no s'utilitza directament, la deixem per si calgués
from ImageData import ImageData # Necessari per obtenir les metadades

class ImageViewer:

    # 1. Constructor
    # MODIFICACIÓ CLAU: Només accepta l'argument image_data
    def __init__(self, image_data: ImageData):
        """
        Inicialitza la classe amb les dependències necessàries.
        """
        # Ja no rebem ImageID com a argument, només guardem la referència a ImageData
        # que és d'on realment es consulten totes les metadades i el path.
        self._image_data = image_data

    # Mètodes Màgics Obligatoris (Requisit: totes les classes)
    def __len__(self) -> int:
        """
        Retorna la quantitat d'elements gestionats per la classe que consulta
        (en aquest cas, la mida de la col·lecció de metadades).
        """
        return len(self._image_data)
    
    def __str__(self) -> str:
        """Retorna una representació en text de la classe."""
        return f"ImageViewer (Connectat a {len(self._image_data)} imatges)"
    
    # 2. Funcions d'Accés
    
    def print_image(self, uuid: str) -> None:
        """
        Imprimeix per pantalla totes les metadades de la imatge identificada per l'UUID.
        Consulta les dades a l'objecte ImageData.
        """
        # Obtenim les dades bàsiques, utilitzant None com a valor per defecte si no existeix
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
        
        # Truncament del prompt si és molt llarg
        display_prompt = prompt if prompt is not None else "None"
        if len(display_prompt) > 100:
             display_prompt = display_prompt[:100] + "..."
             
        # Mostrar les dades (utilitzant 'N/A' si el valor és l'objecte None)
        print(f" Dimensions: {width}x{height} pixels" if width is not None else " Dimensions: N/A")
        print(f" Prompt:     {display_prompt}")
        print(f" Model:      {model if model is not None else 'N/A'}")
        print(f" Seed:       {seed if seed is not None else 'N/A'}")
        print(f" CFG Scale:  {cfg_scale if cfg_scale is not None else 'N/A'}")
        print(f" Steps:      {steps if steps is not None else 'N/A'}")
        print(f" Sampler:    {sampler if sampler is not None else 'N/A'}")
        print(f" Generated:  {generated if generated is not None else 'N/A'}")
        print(f" Created:    {created_date if created_date is not None else 'N/A'}")
        print(f" UUID:       {uuid}")
        print(f" Arxiu:      {file_path if file_path is not None else 'N/A'}")
        print("="*50)


    def show_file(self, file: str) -> None:
        """
        Mostra la imatge especificada utilitzant PIL.
        'file' ha de ser el path canònic relatiu (ex: 'generated_images/cat.png').
        """
        # Construïm el path absolut per al visualitzador
        full_path = os.path.join(cfg.get_root(), file)
        
        if not os.path.isfile(full_path):
             print(f"ERROR: No es pot mostrar l'arxiu. Path inexistent: {full_path}")
             return
             
        print(f"\n[Image Viewer] Mostrant imatge: {full_path}")
        try:
            # Obrim i mostrem la imatge amb el visualitzador per defecte del SO
            img = Image.open(full_path)
            img.show()
        except Exception as e:
            print(f"ERROR: No es pot mostrar la imatge: {e}")
            print("Potser necessiteu instal·lar un visualitzador d'imatges o configurar PIL.")

    
    def show_image(self, uuid: str, mode: int = None) -> None:
        """
        Combina la impressió de metadades i la visualització de l'arxiu
        segons el mode (o cfg.DISPLAY_MODE per defecte).

        Args:
            uuid (str): Identificador de la imatge a mostrar.
            mode (int): 0: només metadades, 1: metadades + imatge, 2: només imatge.
                        Si és None, utilitza cfg.DISPLAY_MODE.
        """
        # Utilitzem el mode passat o el mode de configuració
        display_mode = mode if mode is not None else cfg.DISPLAY_MODE
        
        # Obtenim el path de l'arxiu (necessari per al mode 1 i 2)
        file_path = self._image_data.get_file_path(uuid)
        
        # 1. Mode 0 o 1: Imprimir Metadades
        if display_mode == 0 or display_mode == 1:
            self.print_image(uuid)
        
        # 2. Mode 1 o 2: Mostrar Imatge
        if (display_mode == 1 or display_mode == 2) and file_path is not None:
            # Utilitzem show_file, que no espera el tancament
            self.show_file(file_path)
            
            # 3. Esperar confirmació (Només si s'ha mostrat la imatge)
            #    Això fa que la funció sigui SÍNCRONA.
            print("\nImatge mostrada. Premi Enter per continuar...")
            try:
                # Necessitem fer una pausa per esperar que l'usuari tanqui la imatge
                input() 
            except EOFError:
                # Per si s'executa en entorns que no permeten input()
                pass
        elif file_path is None:
             # Aquest missatge es manté per a una bona gestió d'errors
             print(f"ERROR: No es pot visualitzar la imatge amb UUID {uuid}. Path canònic no trobat.")
