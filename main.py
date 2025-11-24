from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta
from pydantic import BaseModel

from database import get_db, Recipe, RecipeIngredient, InventoryItem, MenuPlan

app = FastAPI(title="Кухонный Помощник")

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Pydantic схемы
class IngredientBase(BaseModel):
    name: str
    amount: float
    unit: str

class RecipeIngredientCreate(IngredientBase):
    pass

class RecipeCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    instructions: str
    ingredients: List[RecipeIngredientCreate]

class RecipeResponse(RecipeCreate):
    id: int
    class Config:
        orm_mode = True

class InventoryCreate(IngredientBase):
    pass

class InventoryResponse(InventoryCreate):
    id: int
    class Config:
        orm_mode = True

class MenuCreate(BaseModel):
    date: date
    recipe_id: int
    servings: int
    meal_type: str

class MenuResponse(MenuCreate):
    id: int
    recipe: RecipeResponse
    class Config:
        orm_mode = True

# Главная страница
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API эндпоинты (остаются без изменений)
@app.get("/api/recipes", response_model=List[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()

@app.post("/api/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = Recipe(name=recipe.name, description=recipe.description, instructions=recipe.instructions)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    
    for ing in recipe.ingredients:
        db_ing = RecipeIngredient(recipe_id=db_recipe.id, name=ing.name.lower().strip(), amount=ing.amount, unit=ing.unit)
        db.add(db_ing)
    
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/api/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    return {"ok": True}

@app.get("/api/inventory", response_model=List[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):
    return db.query(InventoryItem).all()

@app.post("/api/inventory", response_model=InventoryResponse)
def add_inventory(item: InventoryCreate, db: Session = Depends(get_db)):
    if not item.name:
        raise HTTPException(status_code=400, detail="Название продукта не может быть пустым")
    
    normalized_name = item.name.lower().strip()
    
    existing = db.query(InventoryItem).filter(InventoryItem.name == normalized_name).first()
    if existing:
        existing.amount += item.amount
        db.commit()
        db.refresh(existing)
        return existing
    else:
        new_item = InventoryItem(name=normalized_name, amount=item.amount, unit=item.unit)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@app.delete("/api/inventory/{item_id}")
def delete_inventory(item_id: int, db: Session = Depends(get_db)):
    db.query(InventoryItem).filter(InventoryItem.id == item_id).delete()
    db.commit()
    return {"ok": True}

@app.get("/api/menu", response_model=List[MenuResponse])
def get_menu(start_date: Optional[date] = None, end_date: Optional[date] = None, db: Session = Depends(get_db)):
    query = db.query(MenuPlan)
    if start_date:
        query = query.filter(MenuPlan.date >= start_date)
    if end_date:
        query = query.filter(MenuPlan.date <= end_date)
    return query.order_by(MenuPlan.date).all()

@app.post("/api/menu", response_model=MenuResponse)
def add_menu_item(item: MenuCreate, db: Session = Depends(get_db)):
    menu_item = MenuPlan(**item.dict())
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item

@app.delete("/api/menu/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    db.query(MenuPlan).filter(MenuPlan.id == item_id).delete()
    db.commit()
    return {"ok": True}

@app.get("/api/shopping-list")
def generate_shopping_list(start_date: date, end_date: date, db: Session = Depends(get_db)):
    menu_items = db.query(MenuPlan).filter(MenuPlan.date >= start_date, MenuPlan.date <= end_date).all()
    
    required = {}

    for item in menu_items:
        recipe = item.recipe
        for ing in recipe.ingredients:
            name = ing.name
            total_needed = ing.amount * item.servings
            
            if name in required:
                if required[name]['unit'] != ing.unit:
                    continue
                required[name]['amount'] += total_needed
            else:
                required[name] = {'amount': total_needed, 'unit': ing.unit}
    
    shopping_list = []
    for name, data in required.items():
        inventory_item = db.query(InventoryItem).filter(InventoryItem.name == name).first()
        in_stock = inventory_item.amount if inventory_item else 0
        
        if inventory_item and inventory_item.unit != data['unit']:
            continue
            
        to_buy = data['amount'] - in_stock
        
        if to_buy > 0:
            shopping_list.append({
                "name": name,
                "needed": round(data['amount'], 2),
                "in_stock": round(in_stock, 2),
                "to_buy": round(to_buy, 2),
                "unit": data['unit']
            })
            
    return shopping_list

@app.get("/api/suggestions")
def suggest_recipes(db: Session = Depends(get_db)):
    inventory = db.query(InventoryItem).all()
    inventory_names = {item.name for item in inventory if item.amount > 0}
    
    recipes = db.query(Recipe).all()
    suggestions = []
    
    for recipe in recipes:
        recipe_ings = {ing.name for ing in recipe.ingredients}
        if not recipe_ings:
            continue
            
        available = recipe_ings.intersection(inventory_names)
        missing = recipe_ings - inventory_names
        match_percentage = (len(available) / len(recipe_ings)) * 100
        
        if match_percentage > 0:
            suggestions.append({
                "recipe": recipe,
                "match_percentage": round(match_percentage, 1),
                "missing_ingredients": list(missing)
            })
    
    suggestions.sort(key=lambda x: x['match_percentage'], reverse=True)
    return suggestions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)