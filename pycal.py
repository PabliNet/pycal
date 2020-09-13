#!/usr/bin/env python3
from os import chmod, get_terminal_size, getuid, remove
from sys import argv, exit
from os.path import abspath, exists
from shutil import copy
from datetime import date, datetime
from locale import LC_ALL, setlocale
from calendar import day_abbr, monthcalendar

def fEsHoy (dia=0, color='1', hoy=date.today().strftime('%Y-%m-%d'), ayuda=False):
    hoy = hoy.split('-')
    d = {
        'k': ('\x1b[0;30m', 'negro'),
        'b': ('\x1b[0;34m', 'azul'),
        'c': ('\x1b[0;36m', 'celeste opaco'),
        'g': ('\x1b[0;32m', 'verde opaco'),
        'm': ('\x1b[0;35m', 'magenta'),
        'o': ('\x1b[0;33m', 'marrón'),
        'r': ('\x1b[0;31m', 'rojo'),
        'h': ('\x1b[0;37m', 'gris claro'),
        's': ('\x1b[1;30m', 'gris oscuro'),
        'u': ('\x1b[1;34m', 'azul brillante'),
        'l': ('\x1b[1;36m', 'celente brillante'),
        'e': ('\x1b[1;32m', 'verde brillante'),
        't': ('\x1b[1;35m', 'lila'),
        'y': ('\x1b[1;33m', 'amarillo'),
        'x': ('\x1b[1;31m', 'rojo brillante'),
        'w': ('\x1b[1;37m', 'blanco'),
        '0': ('\x1b[0m', 'normal'),
        '1': ('\x1b[01m', 'resaltado')
    }
    if ayuda:
        return {'-l': 'a la izquierda', '-c':'al centro', '-r':'a la derecha'}, (d.keys()), d[color]
    if len(hoy) == 2:
        return '', ''
    elif len(hoy) == 3:
        if dia == int(hoy[2]):
            return d[color][0], d['0'][0]
        else:
            return '', ''
    else:
        err(4)

def strDia (dia, color='', hoy=date.today().strftime('%Y-%m-%d')):
    if dia == 0:
        return '  '
    elif dia < 10:
        return fEsHoy(dia, color, hoy)[0] + ' ' + str(dia) + fEsHoy(dia, color, hoy)[1]
    else:
        return fEsHoy(dia, color, hoy)[0] + str(dia) + fEsHoy(dia, color, hoy)[1]

def alinear (donde, _chrs=0):
    if donde == '-l':
        return ''
    elif donde == '-c':
        return '^' + str(get_terminal_size().columns + _chrs)
    elif donde == '-r':
        return'>' + str(get_terminal_size().columns + _chrs)

def fMes (mes):
    lista = []
    for semana in mes:
        listSemana = []
        for nDia in semana:
            if isinstance(nDia, int):
                listSemana.append(strDia(nDia, paramColor, fecha))
            else:
                listSemana.append(nDia)
        lista.append(listSemana)
    return lista

def ayuda (ins):
    d = {
        '--install': 'instala pycal',
        '--uninstall': 'desinstala pycal',
        '--help': 'muestra esta ayuda y finaliza',
        '--version': 'informa de la versión y finaliza'
    }
    do = {
        '-y': 'año actual',
        '-Y': 'año anterior',
        '+Y': 'año siguiente',
        '-M': 'mes anterior',
        '+M': 'mes siguiente'
    }
    if ins == '--install':
        d.pop('--uninstall')
    elif ins == '--uninstall':
        d.pop('--install')
    else:
        exit()
    print (f'\x1b[0mModo de empleo: {argv[0]} [ALINEACIÓN] [AAAA-MM-DD] [COLOR]\n  o bien:  {argv[0]} [ALINEACIÓN] [AAAA-MM] [COLOR]\n  o bien:  {argv[0]} [ALINEACIÓN] [AAAA] [COLOR]\n  o bien:  {argv[0]} [ALINEACIÓN] [AAAA] [COLOR]\n  o bien:  {argv[0]} [ALINEACIÓN] [AAAA/MM/DD] [COLOR]', 'Muestra un calendario con el día actual resaltado.', 'Alineación:', sep='\n\n')
    for a in tuple(fEsHoy(ayuda=True)[0].keys()):
        print (format('  ' + a, '<18'), f'alinear {fEsHoy(ayuda=True)[0][a]}')
    print ('\nOpciones:')
    for o in tuple(do.keys()):
        print (format('  ' + o, '<18'), do[o])
    print ('\nColorear el día acual:')
    for COLOR in fEsHoy(ayuda=True)[1]:
        print (format('  ' + COLOR, '<18'), f'cambia a este {fEsHoy(color=COLOR, ayuda=True)[2][0]}{fEsHoy(color=COLOR, ayuda=True)[2][1]}\x1b[0m.')
    print ()
    for key in tuple(d.keys()):
        print(format(6 * ' ' + key,'<18'), d[key])
    exit()

