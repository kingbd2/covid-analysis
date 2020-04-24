from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from .crud import group_by_location_order_by_date, get_latest_case_count, get_countries_by_continent, get_provinces_states_by_country
from sqlalchemy.orm import Session
import json

api_version = 'v1'
api_base = '/api/' + api_version + '/'

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
@app.get(api_base + "{table_name}")
async def getTable(table_name: str, db: Session = Depends(get_db)):
    rs = db.execute("SELECT * FROM " + str(table_name))
    row_list = []
    for row in rs:
        row_list.append(row)
    result_dict = {'query_result': [dict(row) for row in row_list]}
    # json_data = json.dumps(result_dict)
    return result_dict

# Get countries by continent
@app.get(api_base + "{continent_value}/countries")
async def get_countries_by_continent_endpoint(db: Session = Depends(get_db), continent_value: str = "North America"):
    return get_countries_by_continent(db, continent_value)

# Get provinces/states by country
@app.get(api_base + "{country_value}/provinces_states")
async def get_provinces_states_by_country_endpoint(db: Session = Depends(get_db), country_value: str = "Canada"):
    return get_provinces_states_by_country(db, country_value)

# Get case totals by location and case type
@app.get(api_base + "totals/{location_type}/{location_value}/{case_type}")
async def get_latest_case_count_endpoint(db: Session = Depends(get_db), location_type: str = "continent", location_value: str = "North America", case_type: str = "Confirmed", sum_counts: bool = False):
    return get_latest_case_count(db, location_type, location_value, case_type, sum_counts)

# API endpoint to display cases by country
@app.get(api_base + "country/{country_name}/{case_type}")
async def group_by_location_order_by_date_endpoint(db: Session = Depends(get_db), country_name: str = "Canada", case_type: str = "Confirmed"):
    return group_by_location_order_by_date(db, "country", country_name, case_type)

# API endpoint to display cases by province_state
@app.get(api_base + "province_state/{province_state_name}/{case_type}")
async def group_by_location_order_by_date_endpoint(db: Session = Depends(get_db), province_state_name: str = "Ontario", case_type: str = "Confirmed"):
    return group_by_location_order_by_date(db, "province_state", province_state_name, case_type)

