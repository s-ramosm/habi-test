from src.core.connection import cursor
from src.core.exceptions import FilterNotAllowed

class StatusControler():

    tablename = "status_history"

    def get_status_by_property_ids(self, ids =  []):

        columns_query = f"SHOW COLUMNS FROM {self.tablename}"

        cursor.execute(columns_query)

        columns = [x[0] for x in cursor.fetchall()]
        columns += ["status_id", "status_name" ]
        print(columns)

        sql_query = f"""SELECT * FROM {self.tablename} SH, status S 
        where SH.status_id = S.id and status_id in (5, 4, 3)
        order by update_date desc;"""

        cursor.execute(sql_query)

        status = cursor.fetchall()

        num_columns = len(columns)

        results = [
            {columns[column]: item[column] for column in range(num_columns)}
            for item in status
        ]

        status_final_dict_data =  {}

        for item in results:
            id_property =  item.get("property_id")
            list_status = status_final_dict_data.get(
                id_property,
                []
            )
            list_status.append(item)
            status_final_dict_data[id_property] = list_status


        return status_final_dict_data




class ImmovableControler():

    allowed_filter_fields = ['year', "city", "state"]

    def handle_filters(self, **filters):
        """Generate SQL filter string based on allowed filter fields."""
        
        str_filters = ""
        for filter_name, filter_value in filters.items():
            if filter_name not in self.allowed_filter_fields:
                raise FilterNotAllowed()

            if filter_name == "year":
                try:
                    year = int(filter_value)
                    str_filters += f" and P.year = {year}"
                except ValueError:
                    raise ValueError("Year must be an integer")

            elif filter_name == "state":
                state = filter_value
                str_filters += f" and S.name = '{state}'"

            elif filter_name == "city":
                city = filter_value
                str_filters += f" and P.city = '{city}'"

        return str_filters
    
    def get_all(self, **filters):
        """
        Retrieve all properties from the database.

        Args:
            **filters: Additional filters to apply in the query.

        Returns:
            list: A list of dictionaries containing property details.
        """

        # Column names to fetch
        columns = ["address", "city", "state", "price", "description", "year"]

        # Base where clause
        where_clause = (
            "WHERE "
            "SH.status_id = S.id AND "
            "status_id IN (5, 4, 3) AND "
            "Last_status.max_date = SH.update_date AND "
            "P.id = SH.property_id AND "
            "P.id = Last_status.property_id"
        )

        # Append additional filters
        where_clause += self.handle_filters(**filters)

        # Construct the SQL query
        sql_query = (
            "SELECT P.address, P.city, S.name, P.price, P.description, P.year "
            "FROM property P, "
            "(SELECT property_id, MAX(update_date) AS max_date "
            "FROM status_history "
            "GROUP BY property_id) Last_status, "
            "status_history SH, "
            "status S "
            f"{where_clause} "
            "ORDER BY SH.update_date DESC"
        )

        cursor.execute(sql_query)
        results = [
            {columns[i]: item[i] for i in range(len(item))}
            for item in cursor.fetchall()
        ]

        return results



if __name__ == "__main__":
    _ImmovableControler = ImmovableControler()
    _ImmovableControler.getAll()