def err (cod):
    err = '\x1b[0;31m[ERROR]\x1b[0m'
    cod -= 1
    t = (
        'No se pudo desinstalar Pycal',
        'Comando mal escrito',
        'Demasiados parámetros',
        'Resolución pequeña',
        'Fecha incompleta'
    )
    print (f'{err} {t[cod]}.')
    exit(cod)

def validarFecha (cadena):
    if cadena.count('/') != 0 and cadena.count('-') == 0:
        cadena = cadena.replace('/', '-')
    try:
        tupla = tuple(map(int, cadena.split('-')))
        if len(tupla) == 3:
            date(*tupla)
            return True
    except ValueError:
        return False
    if len(tupla) == 2:
        if tupla[0] >= 1900 and tupla[1] in range(1, 13):
            return True
    elif len(tupla) == 1 and tupla[0] >= 1900:
        return True
    elif not len(tupla) in (1, 2, 3):
        return False

def validar (lista):
    if len(lista) == 1:
        if lista[0] in tuple(fEsHoy(ayuda=True)[0].keys()):
            return 'a', lista[0]
        elif validarFecha(lista[0]):
            return 'f', lista[0]
        elif lista[0] in fEsHoy(ayuda=True)[1]:
            return 'c', lista[0]
        else:
            err(2)
    elif len(lista) == 2:
        if lista[0] in tuple(fEsHoy(ayuda=True)[0].keys()) and validarFecha(lista[1]):
            lista.insert(0, 'af')
        elif lista[0] in tuple(fEsHoy(ayuda=True)[0].keys()) and lista[1] in fEsHoy(ayuda=True)[1]:
            lista.insert(0, 'ac')
        elif validarFecha(lista[0]) and lista[1] in fEsHoy(ayuda=True)[1]:
            lista.insert(0, 'fc')
        elif lista[1].lower() == '--install':
            if getuid() == 0:
                try:
                    copy(cmd, destino)
                except EnvironmentError:
                    print ('\x1b[31m[ERROR]\x1b[0m No se pudo instalar pycal.')
                    exit(1)
                try:
                    chmod(destino, 0o755)
                except FileNotFoundError:
                    print (f'\x1b[31m[ERROR]\x1b[0m No se pudo dar permisos de ejecución a {comando}.')
                    exit(1)
                else:
                    print ('¡Instalado correctamente!')
                    exit()
            else:
                print ('\x1b[31m[ERROR]\x1b[0m Para instalar se necesita permisos de administrador.')
                exit(100)
        elif lista[1].lower() == '--uninstall':
            if getuid() == 0:
                try:
                    remove(destino)
                except OSError:
                    err(1)
                else:
                    print ('¡Desinstalado correctamente!')
                    exit()
            else:
                print ('\x1b[31m[ERROR]\x1b[0m Para desinstalar se necesita permisos de administrador.')
                exit(100)
        elif lista[1].lower() == '--help':
            ayuda(installer)
        elif lista[1].lower() == '--version':
            print (f'pycal 1.0\nCopyright © 2020\n\nDesarrollado por Pablo Alejandro Carravetti')
            exit()
        else:
            err(2)
        return lista
    elif len(lista) == 3:
        if lista[0] in tuple(fEsHoy(ayuda=True)[0].keys()) and validarFecha(lista[1]) and lista[2] in fEsHoy(ayuda=True)[1]:
            return lista
        else:
            err(2)

def igualarSemanas (lista, inicio, fin):
    for i in range(inicio, fin):
        for sxm in lista[inicio:fin]:
            if not 'cantSemanas' in locals():
                cantSemanas = []
            cantSemanas.append(len(sxm))
        
        cantSemanas.sort()

        for sxm in lista[inicio:fin]:
            while len(sxm) < cantSemanas[-1]:
                sxm.append(('  ' * 7).replace('  ',  '  -')[:-1].split('-'))
        cantSemanas.clear()
        return lista[inicio:fin]

def nMes (columnas):
    c = 0
    for i in range(0, 12):
        if i == 0:
            _mes = [format(datetime.strftime((datetime.strptime(str(i + 1), '%m')), '%B').capitalize(), '^20')]
        elif i % columnas == 0:
            c += 1
            _mes.append(format(datetime.strftime((datetime.strptime(str(i + 1), '%m')), '%B').capitalize(), '^20'))
        else:
            _mes[c] = str(_mes[c]) + '  ' + format(datetime.strftime((datetime.strptime(str(i + 1), '%m')), '%B').capitalize(), '^20')
    return _mes

