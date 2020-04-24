# Create, read, update, and delete functions

## Create

## Read
def get_countries_by_continent(db, continent_value: str = "North America"):
    rs = db.execute(
        "select cn.name, cr.name from continent cn join country cr on cr.continent_id=cn.continent_id where cn.name='" + str(continent_value) + "';"
    )
    country_list = []
    index_list=[]
    for i, row in enumerate(rs):
        index_list.append(i)
        country_list.append(row[1])
    result_dict = {
        'id': [item for item in index_list],
        'location_value': str(continent_value),
        'countries':[item for item in country_list]}
    return result_dict

def get_provinces_states_by_country(db, country_value: str = "Canada"):
    rs = db.execute(
        "select cr.name, p.name from country cr join province_state p on cr.country_id=p.country_id where cr.name='" + str(country_value) + "';"
    )
    province_state_list = []
    index_list=[]
    for i, row in enumerate(rs):
        index_list.append(i)
        province_state_list.append(row[1])
    result_dict = {
        'id': [item for item in index_list],
        'location_value': str(country_value),
        'provinces_states':[item for item in province_state_list]}
    return result_dict

def get_provinces_states_by_continent():
    return 0

def get_latest_case_count(db, location_type: str = "continent", location_value: str = "North America", case_type: str = "Confirmed", sum_counts=False):
    if sum_counts==False:
        if location_type=='continent':
            rs = db.execute(
                "SELECT location.continent_name, location.country_name, type.name, c.count_date, sum(c.count)  \
                    FROM case_timeseries c \
                        JOIN type_category type \
                            ON c.case_type=type.type_category_id \
                                JOIN \
                                    (SELECT ct.name as continent_name, co.name as country_name, co.country_id FROM country co JOIN continent ct ON co.continent_id=ct.continent_id WHERE ct.name='" + str(location_value) + "') location \
                                        ON location.country_id=c.country_id \
                                                WHERE type.name='" + str(case_type)+ "' \
                                                    AND c.count_date IN (SELECT max(count_date) FROM case_timeseries) \
                                                        GROUP BY location.continent_name, location.country_name, type.name, c.count_date;"
                )
        # Need to update this query to provide province_state names 
        elif location_type=='country':
            rs = db.execute(
                "SELECT location.name, type.name, c.count_date, c.count \
                    FROM case_timeseries c \
                        JOIN type_category type \
                            ON c.case_type=type.type_category_id \
                                JOIN " + str(location_type) + " location \
                                    ON c." + str(location_type) + "_id=location." + str(location_type) + "_id \
                                        WHERE location.name='" + str(location_value) + "' \
                                            AND type.name='" + str(case_type)+ "' \
                                                AND c.count_date IN (SELECT max(count_date) FROM case_timeseries);"
                )
        else:
            rs = db.execute(
                "SELECT c.case_timeseries_id, location.name, type.name, c.count_date, c.count \
                    FROM case_timeseries c \
                        JOIN type_category type \
                            ON c.case_type=type.type_category_id \
                                JOIN " + str(location_type) + " location \
                                    ON c." + str(location_type) + "_id=location." + str(location_type) + "_id \
                                        WHERE location.name='" + str(location_value) + "' \
                                            AND type.name='" + str(case_type)+ "' \
                                                AND c.count_date IN (SELECT max(count_date) FROM case_timeseries);"
                )
    else:
        if location_type=='continent':
            rs = db.execute(
                "SELECT location.name, type.name, c.count_date, sum(c.count) \
                    FROM case_timeseries c \
                        JOIN type_category type \
                            ON (c.case_type=type.type_category_id) \
                                JOIN \
                                    (SELECT ct.name, co.country_id FROM country co JOIN continent ct ON co.continent_id=ct.continent_id) location \
                                        ON location.country_id=c.country_id \
                                            WHERE location.name='" + str(location_value) + "' \
                                                AND type.name='" + str(case_type)+ "' \
                                                    AND c.count_date IN (SELECT max(count_date) FROM case_timeseries) \
                                                        GROUP BY location.name, type.name, c.count_date;"
                )
        else:
            rs = db.execute(
                "SELECT location.name, type.name, c.count_date, sum(c.count) \
                    FROM case_timeseries c \
                        JOIN type_category type \
                            ON (c.case_type=type.type_category_id) \
                            JOIN " + str(location_type) + " location \
                            ON (c." + str(location_type) + "_id=location." + str(location_type) + "_id) \
                            WHERE location.name='" + str(location_value) + "' \
                            AND type.name='" + str(case_type)+ "' \
                            AND c.count_date IN (SELECT max(count_date) FROM case_timeseries) \
                            GROUP BY location.name, type.name, c.count_date;"
                )
    index_list = []
    date_list = []
    count_list = []
    continent_name_list = []
    country_name_list = []
    for i, row in enumerate(rs):
        if location_type=='continent' and sum_counts==False:
            index_list.append(i)
            continent_name_list.append(row[0])
            country_name_list.append(row[1])
            date_list.append(row[3])
            count_list.append(row[4])
        else:
            index_list.append(row[0])
            date_list.append(row[-2])
            count_list.append(row[-1])
    if location_type=='continent' and sum_counts==False:
        result_dict = {
            'id': [item for item in index_list],
            'location_type': str(location_type),
            'location_value': str(location_value),
            'case_type': str(case_type),
            'dates': [item for item in date_list],
            'counts':[item for item in count_list],
            'continent_name':[item for item in continent_name_list],
            'country_name':[item for item in country_name_list]}
    else:
        result_dict = {
            'id': [item for item in index_list],
            'location_type': str(location_type),
            'location_value': str(location_value),
            'case_type': str(case_type),
            'dates': [item for item in date_list],
            'counts':[item for item in count_list]}
    return result_dict

def group_by_location_order_by_date(db, location_type: str = "continent", location_value: str = "North America", case_type: str = "Confirmed"):
    rs = db.execute(
        "SELECT location.name, type.name, c.count_date, sum(c.count) \
            FROM case_timeseries c \
                JOIN type_category type \
                    ON (c.case_type=type.type_category_id) \
                        JOIN " + str(location_type) + " location \
                            ON (c." + str(location_type) + "_id=location." + str(location_type) + "_id) \
                                WHERE location.name='" + str(location_value) + "' AND type.name='" + str(case_type)+ "' \
                                    GROUP BY location.name, type.name, c.count_date \
                                        ORDER BY c.count_date;"
        )
    index_list = []
    date_list = []
    count_list = []
    for i, row in enumerate(rs):
        index_list.append(i)
        date_list.append(row[2])
        count_list.append(row[3])
    result_dict = {
        'id': [item for item in index_list],
        'location_type': str(location_type),
        'location_value': str(location_value),
        'case_type': str(case_type),
        'dates': [item for item in date_list],
        'counts':[item for item in count_list]}
    return result_dict