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
    row_list = []
    for row in rs:
        row_list.append(row)
    result_dict = {'query_result': [dict(row) for row in row_list]}
    return result_dict