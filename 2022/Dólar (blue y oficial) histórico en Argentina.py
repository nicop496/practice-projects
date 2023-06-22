import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pyinputplus import inputCustom
from more_itertools import sort_together
from os.path import exists as path_exists
from calendar import monthrange


MONTHS = 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'


def get_data(dolar_type: str, months_to_get: list, file_name: str):
    dates, values, percentages = [], [], [0]
    last_value = None

    # Recorrer los años desde 2011 hasta el actual
    for year in range(2011, datetime.now().year + 1):
        # Recorrer los meses de cada año
        for month in MONTHS if year != datetime.now().year else MONTHS[:datetime.now().month]:
            if not month in months_to_get:
                continue

            # Obtener el valor del dólar (de venta) al finalizar ese mes
            url = f'https://dolarhistorico.com/cotizacion-dolar-{dolar_type}/mes/{month}-{year}'
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            _, dolar_value = [float(i.text.replace(',', '.')) for i in soup.find_all(
                class_='h5 mb-0 font-weight-bold text-gray-800')]
            
            month = MONTHS.index(month) + 1 # Convertir month en un número
            dates.append(datetime(year, month, monthrange(year, month)[1]))
            values.append(dolar_value)
            
            if last_value:
                difference = dolar_value - last_value
                try:
                    percentages.append(round(100 / (dolar_value / difference), 2))  
                except ZeroDivisionError:
                    percentages.append(0)
            last_value = dolar_value
    
    df = pd.DataFrame({'Fecha': dates, 'Valor': values,'Porcentaje': percentages})
    df.to_excel(file_name, index=False)
    return df


def main():
    ####### Input
    def months_string_to_list(months: str):
        months = set(months.lower().replace(' ', '').split(',')) # Convertir en lista
        if all([month in MONTHS for month in months]): # Si los meses son correctos:
            # Ordenarlos y retornarlos
            return sort_together([[MONTHS.index(m) + 1 for m in months], months])[1]
        else:
            raise Exception('Alguno de esos meses no existe.')

    months = inputCustom(months_string_to_list, 'Introduce los meses de los que quieras saber el valor en cada año (separados por comas): ')
    
    ####### Dataframe y excel
    beauty_months = f"{', '.join(months[:-1])} y {months[-1]}" if len(months) != 1 else months[0]
    current_month = MONTHS[datetime.now().month - 1]
    file_name = lambda dolar_type: f'Datos del dólar {dolar_type} en los meses de {beauty_months} hasta {current_month} de {datetime.now().year}.xlsx'

    if path_exists(file_name('blue')):
        blue_df = pd.read_excel(file_name('blue'))
        oficial_df = pd.read_excel(file_name('oficial'))

    else:
        print('Se están obteniendo los datos...')
        blue_df = get_data('blue', months, file_name('blue'))
        oficial_df = get_data('oficial', months, file_name('oficial'))

    ####### Graficar
    # Precio
    plt.subplot(2, 1, 1)
    plt.ylabel('Precio')
    plt.grid(linestyle='dotted')
    plt.plot(blue_df['Fecha'], blue_df['Valor'], 'h-', label='Dólar blue', color='blue')
    plt.plot(oficial_df['Fecha'], oficial_df['Valor'], 'h-', label='Dólar oficial', color='orange')
    plt.legend()

    # Porcentaje
    plt.subplot(2, 1, 2)
    plt.ylabel('Porcentaje')
    plt.grid(linestyle='dotted')    
    plt.plot(blue_df['Fecha'], blue_df['Porcentaje'], 'o:', label='Dólar blue', color='blue')
    plt.plot(oficial_df['Fecha'], oficial_df['Porcentaje'], 'o:', label='Dólar oficial', color='orange',)

    plt.suptitle("Precio histórico del dólar en Argentina")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gcf().autofmt_xdate(rotation=30)
    plt.show()

if __name__ == '__main__':
    main()

