import socket
import csv
import random


def goto_the_wanted_page(req):
    if 'category[]' in req:
        splited_request = req.split(' ')[1] # look like: "/?category[]=auto&category[]=trains"
        desired_category = splited_request.split('category[]=') # look like: "auto&category[]"
        desired_category = [category[:-1] for category in desired_category[1:-1]] + [desired_category[-1]]
        print(desired_category)
        HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
        for categories in data_from_csv:
            if any(category in categories[2:] for category in desired_category):
                url = categories[0]
                categories[1] = str(int(categories[1])-1)
                if categories[1] == '0':
                    data_from_csv_showed.append(data_from_csv.pop(data_from_csv.index(categories)))
                break
            elif not desired_category[0].isalpha():
                random_category = random.choice(data_from_csv)
                url = random_category[0]
                random_category[1] = str(int(random_category[1])-1)
                if random_category[1] == '0':
                    data_from_csv_showed.append(data_from_csv.pop(data_from_csv.index(random_category)))
                if len(data_from_csv) == 0:
                    return HDRS.encode('utf-8') + 'no more pictures :('.encode('utf-8')
                break
        else: 
            return HDRS.encode('utf-8') + 'not found'.encode('utf-8')
    elif any([link[0].split('/')[-1] in req for link in data_from_csv]):
        url = 'http://localhost:8080' + req.split(' ')[1]
    else: 
        return 'skip'
    html = f'''
    <!DOCTYPE html>
    <html>
    
    <head>
      <title>No title</title>
    </head>
    
    <body>
      <img src="{url}">
    </body>
    
    </html>'''
    return HDRS.encode('utf-8') + bytes(html, 'utf-8')


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost',8080))
    server.listen(4)
    while 1:
        print('Start...')
        client_socket, address = server.accept()
        request = client_socket.recv(1024).decode('utf-8')
        print(request)
        message = goto_the_wanted_page(request)
        if message == 'skip':
            continue
        client_socket.send(message)
    print('the end')


data_from_csv = []
data_from_csv_showed = []
with open("CSVFILENAME.csv", encoding='utf-8') as read_file:
    file_reader = csv.reader(read_file, delimiter=";")
    for row in file_reader:
        data_from_csv.append(row)
if __name__ == '__main__':
    start_server()
