# REST API по работе с меню ресторана

## Запуск приложения

Для запуска проекта необходимо выполнить следующие шаги:

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/RaraykinValery/menu_app.git
```
3. Перейдите в папку с проектом:

```bash
cd menu_app
```

4. Запустите приложение с помощью Docker Compose:

```bash
docker-compose up -d
```
Опция -d запускает контейнеры в фоновом режиме.

После успешного запуска, приложение будет доступно по адресу http://127.0.0.1:8000 и его можно тестировать через Postman.

5. Остановка проекта

Для остановки приложения выполните следующую команду в корневой директории проекта:

```bash
docker-compose down
```

## Запуск тестов

Чтобы запустить тесты нужно сделать файл run_tests.sh исполняемым:

```bash
sudo chmod +x run_tests.sh
```

И запустить его:

```bash
./run_tests.sh
```

## ORM запрос

ORM запрос для вывода количества подменю и блюд для Меню из пункта 3 находится по пути:
`menu_app/app/operations.py` в функции get_menus_with_submenus_and_dishes_counts.
