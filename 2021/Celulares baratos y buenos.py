from bs4 import BeautifulSoup
from requests import get
from webbrowser import open as open_browser
from tkinter import *
from tkinter import messagebox

BATERIA = 'Capacidad de la batería' 
SISTEMA_OPERATIVO = 'Versión original del sistema operativo'
CAMARA_TRASERA = 'Resolución de la cámara trasera principal'
CAMARA_FRONTAL = 'Resolución de la cámara frontal principal'
HTML_PARSER = 'lxml'

def any_sub_string(string, sub_strings):
    """
    Si alguna sub-cadena de caracteres
    se encuentra en el string pasado,
    devuelve True, sino False.
    """
    for sub_string in sub_strings:
        if sub_string in string:
            return True
    return False

def get_phones(url, not_wanted_tags, 
               wanted_tags,
               min_batery,
               min_sys_version,
               min_front_camera_cuality,
               min_back_camera_cuality):
    """
    Si alguna etiquita de las 'wanted_tags'
    NO se encuentra en el título de la venta
    el celular será descartado. 
    Además, si alguna etiqueta de 'not_wanted_tags' 
    se encuentra en el título de la venta el celular
    también será descartado.
    """
    http_request = get(url)
    soup = BeautifulSoup(http_request.text, HTML_PARSER)

    #-------Obtener un diccionario con el título de cada celular, su precio y su link.
    titles_html = soup.find_all(class_='ui-search-item__group ui-search-item__group--title')
    titles = [a_label.text.lower() for a_label in titles_html]
    links = [a_label.a['href'] for a_label in titles_html]
    prices = [int(i.text.split()[0]) for i in soup.find_all(class_='price-tag ui-search-price__part')]
    phones = dict(zip(titles, list(zip(prices, links))))

    #-------Filtrar los celulares por los títulos con ciertas etiquetas
    for bad_phone in filter(lambda title: any_sub_string(title, not_wanted_tags) or not any_sub_string(title, wanted_tags), titles):
        try:
            phones.pop(bad_phone)
        except KeyError: 
            pass #si hay dos celulares iguales ocurre este error

    #-------Volver a filtrar pero ahora entrando al link de cada celular
    desc_filter_tags = {'rot', 'repuesto', 'reparar', 'no funciona', 'módulo', 'astillad', 'rayad', 'cambiar'}
    bad_phones = set()
    for title, price_and_link in phones.items():
        phone_url = price_and_link[1]
        r = get(phone_url)
        phone_soup = BeautifulSoup(r.text, HTML_PARSER)

        #---Filtrar por la descripción con etiquetas
        description = phone_soup.find(class_='ui-pdp-description__content')
        if any_sub_string(description.text.lower(), desc_filter_tags):
            bad_phones.add(title)

        #---Filtrar por estadísticas
        #obtener las estadísticas
        stats_names = [name.text for name in phone_soup.find_all(class_='andes-table__header andes-table__header--left ui-vpp-striped-specs__row__column ui-vpp-striped-specs__row__column--id')]
        stats_values = [value.text for value in phone_soup.find_all(class_='andes-table__column--value')]
        
        #si alguna estadística no se encuentra en la publicación del celular descartar el mismo
        if any([
            BATERIA and not BATERIA in stats_names,
            SISTEMA_OPERATIVO and not SISTEMA_OPERATIVO in stats_names,
            CAMARA_TRASERA and not CAMARA_TRASERA in stats_names,
            CAMARA_FRONTAL and not CAMARA_FRONTAL in stats_names
        ]):
            bad_phones.add(title)

        for name, value in zip(stats_names, stats_values):
            #(si la batería aparece en ah y no en mah la cambio para que no haya problemas)
            if name == BATERIA and value.split()[1].lower() == 'ah':
                value = int(value.replace('.', '')) * 100
            
            #comparar las estadísticas con los parámetros
            """
            ejemplos de cómo aparecen las estadísticas:
            -batería: 3000 mAh
            -sistema operativo: 4.0 KitKat
            -cámara: 8 mpx
            """
            if any([
                name == BATERIA and int(value.split()[0]) < min_batery,
                name == SISTEMA_OPERATIVO and int(value[0]) < min_sys_version, 
                name == CAMARA_TRASERA and int(value.split()[0].split('.')[0]) < min_back_camera_cuality,
                name == CAMARA_FRONTAL and int(value.split()[0].split('.')[0]) < min_front_camera_cuality,
            ]):
                bad_phones.add(title)

    for bad_phone in bad_phones:
        phones.pop(bad_phone)

    #-------Hacer lo mismo con as páginas siguientes
    next_page_url = soup.find(class_='andes-pagination__link ui-search-link')
    if next_page_url:
        if next_page_url.text == 'Siguiente':
            next_page_phones = get_phones(
                next_page_url['href'],
                not_wanted_tags,
                wanted_tags,
                min_batery,
                min_sys_version,
                min_front_camera_cuality,
                min_back_camera_cuality)
            phones.update(next_page_phones)
            
    return phones


