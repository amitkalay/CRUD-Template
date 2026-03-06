from fastapi import FastAPI, HTTPException
from database import get_internet_usage_db, init_db, get_db
import schemas

app = FastAPI()

# Initialize database on startup
init_db()

# enhance this API to include an optional year query parameter to filter results by year
# enhance this further to include an optional region query parameter to filter results by region as well
@app.get("/internet_usage_data/", response_model=list[schemas.InternetUsageDataSchema])
def read_internet_usage_data(year: int | None = None, region: str | None = None):
    with get_internet_usage_db() as conn:
        if year is not None and region is not None:
            items = conn.execute("SELECT * FROM usage_table WHERE Year = ? AND Region = ?", (year, region)).fetchall()
        elif year is not None:
            items = conn.execute("SELECT * FROM usage_table WHERE Year = ?", (year,)).fetchall()
        elif region is not None:
            items = conn.execute("SELECT * FROM usage_table WHERE Region = ?", (region,)).fetchall()
        else:
            items = conn.execute("SELECT * FROM usage_table").fetchall()
        return [dict(row) for row in items]
    
# create a new API endpoint to write a single record to the database. The API should accept a JSON body with the same structure as the InternetUsageDataSchema, but without the id field (since it will be auto-incremented by the database). The API should return the newly created record, including the generated id.
@app.post("/internet_usage_data/", response_model=schemas.InternetUsageDataSchema)
def create_internet_usage_data(item: schemas.InternetUsageDataCreate):
    with get_internet_usage_db() as conn:
        # if id already exists, return an error or do a NO-OP
        cursor = conn.execute(
            "INSERT INTO usage_table (Region, Year, Percentage_using, Source) VALUES (?, ?, ?, ?)",
            (item.Region, item.Year, item.Percentage_using, item.Source)
        )
        new_id = cursor.lastrowid
        new_item = conn.execute("SELECT * FROM usage_table WHERE id = ?", (new_id,)).fetchone()
        return dict(new_item)