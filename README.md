# Cервис просмотра контента
Запуск ```python main.py```

Доступен по адресу: ```localhost:8080``` 

Конфигурационный файл   ```CSVFILENAME.csv```

Доступные категории: 

```flight``` ```airlplane``` ```show``` ```britain``` ```bennyhill``` ```sketches``` ```tv``` ```games``` ```minecraft``` ```blocks``` ```sandbox``` ```onlycategory``` ```test```

Примеры запроса:

```
http://localhost:8080/

http://localhost:8080/?category[]=show&category[]=test

http://localhost:8080/?category[]=blocks