class GUI:
    root = Tk()
    root.title('Celulares')

    trademarks = 'Samsung', 'Motorola', 'Huawei', 'Sony', 'Xiaomi', 'LG', 'TCL', 'Alcatel', 'Iphone', 'Nokia'
    trademarks_btns_info = {td : IntVar() for td in trademarks}

    # Crear los widgets que no tienen la propiedad command
    options_frame = LabelFrame(root, relief=GROOVE, text='Opciones', bd=5, padx=5, pady=5)
    min_price_label = Label(options_frame, text='Precio mínimo:')
    min_price_entry = Entry(options_frame)
    max_price_label = Label(options_frame, text='Precio máximo:')
    max_price_entry = Entry(options_frame)
    min_batery_label = Label(options_frame, text='Batería mínima (mAh):')
    min_batery_entry = Entry(options_frame)
    min_android_version_label = Label(options_frame, text='Versión mínima\ndel sistema operativo:')
    min_android_version_entry = Entry(options_frame)
    min_backcamera_cuality_label = Label(options_frame, text='Calidad mínima de\nla cámara trasera:')
    min_backcamera_cuality_entry = Entry(options_frame)
    min_frontcamera_cuality_label = Label(options_frame, text='Calidad mínima de\nla cámara frontal:')
    min_frontcamera_cuality_entry = Entry(options_frame)
    min_ram_label = Label(options_frame, text='RAM mínima:')
    min_ram_entry = Entry(options_frame)
    min_storage_label = Label(options_frame, text='Almacenamiento interno mínimo:')
    min_storage_entry = Entry(options_frame)

    entries = {min_price_entry, max_price_entry, min_batery_entry,
               min_android_version_entry, min_backcamera_cuality_entry,
               min_frontcamera_cuality_entry, min_ram_entry, min_storage_entry
               }

    trademarks_frame = LabelFrame(root, relief=GROOVE, text='Seleccionar marcas', bd=5)
    for td in trademarks:
        Checkbutton(trademarks_frame, text=td, variable=trademarks_btns_info[td])


    def __init__(self):
        # Crear el resto de los widgets
        self.search_button = Button(self.root, text='Buscar', command=self.search_button_command)
        self.save_links_button = Button(self.root, text='Guardar links', command=self.save_links, state=DISABLED)
        change_all_button = Button(self.trademarks_frame, text='Cambiar todos', command=self.toggle_all_trademarks, padx=3)

        # Posicionar los widgets
        self.trademarks_frame.grid(row=0, column=0, pady=5, padx=5, columnspan=2)
        change_all_button.pack(pady=5, fill=BOTH)
        for btn in self.trademarks_frame.winfo_children():
            btn.pack(anchor=W)

        self.options_frame.grid(row=0, column=2, padx=5, pady=5, columnspan=3)
        for index, widget in enumerate(self.options_frame.winfo_children()):
            widget.grid(row=index // 2, column=index % 2 + 1, pady=5)

        self.save_links_button.grid(row=1, column=3, padx=15, pady=10)
        self.search_button.grid(row=1, column=2, padx=15, pady=10)

        # # # # # # # # # # # # #
        self.root.mainloop()
    
    def save_links(self):
        file = open('links de los celulares.txt', 'w')
        for phone, price_and_link in self.phones.items():
            file.write(f'{phone} ---> {price_and_link}\n\n')
        file.close()

    def search_button_command(self):
        messagebox.showinfo('Paciencia', 'Espera unos segundos.')
        try:
            self.phones = get_phones(self.url,
                                     self.not_wanted_tags,
                                     self.wanted_tags,
                                     int(self.min_batery_entry.get()),
                                     int(self.min_android_version_entry.get()),
                                     int(self.min_frontcamera_cuality_entry.get()),
                                     int(self.min_backcamera_cuality_entry.get())
                                     )
        except ValueError:
            messagebox.showerror('Error', 'Debes llenar los espacios\nen blanco (y con números enteros).')

        else:
            if not self.phones:
                messagebox.showerror('Error', 'No se encontraron celulares con esas características.')
                return
            for phone in self.phones.values():    
                open_browser(phone[1])
            self.save_links_button.config(state = ACTIVE)

    def toggle_all_trademarks(self):
        for btn in self.trademarks_frame.winfo_children(): 
            if type(btn) != Checkbutton:
                continue
            btn.toggle()

    @property
    def not_wanted_tags(self):
        return [
            'rota', 'pantalla',
            'descripción', 'leer',
            'reparar', 'repuesto',
            'no funciona', 'no anda',
            'módulo', 'roto',
            'no funciona', 'módulo', 
            'astillad', 'rayad',
            'falla'
        ] + [td.lower() for td, value in self.trademarks_btns_info.items() if not value.get()]

    @property
    def wanted_tags(self):
        return [

        ] + [td.lower() for td, value in self.trademarks_btns_info.items() if value.get()]

    @property
    def url(self):
        ram = f'mas-de-{self.min_ram_entry.get()}-GB-ram'
        storage = f'mas-de-{self.min_storage_entry.get()}-gb'
        place = 'capital-federal/almagro-o-caballito-o-villa-crespo-o-palermo'
        price_range = f'smartphone_PriceRange_{self.min_price_entry.get()}-{self.max_price_entry.get()}'
        return f'https://celulares.mercadolibre.com.ar/{storage}/{ram}/{place}/{price_range}'



GUI()
