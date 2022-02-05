import socket
import csv
import random


HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'.encode('utf-8')


def fill_data():
    """ 
    Считывает csv файл и возвращает список из строк csv файла и пустой список, 
    хранящий строки картинок, с нулевым числом необходимых показов соотвестсвенно

    Returns:
        [list]: список строк файла и список строк картинок, не нуждающихся в показе
    """    
    data = []
    data_showed = []
    with open("CSVFILENAME.csv", encoding='utf-8') as read_file:
        file_reader = csv.reader(read_file, delimiter=";")
        for row in file_reader:
            data.append(row)
    return data, data_showed


def goto_wanted_page(request, data, data_showed):
    """
    Получает GET запрос, списки строк конфигурационного файла
    Возвращает соответсвующий контент или 'skip' для начала следующей итерации, 
    обновлённые списки строк конфигурационного файла.

    Args:
        request (str): GET запрос
        data ([list]): список строк конфигурационного файла, доступных к показу
        data_showed ([list]): список строк конфигурационного файла, с нулевым количеством показов

    Returns:
        [bytes]: контент соответсвующий запросу
        or
        [str]: 'skip'

        [list]: обновлённый список строк конфигурационного файла, доступных к показу
        [list]: обновлённый список строк конфигурационного файла, с нулевым количеством показов
    """
    print('gtwp')     
    if len(data) == 0:
        # в случае, если все картинки были показаны
        return HDRS + 'no more pictures :('.encode('utf-8'), data, data_showed

    splited_request = request.split(' ')[1] # look like: "/?category[]=auto&category[]=trains" or "/" or "static/image4.jpg" 
    if splited_request == '/':
        print('SR')
        # обработка пустого запроса
        return empty_request_received(data, data_showed) 
    elif 'category[]=' in splited_request:
        print('DR')
        # обработка прямого запроса
        return direct_request_received(splited_request, data, data_showed)
    elif any([link[0].split('/')[-1] in splited_request for link in data]):
        print('ER')
        # в случае получения ссыки
        url = 'http://localhost:8080' + splited_request
        message = wrap_in__html(url)
        return message, data, data_showed
    else:
        print('skip') 
        return 'skip', data, data_showed


def empty_request_received(data, data_showed):
    """
    Обрабатывает пустой запрос.
    Считает количество оставшихся показов для запроса.
    Возвращает случайный контент, 
    обновлённые списки строк конфигурационного файла.

    Args:
        data ([list]): список строк конфигурационного файла, доступных к показу
        data_showed ([list]): список строк конфигурационного файла, с нулевым количеством показов

    Returns:
        [bytes]: html обёртка с картинкой из случайной категории
        [list]: обновлённый список строк конфигурационного файла, доступных к показу
        [list]: обновлённый список строк конфигурационного файла, с нулевым количеством показов
    """   
    random_category = random.choice(data)
    url = random_category[0]
    random_category[1] = str(int(random_category[1])-1)
    if random_category[1] == '0':
        data_showed.append(data.pop(data.index(random_category)))
    message = wrap_in__html(url)
    return message, data, data_showed


def direct_request_received(splited_request, data, data_showed):  
    """ 
    Обрабатывает прямой запрос категорий.
    Считает количество оставшихся показов для запроса.
    Возвращает требуемый контент или 'not found' в случае невозможности показать категорию, 
    обновлённые списки строк конфигурационного файла.


    Args:
        splited_request (str): строка с запрашиваемыми категориями
        data ([list]): список строк конфигурационного файла, доступных к показу
        data_showed ([list]): список строк конфигурационного файла, с нулевым количеством показов

    Returns:
        [bytes]: html обёртка с картинкой из требуемой категории
        [list]: обновлённый список строк конфигурационного файла, доступных к показу
        [list]: обновлённый список строк конфигурационного файла, с нулевым количеством показов
    """    
    desired_category = splited_request.split('category[]=') # look like: ['/?', 'auto&', 'cats&', 'trains']
    desired_category = [category[:-1] for category in desired_category[1:-1]] + [desired_category[-1]]
    # look like: ['auto', 'cats'] + ['trains']
    print(desired_category)
    for categories in data:
        if any(category in categories[2:] for category in desired_category):
            url = categories[0]
            categories[1] = str(int(categories[1])-1)
            if categories[1] == '0':
                data_showed.append(data.pop(data.index(categories)))
            message = wrap_in__html(url)
            return message, data, data_showed
    else: 
        return HDRS + 'not found'.encode('utf-8'), data, data_showed


def wrap_in__html(url):
    """ 
    Получает url необходимой к показу картинки и вставляет её в html шаблон

    Args:
        url (str): url запрашиваемой картинки

    Returns:
        [bytes]: Необходимая html обёртка
    """    
    print(url)
    html = f'''
    <!DOCTYPE html>
    <html>
    
    <head>
      <title>Картиночный сервис</title>
    </head>
    
    <body>
      <img src="{url}" align="center" height="600">
    </body>
    
    </html>'''
    return HDRS + html.encode('utf-8')  


def start_server():
    """ 
    Запускает работу сервера
    """    
    data, data_showed = fill_data()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost',8080))
    server.listen(4)
    while 1:
        print('\nStart...')
        client_socket, address = server.accept()
        request = client_socket.recv(1024).decode('utf-8')
        if len(request) == 0:
            continue
        message, data, data_showed = goto_wanted_page(request, data, data_showed)
        if message == 'skip':
            continue
        client_socket.send(message)
