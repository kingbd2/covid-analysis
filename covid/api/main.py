from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from .crud import group_by_location_order_by_date, get_latest_case_count
from sqlalchemy.orm import Session
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Test query, return an entire table (select *)
@app.get("/api/v1/{table_name}")
async def getTable(table_name: str, db: Session = Depends(get_db)):
    rs = db.execute("SELECT * FROM " + str(table_name))
    row_list = []
    for row in rs:
        row_list.append(row)
    result_dict = {'query_result': [dict(row) for row in row_list]}
    # json_data = json.dumps(result_dict)
    return result_dict

# Get case totals by location and case type
@app.get("/api/v1/totals/{location_type}/{location_value}/{case_type}")
async def get_latest_cases(db: Session = Depends(get_db), location_type: str = "continent", location_value: str = "North America", case_type: str = "Confirmed", sum_counts: bool = False):
    return get_latest_case_count(db, location_type, location_value, case_type, sum_counts)


# API endpoint to display cases by country
@app.get("/api/v1/country/{country_name}/{case_type}")
async def cases_by_country(db: Session = Depends(get_db), country_name: str = "Canada", case_type: str = "Confirmed"):
    return group_by_location_order_by_date(db, "country", country_name, case_type)

# API endpoint to display cases by province_state
@app.get("/api/v1/province_state/{province_state_name}/{case_type}")
async def cases_by_province_state(db: Session = Depends(get_db), province_state: str = "Ontario", case_type: str = "Confirmed"):
    return group_by_location_order_by_date(db, "province_state", province_state, case_type)

