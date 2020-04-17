# Create, read, update, and delete functions

## Reading
def group_by_location_order_by_date(db, location_type: str = "continent", location_value: str = "North America", case_type: str = "Confirmed"):
    rs = db.execute(
        "SELECT co.name, t.name, ca.date, sum(ca.count) \
            FROM case_timeseries ca \
                JOIN type_category t \
                    ON (ca.case_type=t.type_category_id) \
                        JOIN " + str(location_type) + " co \
                            ON (ca." + str(location_type) + "_id=co." + str(location_type) + "_id) \
                                WHERE co.name='" + str(location_value) + "' AND t.name='" + str(case_type)+ "' \
                                    GROUP BY co.name, t.name, ca.date \
                                        ORDER BY ca.date;"
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