def printcal (mes, semanas, c=0):
    for semana in mes:
        if not '_strMes' in locals():
            _strMes = []
        if c == 0:
            _strMes.append(' '.join(semana))
        else:
            if int(fecha.split('-')[2]) in listSemana[c]:
                semana = format(' '.join(semana))
            else:
                semana = format(' '.join(semana))
            _strMes.append(semana)
        c += 1
    return _strMes

def deltaFecha (opcion):
    _ano, _mes = tuple(map(int, date.today().strftime('%Y-%m').split('-')))
    if opcion == '-y':
        return str(_ano)
    elif opcion == '-Y':
        return str(_ano - 1)
    elif opcion == '+Y':
        return str(_ano + 1)
    elif opcion == '-M':
        _mes -= 1
        if _mes == 0:
            _ano -= 1
            _mes = 12
        return str(_ano) + '-' + str(_mes)
    elif opcion == '+M':
        _mes += 1
        if _mes == 13:
            _ano += 1
            _mes = 1
        return str(_ano) + '-' + str(_mes)

setlocale(LC_ALL, '')

for i in range(1, len(argv)):
    if argv[i] in ('-y', '-Y', '-M', '+Y', '+M'):
        argv[i] = deltaFecha(argv[i])

cmd = argv[0]
paramHorizontal = '-l'
paramFecha = fecha = date.today().strftime('%Y-%m')
paramColor = '1'

destino = comando = '/usr/local/bin/pycal'

if exists(comando):
    installer = '--uninstall'
else:
    installer = '--install'

if len(argv) > 1:
    if not (len(argv) == 2 and argv[1] in ('--help', '--version', installer)):
        argv.pop(0)
        argv.sort()
        contparam = len(argv)
    else:
        contparam = 1
else:
    contparam = 0

if contparam in range(2, 4):
    argv.sort()
    if argv[-2] in ('0', '1'):
        aux = [argv[-1], argv[-2]]
        argv = argv[:-2]
        argv.extend(aux)
elif contparam > 3:
    err(3)

if contparam > 0:
    validado = validar(argv)

if contparam == 1:
    if validado[0] == 'a':
        paramHorizontal = validado[1]
    elif validado[0] == 'f':
        paramFecha = validado[1]
    elif validado[0] == 'c':
        paramColor = validado[1]
elif contparam == 2:
    if validado[0] == 'af':
        paramHorizontal, paramFecha = validado[1:]
    elif validado[0] == 'ac':
        paramHorizontal, paramColor = validado[1:]
    elif validado[0] == 'fc':
        paramFecha, paramColor = validado[1:]
elif contparam == 3:
    paramHorizontal, paramFecha, paramColor = validado
elif len(argv) > 3:
        err(3)

if paramHorizontal == '-r':
    espacio = ' ' * (get_terminal_size().columns - 20)
else:
    espacio = ''

if len(paramFecha.split('-')) == 3:
    fecha = paramFecha
    paramFecha = paramFecha[:paramFecha.rfind('-')]
    resaltado = True
elif paramFecha == date.today().strftime('%Y-%m'):
    fecha = date.today().strftime('%Y-%m-%d')
    resaltado = True
else:
    fecha = fecha + '-34'
    resaltado = False
for nomDia in tuple(day_abbr):
    if not 'dias' in locals():
        dias = []
    dias.append(nomDia[:2].capitalize())
if paramFecha.count('/') == 0:
    tuplaAgnoMes = tuple(map(int, paramFecha.split('-')))
    if len(paramFecha.split('-')) > 1:
        mes = date.today().strftime("%B %Y").capitalize()
        mes = format(datetime.strftime((datetime.strptime(paramFecha, '%Y-%m')), '%B %Y').capitalize(), '^20')
        print (format(mes, alinear(paramHorizontal)))
        semanas = monthcalendar(*tuplaAgnoMes)

strMes = [dias.copy()]

c = 0
if len(paramFecha.split('-')) in (2, 3):
    strMes.extend(fMes(semanas))
    listSemana = [dias]
    listSemana.extend(semanas)
    for semana in printcal(strMes, listSemana):
        if c == 0:
            print ('\x1b[1m' + format(semana, alinear(paramHorizontal)) + '\x1b[0m')
            chrs = len(semana)
        else:
            dif = len(semana) - chrs
            print(format(semana, alinear(paramHorizontal, dif)))
        c += 1
