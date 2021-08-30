## Задание1 (Вариант1).

Разработать сайт для заказа ингредиентов по рецептам блюд.
На сайте должен присутствовать каталог/список всех блюд.
Для блюда должна быть возможность указать входящие в него ингредиенты и количество каждого ингредиента(просто числом).
На странице каждого из блюд отобразить список ингредиентов входяших в блюдо
и в каком количестве он входит в блюдо,  а также кнопка оформления заказа _"Оформить заказ"_.
После нажатия на кнопку _"Оформить заказ"_ пользователю отображается форма/список всех
ингредиентов блюда и возможность ввода количества каждого из них
(можно заказать количество отличное от того что указано в рецепте).

Сущности:
```
- Dish(блюдо)
- Ingredient(ингредиент)
- Order(заказ)
```
В блюде может быть много ингредиентов,
один ингредиент может быть в нескольких блюдах.
В заказе может быть много ингредиентов,
каждый ингредиент можно заказать в определенном
количестве.

## How to run
1. Copy `.env` file from `/examples` folder to root folder:
    ```
    cp /examples/.env .env
    ```
2. Set following environment variables:
   - SECRET_KEY
   - DEFAULT_DATABASE_URL
3. Apply all migrations:
    ```
    python manage.py migrate
    ```
4. Run server:
    ```
    python manage.py runserver
    ```