from fastapi import FastAPI, HTTPException
from database import init_db, get_db
import schemas

app = FastAPI()

# Initialize database on startup
init_db()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (title, description) VALUES (?, ?)",
            (item.title, item.description)
        )
        item_id = cursor.lastrowid
        return {"id": item_id, **item.model_dump()}

@app.get("/items/", response_model=list[schemas.Item])
def read_items():
    with get_db() as conn:
        items = conn.execute("SELECT * FROM items").fetchall()
        return [dict(row) for row in items]

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int):
    with get_db() as conn:
        item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return dict(item)

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items SET title = ?, description = ? WHERE id = ?",
            (item.title, item.description, item_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": item_id, **item.model_dump()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item deleted successfully"}