from requests import get as get_requests
from bs4 import BeautifulSoup

TILDES = {'á': '%E1', 'é': '%E9', 'í': '%ED', 'ó': '%F3', 'ú': '%FA'}
PERSONAS = {'primera':'1ra', 'segunda':'2da', 'tercera':'3ra'}

def clasificacion_morfologica_verbo(verbo):
    verbo = ''.join([TILDES.get(c, c) for c in verbo])
    http_request = get_requests('https://www.elconjugador.com/conjugacion/verbo/' + verbo)
    soup = BeautifulSoup(http_request.text, 'lxml')
    titulo = soup.find('h2')
    if titulo:
        try:
            tabla = [celda.text.lower().strip() for celda in soup.find_all('td')]
            modo, _, tiempo = tabla[-2].partition(' ')
            persona, _, _, numero = tabla[-1].split()
            return f"""
            Tiempo: {tiempo}
            Persona: {PERSONAS.get(persona)}
            Número: {numero}
            Modo: {modo}
            Infinitivo: {tabla[6]}
            """
        except ValueError:
            return 'Es un verboide.'
    else:
        return 'Verbo no encontrado.'

input(clasificacion_morfologica_verbo(input('Introduce un verbo: ')))