elif len(paramFecha.split('-')) == 1:
    if paramFecha.count('/') == 2:
        paramFecha = paramFecha.replace('/', '-')
        resaltado = True
    elif not paramFecha.count('/') in (0, 2):
        err(5)
    if paramFecha.split('-')[0] == date.today().strftime('%Y'):
        paramFecha = date.today().strftime('%Y-%m-%d')
        resaltado = True
    if resaltado:
        sAno, sMes, sDia = tuple(map(int, paramFecha.split('-')))
        sMes -= 1
    else:
        sAno = int(paramFecha.split('-')[0])
    _1, _2, _3, _4, _6 = 20, 42, 64, 86, 130
    for i in range(1, 13):
        semanasMes = [dias.copy()]
        semanasMes.extend(monthcalendar(sAno, i))
        if not 'meses' in locals():
            meses = meses = []
        meses.append(semanasMes)
    for i in range(0, len(meses)):
        if not 'ano' in locals():
            ano = []
        ano.append(fMes(meses[i]))
        nombreMes = [format(datetime.strftime((datetime.strptime(str(i+1), '%m')), '%B').capitalize(), '^20')]
        ano[i].insert(0, nombreMes)
    if resaltado:
        for i in range(0, len(meses[sMes])):
            if sDia in meses[sMes][i]:
                ano[sMes][i+1][meses[sMes][i].index(sDia)] = fEsHoy(color=paramColor, ayuda=True)[2][0] + ano[sMes][i+1][meses[sMes][i].index(sDia)] + fEsHoy(color='0', ayuda=True)[2][0]
                sem = i
    if get_terminal_size().columns < 20:
        err(4)
    elif get_terminal_size().columns in range(20, 42):
        # Un mes por fila = 1
        formatAno = format(sAno, '^20')
        print (format(formatAno, alinear(paramHorizontal)))
        enter = True
        for mes in ano:
            for semana in mes:
                if ' '.join(semana).replace(' ', '').isalpha():
                    if enter:
                        print ()
                        enter = False
                    renglon = format(' '.join(semana), alinear(paramHorizontal, len(' '.join(semana)) - 20))
                    print (f'\x1b[0;1m{renglon}\x1b[0m')
                else:
                    enter = True
                    print (format(' '.join(semana), alinear(paramHorizontal, len(' '.join(semana)) - 20)))
        exit()
    elif get_terminal_size().columns in range(42, 64):
        # Dos meses por fila
        periodos = [
            igualarSemanas(ano, 0, 2),
            igualarSemanas(ano, 2, 4),
            igualarSemanas(ano, 4, 6),
            igualarSemanas(ano, 6, 8),
            igualarSemanas(ano, 8, 10),
            igualarSemanas(ano, 10, 12)
        ]
        cc = 42
    elif get_terminal_size().columns in range(64, 86):
        # Tres meses por fila = 3
        periodos = [
            igualarSemanas(ano, 0,3),
            igualarSemanas(ano, 3,6),
            igualarSemanas(ano, 6, 9),
            igualarSemanas(ano, 9, 12)
        ]
        cc =64
    elif get_terminal_size().columns in range(86, 130):
        # mesesxfila = 4
        periodos = [
            igualarSemanas(ano, 0, 4),
            igualarSemanas(ano, 4, 8),
            igualarSemanas(ano, 8,12)
        ]
        cc = 86
    elif get_terminal_size().columns > 129:
        # mesesxfila = 6
        periodos = [
            igualarSemanas(ano, 0, 6),
            igualarSemanas(ano, 6, 12)
        ]
        cc = 130
    mesdiv = 6
    for i in range(0, len(periodos)):
        for j in range(0, len(periodos[i])):
            for k in range(0, len(periodos[i][j])):
                periodos[i][j][k] = ' '.join(periodos[i][j][k])
    fila = []
    filas = []
    for periodo in periodos:
        nFila = 0
        while nFila < len(periodo[0]):
            for mes in range(0, len(periodo)):
                fila.append(periodo[mes][nFila])
            filas.append(fila.copy())
            fila.clear()
            nFila += 1
    formatAno = format(sAno, '^' + str(cc))
    print (format(formatAno, alinear(paramHorizontal)))
    enter = 0
    for _Fila in filas:
        if '  '.join(_Fila).replace(' ', '').isalpha():
            if enter == 0:
                print()
            renglon = format('  '.join(_Fila), alinear(paramHorizontal, len('  '.join(_Fila)) - cc))
            print(f'\x1b[0;1m{renglon}\x1b[0m')
            enter += 1
        else:
            enter = 0
            print(format('  '.join(_Fila), alinear(paramHorizontal, len('  '.join(_Fila)) - cc)))