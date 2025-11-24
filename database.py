# database.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

SQLALCHEMY_DATABASE_URL = "sqlite:///./kitchen.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модели базы данных
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    instructions = Column(Text)
    
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    menu_plans = relationship("MenuPlan", back_populates="recipe")

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    name = Column(String, index=True)
    amount = Column(Float)
    unit = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    amount = Column(Float)
    unit = Column(String)

class MenuPlan(Base):
    __tablename__ = "menu_plans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    servings = Column(Integer, default=1)
    meal_type = Column(String)

    recipe = relationship("Recipe", back_populates="menu_plans")

# Данные для инициализации
SAMPLE_RECIPES = [
    {
        "name": "Омлет классический",
        "description": "Простой и вкусный завтрак",
        "instructions": "1. Взбейте яйца с молоком и солью\n2. Разогрейте сковороду с маслом\n3. Вылейте смесь и жарьте 5-7 минут",
        "ingredients": [
            {"name": "яйцо", "amount": 3, "unit": "шт"},
            {"name": "молоко", "amount": 50, "unit": "мл"},
            {"name": "соль", "amount": 2, "unit": "г"},
            {"name": "масло растительное", "amount": 15, "unit": "мл"}
        ]
    },
    {
        "name": "Борщ",
        "description": "Традиционный украинский суп",
        "instructions": "1. Сварите бульон\n2. Обжарьте овощи\n3. Добавьте свеклу и капусту\n4. Варите 30 минут",
        "ingredients": [
            {"name": "говядина", "amount": 500, "unit": "г"},
            {"name": "свекла", "amount": 2, "unit": "шт"},
            {"name": "картофель", "amount": 4, "unit": "шт"},
            {"name": "капуста", "amount": 300, "unit": "г"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "томатная паста", "amount": 2, "unit": "ст.л"},
            {"name": "сметана", "amount": 100, "unit": "г"}
        ]
    },
    {
        "name": "Плов",
        "description": "Узбекское блюдо из риса и мяса",
        "instructions": "1. Обжарьте мясо с морковью и луком\n2. Добавьте рис и воду\n3. Томите под крышкой 40 минут",
        "ingredients": [
            {"name": "рис", "amount": 400, "unit": "г"},
            {"name": "баранина", "amount": 500, "unit": "г"},
            {"name": "морковь", "amount": 3, "unit": "шт"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "чеснок", "amount": 1, "unit": "головка"},
            {"name": "масло растительное", "amount": 100, "unit": "мл"},
            {"name": "зира", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Салат Цезарь",
        "description": "Классический салат с курицей",
        "instructions": "1. Обжарьте курицу\n2. Подсушите хлеб\n3. Смешайте все ингредиенты с соусом",
        "ingredients": [
            {"name": "куриное филе", "amount": 300, "unit": "г"},
            {"name": "салат айсберг", "amount": 1, "unit": "шт"},
            {"name": "помидоры черри", "amount": 200, "unit": "г"},
            {"name": "сыр пармезан", "amount": 100, "unit": "г"},
            {"name": "хлеб белый", "amount": 200, "unit": "г"},
            {"name": "соус цезарь", "amount": 100, "unit": "мл"}
        ]
    },
    {
        "name": "Гречневая каша",
        "description": "Простая и полезная каша",
        "instructions": "1. Промойте гречку\n2. Залейте водой 1:2\n3. Варите 15-20 минут",
        "ingredients": [
            {"name": "гречка", "amount": 200, "unit": "г"},
            {"name": "вода", "amount": 400, "unit": "мл"},
            {"name": "соль", "amount": 5, "unit": "г"},
            {"name": "масло сливочное", "amount": 30, "unit": "г"}
        ]
    },
    {
        "name": "Курица в духовке",
        "description": "Запеченная курица с картофелем",
        "instructions": "1. Натрите курицу специями\n2. Выложите на противень с картофелем\n3. Запекайте 60 минут при 180°C",
        "ingredients": [
            {"name": "курица", "amount": 1, "unit": "шт"},
            {"name": "картофель", "amount": 1, "unit": "кг"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "растительное масло", "amount": 50, "unit": "мл"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Блины",
        "description": "Тонкие блины на молоке",
        "instructions": "1. Смешайте все ингредиенты\n2. Дайте тесту постоять 30 минут\n3. Жарьте на сковороде с двух сторон",
        "ingredients": [
            {"name": "мука", "amount": 200, "unit": "г"},
            {"name": "молоко", "amount": 500, "unit": "мл"},
            {"name": "яйцо", "amount": 3, "unit": "шт"},
            {"name": "сахар", "amount": 30, "unit": "г"},
            {"name": "соль", "amount": 5, "unit": "г"},
            {"name": "масло растительное", "amount": 30, "unit": "мл"}
        ]
    },
    {
        "name": "Овощной салат",
        "description": "Свежий салат из сезонных овощей",
        "instructions": "1. Нарежьте все овощи\n2. Заправьте маслом и лимонным соком\n3. Посолите по вкусу",
        "ingredients": [
            {"name": "помидор", "amount": 3, "unit": "шт"},
            {"name": "огурец", "amount": 2, "unit": "шт"},
            {"name": "перец болгарский", "amount": 1, "unit": "шт"},
            {"name": "лук красный", "amount": 0.5, "unit": "шт"},
            {"name": "масло оливковое", "amount": 30, "unit": "мл"},
            {"name": "лимонный сок", "amount": 15, "unit": "мл"},
            {"name": "соль", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Картофельное пюре",
        "description": "Нежное пюре с молоком и маслом",
        "instructions": "1. Отварите картофель\n2. Слейте воду и разомните\n3. Добавьте теплое молоко и масло",
        "ingredients": [
            {"name": "картофель", "amount": 1, "unit": "кг"},
            {"name": "молоко", "amount": 200, "unit": "мл"},
            {"name": "масло сливочное", "amount": 50, "unit": "г"},
            {"name": "соль", "amount": 10, "unit": "г"}
        ]
    },
    {
        "name": "Жаркое",
        "description": "Мясо с овощами в горшочках",
        "instructions": "1. Обжарьте мясо и лук\n2. Сложите в горшочки с овощами\n3. Тушите 1.5 часа в духовке",
        "ingredients": [
            {"name": "свинина", "amount": 500, "unit": "г"},
            {"name": "картофель", "amount": 600, "unit": "г"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "сметана", "amount": 200, "unit": "г"},
            {"name": "чеснок", "amount": 3, "unit": "зубчик"}
        ]
    },
    {
        "name": "Суп куриный",
        "description": "Легкий куриный суп с вермишелью",
        "instructions": "1. Сварите куриный бульон\n2. Добавьте овощи и вермишель\n3. Варите до готовности",
        "ingredients": [
            {"name": "курица", "amount": 400, "unit": "г"},
            {"name": "вермишель", "amount": 100, "unit": "г"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "картофель", "amount": 3, "unit": "шт"},
            {"name": "соль", "amount": 10, "unit": "г"}
        ]
    },
    {
        "name": "Голубцы",
        "description": "Фарш в капустных листьях",
        "instructions": "1. Отварите капустные листья\n2. Заверните фарш\n3. Тушите в томатном соусе 40 минут",
        "ingredients": [
            {"name": "капуста белокочанная", "amount": 1, "unit": "шт"},
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "рис", "amount": 100, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "томатная паста", "amount": 3, "unit": "ст.л"},
            {"name": "сметана", "amount": 200, "unit": "г"}
        ]
    },
    {
        "name": "Шарлотка",
        "description": "Яблочный пирог",
        "instructions": "1. Взбейте яйца с сахаром\n2. Добавьте муку и яблоки\n3. Выпекайте 40 минут при 180°C",
        "ingredients": [
            {"name": "яблоки", "amount": 4, "unit": "шт"},
            {"name": "яйцо", "amount": 4, "unit": "шт"},
            {"name": "мука", "amount": 200, "unit": "г"},
            {"name": "сахар", "amount": 200, "unit": "г"},
            {"name": "разрыхлитель", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Котлеты",
        "description": "Домашние котлеты из фарша",
        "instructions": "1. Смешайте фарш с луком и хлебом\n2. Сформируйте котлеты\n3. Обжарьте с двух сторон",
        "ingredients": [
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "хлеб белый", "amount": 100, "unit": "г"},
            {"name": "молоко", "amount": 100, "unit": "мл"},
            {"name": "яйцо", "amount": 1, "unit": "шт"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Рагу овощное",
        "description": "Тушеные овощи",
        "instructions": "1. Обжарьте лук и морковь\n2. Добавьте остальные овощи\n3. Тушите 30 минут",
        "ingredients": [
            {"name": "картофель", "amount": 400, "unit": "г"},
            {"name": "капуста", "amount": 300, "unit": "г"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "перец болгарский", "amount": 2, "unit": "шт"},
            {"name": "томатная паста", "amount": 2, "unit": "ст.л"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Греческий салат",
        "description": "Средиземноморский салат",
        "instructions": "1. Нарежьте овощи крупно\n2. Добавьте сыр и оливки\n3. Заправьте оливковым маслом",
        "ingredients": [
            {"name": "помидор", "amount": 3, "unit": "шт"},
            {"name": "огурец", "amount": 2, "unit": "шт"},
            {"name": "перец болгарский", "amount": 1, "unit": "шт"},
            {"name": "лук красный", "amount": 0.5, "unit": "шт"},
            {"name": "сыр фета", "amount": 200, "unit": "г"},
            {"name": "маслины", "amount": 100, "unit": "г"},
            {"name": "масло оливковое", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Паста Карбонара",
        "description": "Итальянская паста с беконом",
        "instructions": "1. Отварите пасту\n2. Обжарьте бекон\n3. Смешайте с яично-сырной смесью",
        "ingredients": [
            {"name": "паста", "amount": 400, "unit": "г"},
            {"name": "бекон", "amount": 200, "unit": "г"},
            {"name": "яйцо", "amount": 3, "unit": "шт"},
            {"name": "сыр пармезан", "amount": 100, "unit": "г"},
            {"name": "сливки", "amount": 200, "unit": "мл"},
            {"name": "чеснок", "amount": 2, "unit": "зубчик"}
        ]
    },
    {
        "name": "Сырники",
        "description": "Творожные оладьи",
        "instructions": "1. Смешайте творог с яйцами и мукой\n2. Сформируйте сырники\n3. Обжарьте до золотистой корочки",
        "ingredients": [
            {"name": "творог", "amount": 500, "unit": "г"},
            {"name": "яйцо", "amount": 2, "unit": "шт"},
            {"name": "мука", "amount": 100, "unit": "г"},
            {"name": "сахар", "amount": 50, "unit": "г"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Овсяная каша",
        "description": "Полезный завтрак",
        "instructions": "1. Доведите молоко до кипения\n2. Добавьте овсянку\n3. Варите 5-7 минут",
        "ingredients": [
            {"name": "овсяные хлопья", "amount": 100, "unit": "г"},
            {"name": "молоко", "amount": 300, "unit": "мл"},
            {"name": "сахар", "amount": 20, "unit": "г"},
            {"name": "масло сливочное", "amount": 20, "unit": "г"}
        ]
    },
    {
        "name": "Щи",
        "description": "Русский капустный суп",
        "instructions": "1. Сварите мясной бульон\n2. Добавьте капусту и овощи\n3. Варите 25 минут",
        "ingredients": [
            {"name": "говядина", "amount": 400, "unit": "г"},
            {"name": "капуста", "amount": 300, "unit": "г"},
            {"name": "картофель", "amount": 3, "unit": "шт"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "томатная паста", "amount": 2, "unit": "ст.л"},
            {"name": "сметана", "amount": 100, "unit": "г"}
        ]
    },
    {
        "name": "Пельмени",
        "description": "Домашние пельмени",
        "instructions": "1. Замесите тесто\n2. Приготовьте фарш\n3. Слепите пельмени",
        "ingredients": [
            {"name": "мука", "amount": 500, "unit": "г"},
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "яйцо", "amount": 1, "unit": "шт"},
            {"name": "вода", "amount": 200, "unit": "мл"},
            {"name": "соль", "amount": 10, "unit": "г"}
        ]
    },
    {
        "name": "Жареная картошка",
        "description": "Простое и сытное блюдо",
        "instructions": "1. Нарежьте картофель\n2. Обжарьте на сковороде до готовности\n3. Добавьте лук в конце",
        "ingredients": [
            {"name": "картофель", "amount": 1, "unit": "кг"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Солянка",
        "description": "Густой мясной суп",
        "instructions": "1. Сварите бульон\n2. Добавьте различные виды мяса\n3. Положите огурцы и оливки",
        "ingredients": [
            {"name": "говядина", "amount": 300, "unit": "г"},
            {"name": "колбаса", "amount": 200, "unit": "г"},
            {"name": "огурцы соленые", "amount": 3, "unit": "шт"},
            {"name": "оливки", "amount": 100, "unit": "г"},
            {"name": "томатная паста", "amount": 2, "unit": "ст.л"},
            {"name": "лимон", "amount": 0.5, "unit": "шт"}
        ]
    },
    {
        "name": "Лазанья",
        "description": "Итальянская запеканка",
        "instructions": "1. Приготовьте мясной соус\n2. Соберите слои\n3. Запекайте 40 минут",
        "ingredients": [
            {"name": "листы лазаньи", "amount": 250, "unit": "г"},
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "сыр моцарелла", "amount": 300, "unit": "г"},
            {"name": "томатный соус", "amount": 500, "unit": "мл"},
            {"name": "молоко", "amount": 500, "unit": "мл"},
            {"name": "мука", "amount": 50, "unit": "г"},
            {"name": "масло сливочное", "amount": 50, "unit": "г"}
        ]
    },
    {
        "name": "Пирожки с капустой",
        "description": "Жареные пирожки",
        "instructions": "1. Приготовьте тесто\n2. Сделайте начинку из капусты\n3. Обжарьте пирожки",
        "ingredients": [
            {"name": "мука", "amount": 500, "unit": "г"},
            {"name": "капуста", "amount": 500, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "яйцо", "amount": 2, "unit": "шт"},
            {"name": "дрожжи", "amount": 10, "unit": "г"},
            {"name": "масло растительное", "amount": 100, "unit": "мл"}
        ]
    },
    {
        "name": "Куриные крылышки",
        "description": "Запеченные крылышки в соусе",
        "instructions": "1. Замаринуйте крылышки\n2. Выложите на противень\n3. Запекайте 40 минут",
        "ingredients": [
            {"name": "куриные крылья", "amount": 1, "unit": "кг"},
            {"name": "соус соевый", "amount": 50, "unit": "мл"},
            {"name": "мед", "amount": 30, "unit": "мл"},
            {"name": "чеснок", "amount": 4, "unit": "зубчик"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Манная каша",
        "description": "Нежная каша на молоке",
        "instructions": "1. Доведите молоко до кипения\n2. Постепенно всыпьте манку\n3. Варите 5 минут",
        "ingredients": [
            {"name": "манная крупа", "amount": 100, "unit": "г"},
            {"name": "молоко", "amount": 500, "unit": "мл"},
            {"name": "сахар", "amount": 30, "unit": "г"},
            {"name": "масло сливочное", "amount": 20, "unit": "г"}
        ]
    },
    {
        "name": "Стейк из говядины",
        "description": "Сочный стейк средней прожарки",
        "instructions": "1. Разогрейте сковороду\n2. Обжарьте стейк по 3-4 минуты с каждой стороны\n3. Дайте отдохнуть 5 минут",
        "ingredients": [
            {"name": "говяжий стейк", "amount": 300, "unit": "г"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"},
            {"name": "масло растительное", "amount": 20, "unit": "мл"},
            {"name": "розмарин", "amount": 2, "unit": "веточка"}
        ]
    },
    {
        "name": "Винегрет",
        "description": "Овощной салат",
        "instructions": "1. Отварите овощи\n2. Нарежьте кубиками\n3. Заправьте маслом",
        "ingredients": [
            {"name": "свекла", "amount": 2, "unit": "шт"},
            {"name": "картофель", "amount": 3, "unit": "шт"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "огурцы соленые", "amount": 3, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Куриный суп с лапшой",
        "description": "Ароматный суп с курицей",
        "instructions": "1. Сварите куриный бульон\n2. Добавьте овощи и лапшу\n3. Варите 10 минут",
        "ingredients": [
            {"name": "курица", "amount": 400, "unit": "г"},
            {"name": "лапша", "amount": 150, "unit": "г"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "картофель", "amount": 3, "unit": "шт"},
            {"name": "зелень", "amount": 20, "unit": "г"}
        ]
    },
    {
        "name": "Фаршированный перец",
        "description": "Перцы с мясной начинкой",
        "instructions": "1. Приготовьте фарш\n2. Нафаршируйте перцы\n3. Тушите в томатном соусе 40 минут",
        "ingredients": [
            {"name": "перец болгарский", "amount": 6, "unit": "шт"},
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "рис", "amount": 100, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "томатная паста", "amount": 3, "unit": "ст.л"},
            {"name": "сметана", "amount": 200, "unit": "г"}
        ]
    },
    {
        "name": "Творожная запеканка",
        "description": "Нежная запеканка в духовке",
        "instructions": "1. Смешайте творог с яйцами и манкой\n2. Выложите в форму\n3. Запекайте 40 минут",
        "ingredients": [
            {"name": "творог", "amount": 500, "unit": "г"},
            {"name": "яйцо", "amount": 3, "unit": "шт"},
            {"name": "манная крупа", "amount": 50, "unit": "г"},
            {"name": "сахар", "amount": 100, "unit": "г"},
            {"name": "сметана", "amount": 100, "unit": "г"}
        ]
    },
    {
        "name": "Гуляш",
        "description": "Мясо в густом соусе",
        "instructions": "1. Обжарьте мясо\n2. Добавьте овощи и томат\n3. Тушите 1.5 часа",
        "ingredients": [
            {"name": "говядина", "amount": 600, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "томатная паста", "amount": 3, "unit": "ст.л"},
            {"name": "мука", "amount": 20, "unit": "г"},
            {"name": "сметана", "amount": 100, "unit": "г"}
        ]
    },
    {
        "name": "Рисовая каша",
        "description": "Молочная рисовая каша",
        "instructions": "1. Промойте рис\n2. Варите в молоке 20 минут\n3. Добавьте масло и сахар",
        "ingredients": [
            {"name": "рис", "amount": 200, "unit": "г"},
            {"name": "молоко", "amount": 600, "unit": "мл"},
            {"name": "сахар", "amount": 40, "unit": "г"},
            {"name": "масло сливочное", "amount": 30, "unit": "г"},
            {"name": "соль", "amount": 2, "unit": "г"}
        ]
    },
    {
        "name": "Суп-пюре из тыквы",
        "description": "Нежный крем-суп",
        "instructions": "1. Запеките тыкву\n2. Взбейте с бульоном\n3. Добавьте сливки",
        "ingredients": [
            {"name": "тыква", "amount": 800, "unit": "г"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "сливки", "amount": 200, "unit": "мл"},
            {"name": "бульон куриный", "amount": 500, "unit": "мл"},
            {"name": "имбирь", "amount": 10, "unit": "г"}
        ]
    },
    {
        "name": "Куриные наггетсы",
        "description": "Хрустящие кусочки курицы",
        "instructions": "1. Нарежьте курицу\n2. Обваляйте в панировке\n3. Обжарьте во фритюре",
        "ingredients": [
            {"name": "куриное филе", "amount": 500, "unit": "г"},
            {"name": "мука", "amount": 100, "unit": "г"},
            {"name": "яйцо", "amount": 2, "unit": "шт"},
            {"name": "сухари панировочные", "amount": 150, "unit": "г"},
            {"name": "масло растительное", "amount": 300, "unit": "мл"}
        ]
    },
    {
        "name": "Салат Оливье",
        "description": "Классический праздничный салат",
        "instructions": "1. Отварите овощи и яйца\n2. Нарежьте все ингредиенты\n3. Заправьте майонезом",
        "ingredients": [
            {"name": "картофель", "amount": 4, "unit": "шт"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "яйцо", "amount": 4, "unit": "шт"},
            {"name": "огурцы соленые", "amount": 4, "unit": "шт"},
            {"name": "колбаса вареная", "amount": 300, "unit": "г"},
            {"name": "горошек консервированный", "amount": 200, "unit": "г"},
            {"name": "майонез", "amount": 150, "unit": "г"}
        ]
    },
    {
        "name": "Чечевичный суп",
        "description": "Питательный суп из чечевицы",
        "instructions": "1. Обжарьте овощи\n2. Добавьте чечевицу и бульон\n3. Варите 30 минут",
        "ingredients": [
            {"name": "чечевица", "amount": 200, "unit": "г"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "картофель", "amount": 2, "unit": "шт"},
            {"name": "бульон куриный", "amount": 1, "unit": "л"},
            {"name": "чеснок", "amount": 2, "unit": "зубчик"}
        ]
    },
    {
        "name": "Куриные грудки в сливочном соусе",
        "description": "Нежное куриное филе в соусе",
        "instructions": "1. Обжарьте курицу\n2. Приготовьте сливочный соус\n3. Тушите 15 минут",
        "ingredients": [
            {"name": "куриное филе", "amount": 500, "unit": "г"},
            {"name": "сливки", "amount": 300, "unit": "мл"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "чеснок", "amount": 3, "unit": "зубчик"},
            {"name": "сыр пармезан", "amount": 50, "unit": "г"}
        ]
    },
    {
        "name": "Картофель по-деревенски",
        "description": "Запеченный картофель со специями",
        "instructions": "1. Нарежьте картофель\n2. Обваляйте в специях и масле\n3. Запекайте 40 минут",
        "ingredients": [
            {"name": "картофель", "amount": 1, "unit": "кг"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"},
            {"name": "паприка", "amount": 10, "unit": "г"},
            {"name": "чеснок", "amount": 4, "unit": "зубчик"},
            {"name": "соль", "amount": 10, "unit": "г"}
        ]
    },
    {
        "name": "Спагетти Болоньезе",
        "description": "Паста с мясным соусом",
        "instructions": "1. Приготовьте мясной соус\n2. Отварите спагетти\n3. Подавайте с соусом",
        "ingredients": [
            {"name": "спагетти", "amount": 400, "unit": "г"},
            {"name": "фарш мясной", "amount": 500, "unit": "г"},
            {"name": "томатный соус", "amount": 500, "unit": "мл"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "сельдерей", "amount": 1, "unit": "стебель"},
            {"name": "сыр пармезан", "amount": 100, "unit": "г"}
        ]
    },
    {
        "name": "Куриные окорочка",
        "description": "Запеченные куриные ножки",
        "instructions": "1. Натрите окорочка специями\n2. Выложите на противень\n3. Запекайте 50 минут",
        "ingredients": [
            {"name": "куриные окорочка", "amount": 4, "unit": "шт"},
            {"name": "соль", "amount": 10, "unit": "г"},
            {"name": "перец", "amount": 5, "unit": "г"},
            {"name": "чеснок", "amount": 4, "unit": "зубчик"},
            {"name": "масло растительное", "amount": 30, "unit": "мл"}
        ]
    },
    {
        "name": "Гренки",
        "description": "Жареные хлебные ломтики",
        "instructions": "1. Нарежьте хлеб\n2. Обжарьте на сковороде с маслом\n3. Посолите по вкусу",
        "ingredients": [
            {"name": "хлеб белый", "amount": 300, "unit": "г"},
            {"name": "масло сливочное", "amount": 50, "unit": "г"},
            {"name": "чеснок", "amount": 2, "unit": "зубчик"},
            {"name": "соль", "amount": 5, "unit": "г"}
        ]
    },
    {
        "name": "Фасоль в томатном соусе",
        "description": "Тушеная фасоль с овощами",
        "instructions": "1. Замочите фасоль\n2. Отварите до готовности\n3. Потушите с томатом и овощами",
        "ingredients": [
            {"name": "фасоль белая", "amount": 300, "unit": "г"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "томатная паста", "amount": 3, "unit": "ст.л"},
            {"name": "масло растительное", "amount": 30, "unit": "мл"}
        ]
    },
    {
        "name": "Куриный рулет",
        "description": "Рулет из куриного филе с начинкой",
        "instructions": "1. Отбейте куриное филе\n2. Выложите начинку\n3. Запекайте 40 минут",
        "ingredients": [
            {"name": "куриное филе", "amount": 500, "unit": "г"},
            {"name": "сыр", "amount": 200, "unit": "г"},
            {"name": "грибы", "amount": 200, "unit": "г"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "чеснок", "amount": 2, "unit": "зубчик"}
        ]
    },
    {
        "name": "Капуста тушеная",
        "description": "Тушеная капуста с овощами",
        "instructions": "1. Нарежьте капусту\n2. Обжарьте лук и морковь\n3. Тушите 40 минут",
        "ingredients": [
            {"name": "капуста белокочанная", "amount": 1, "unit": "кг"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "морковь", "amount": 2, "unit": "шт"},
            {"name": "томатная паста", "amount": 2, "unit": "ст.л"},
            {"name": "масло растительное", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Яичница",
        "description": "Жареные яйца",
        "instructions": "1. Разогрейте сковороду\n2. Разбейте яйца\n3. Жарьте 5-7 минут",
        "ingredients": [
            {"name": "яйцо", "amount": 3, "unit": "шт"},
            {"name": "соль", "amount": 5, "unit": "г"},
            {"name": "масло растительное", "amount": 15, "unit": "мл"}
        ]
    },
    {
        "name": "Суп с фрикадельками",
        "description": "Легкий суп с мясными шариками",
        "instructions": "1. Приготовьте фрикадельки\n2. Сварите бульон\n3. Добавьте овощи и фрикадельки",
        "ingredients": [
            {"name": "фарш мясной", "amount": 300, "unit": "г"},
            {"name": "картофель", "amount": 3, "unit": "шт"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "рис", "amount": 50, "unit": "г"}
        ]
    },
    {
        "name": "Запеченные овощи",
        "description": "Смесь овощей в духовке",
        "instructions": "1. Нарежьте овощи\n2. Смешайте с маслом и специями\n3. Запекайте 35 минут",
        "ingredients": [
            {"name": "кабачок", "amount": 1, "unit": "шт"},
            {"name": "баклажан", "amount": 1, "unit": "шт"},
            {"name": "перец болгарский", "amount": 2, "unit": "шт"},
            {"name": "помидор", "amount": 2, "unit": "шт"},
            {"name": "лук", "amount": 1, "unit": "шт"},
            {"name": "масло оливковое", "amount": 50, "unit": "мл"}
        ]
    },
    {
        "name": "Куриные сердечки",
        "description": "Тушеные куриные сердечки",
        "instructions": "1. Обжарьте лук\n2. Добавьте сердечки\n3. Тушите 40 минут",
        "ingredients": [
            {"name": "куриные сердечки", "amount": 500, "unit": "г"},
            {"name": "лук", "amount": 2, "unit": "шт"},
            {"name": "морковь", "amount": 1, "unit": "шт"},
            {"name": "сметана", "amount": 200, "unit": "г"}
        ]
    },
    {
        "name": "Молочный коктейль",
        "description": "Освежающий молочный напиток",
        "instructions": "1. Смешайте все ингредиенты в блендере\n2. Взбейте до однородности\n3. Подавайте охлажденным",
        "ingredients": [
            {"name": "молоко", "amount": 400, "unit": "мл"},
            {"name": "мороженое", "amount": 200, "unit": "г"},
            {"name": "сахар", "amount": 30, "unit": "г"}
        ]
    }
]

INITIAL_INVENTORY = [
    {"name": "яйцо", "amount": 10, "unit": "шт"},
    {"name": "молоко", "amount": 1, "unit": "л"},
    {"name": "мука", "amount": 2, "unit": "кг"},
    {"name": "сахар", "amount": 1, "unit": "кг"},
    {"name": "соль", "amount": 500, "unit": "г"},
    {"name": "масло растительное", "amount": 500, "unit": "мл"},
    {"name": "картофель", "amount": 3, "unit": "кг"},
    {"name": "лук", "amount": 1, "unit": "кг"},
    {"name": "морковь", "amount": 1, "unit": "кг"},
    {"name": "рис", "amount": 1, "unit": "кг"},
    {"name": "гречка", "amount": 1, "unit": "кг"},
    {"name": "макароны", "amount": 1, "unit": "кг"},
    {"name": "куриное филе", "amount": 1, "unit": "кг"},
    {"name": "фарш мясной", "amount": 1, "unit": "кг"},
    {"name": "сыр", "amount": 500, "unit": "г"},
    {"name": "сметана", "amount": 400, "unit": "г"},
    {"name": "томатная паста", "amount": 200, "unit": "г"},
    {"name": "чеснок", "amount": 100, "unit": "г"},
    {"name": "перец болгарский", "amount": 500, "unit": "г"},
    {"name": "помидор", "amount": 1, "unit": "кг"},
    {"name": "огурец", "amount": 500, "unit": "г"},
    {"name": "капуста", "amount": 1, "unit": "кг"},
    {"name": "масло сливочное", "amount": 200, "unit": "г"},
    {"name": "хлеб", "amount": 1, "unit": "шт"}
]

def init_database():
    """Инициализация базы данных с примерами рецептов и запасов"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже рецепты в базе
        existing_recipes = db.query(Recipe).count()
        if existing_recipes == 0:
            print("Инициализация базы данных с примерами рецептов...")
            
            # Добавляем рецепты
            for recipe_data in SAMPLE_RECIPES:
                recipe = Recipe(
                    name=recipe_data["name"],
                    description=recipe_data["description"],
                    instructions=recipe_data["instructions"]
                )
                db.add(recipe)
                db.flush()  # Получаем ID
                
                for ing in recipe_data["ingredients"]:
                    ingredient = RecipeIngredient(
                        recipe_id=recipe.id,
                        name=ing["name"],
                        amount=ing["amount"],
                        unit=ing["unit"]
                    )
                    db.add(ingredient)
            
            # Добавляем начальные запасы - проверяем уникальность
            existing_inventory = db.query(InventoryItem).all()
            existing_names = {item.name for item in existing_inventory}
            
            for item in INITIAL_INVENTORY:
                if item["name"] not in existing_names:
                    inventory_item = InventoryItem(**item)
                    db.add(inventory_item)
                    existing_names.add(item["name"])
            
            db.commit()
            print(f"Добавлено {len(SAMPLE_RECIPES)} рецептов и {len(INITIAL_INVENTORY)} позиций в запасы")
        else:
            print(f"В базе уже есть {existing_recipes} рецептов, инициализация не требуется")
            
    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        db.close()

# Автоматическая инициализация при импорте
init_database()