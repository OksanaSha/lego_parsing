## Парсинг через API
#### Почему API:
Скрапинг занял бы в разы больше времени из-за обфусцированных названий в HTML и отсутсвии тэгов.
#### Почему отсутствуют классы:
Небольшая программа, поэтому я выбрала функциональный стиль.
#### Выходные данные:
Два файла - по Москве и Питеру. Т.к. по заданию в csv-файле нет колонки **'city'**
#### Как запустить:
Для записи новых файлов удалить старые или изменить названия при запуске  main.py
- Docker<br>
`docker build -t lego_parsing .`<br>
`docker run lego_parsing`<br>


- Python<br>
`python==3.9`<br>
`pip install --upgrade pip`<br>
`pip install -r requirements.txt`<br>
`python main.py`

#### Примечание:
В коде использован **time.sleep** перед отправкой нового запроса. Это сделано, чтобы капризный API Детского мира не забанил как бота.
