from pytube import YouTube, Playlist, exceptions
from pathlib import Path
from math import ceil
import pyinputplus as pyip


FORMATS = ['Video', 'Audio']
QUALITIES = ['Baja', 'Media', 'Alta']

url = pyip.inputURL(prompt='Introduzca el link del video o playlist: ')
print()
format_ = pyip.inputMenu(FORMATS, numbered=True, prompt='Elija el formato:\n')
print()
quality = pyip.inputMenu(QUALITIES, numbered=True, prompt='Elija la calidad:\n')


print(f'''
Formato: {format_}
Calidad: {quality}''')

format_ = [i == format_ for i in FORMATS]
quality = [i == quality for i in QUALITIES]

try:
    videos = []
    path = Path.home() / 'Downloads'
    
    if 'playlist' in url:
        playlist = Playlist(url)
        print(f'Playlist: "{playlist.title}"')
        videos = playlist.videos
        path /= playlist.title
    else:
        videos.append(YouTube(url))
        print(f'Video: "{videos[0].title}"')
    
    print('\nDescargando...')

    for video in videos:
        # Formato
        if format_[0]: # video
            streams = video.streams.filter(only_video=True).order_by('resolution')
        if format_[1]: # audio
            streams = video.streams.filter(only_audio=True).order_by('abr')

        
        # Calidad
        if quality[0]: #baja
            stream = streams[0]
        if quality[1]: #media
            stream = streams[ceil(len(streams) / 2)]
        if quality[2]: #alta
            stream = streams[-1]

        stream.download(path)                
            
except exceptions.RegexMatchError:
    print('\nERROR: Link inválido')
    raise
except exceptions.VideoPrivate:
    print('\nERROR: Video privado')
except exceptions.MembersOnly:
    print('\nERROR: Video solo para miembros del canal')
except exceptions.VideoRegionBlocked:
    print('\nERROR: Video no disponible en tu país')
except exceptions.VideoUnavailable:
    print('\nERROR: Video no disponible')
except KeyError as e:
    print('\nError al descargar. Probá con otro formato y/o calidad o intentá luego.')
except Exception as e:
    print('\nOcurrió un error inesperado:\n' + e)
else:
    if 'playlist' in url:
        print('\nPlaylist descargada correctamente.')
    else:
        print('\nVideo descargado correctamente.')
    print('Se guardó en la carpeta de descargas')

input('\nPresione ENTER para salir...')
