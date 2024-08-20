from src.core.connection import cursor

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

        print(status)

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

    allow_filter_fields = []
    
    def get_all(fields=None, **filters):
        """
        Retrieves all properties from the database.

        Args:
            fields (list, optional): List of fields to include in the result.
            **filters: Additional filters to apply in the query.

        """
        
        # Fetch column names
        columns_query = "SHOW COLUMNS FROM property"
        cursor.execute(columns_query)
        columns = [x[0] for x in cursor.fetchall()]

        sql_query = """SELECT * FROM property;"""

        cursor.execute(sql_query)

        results = [
            {columns[column]: item[column] for column in range(len(item))}
            for item in cursor.fetchall()
        ]

        return results


if __name__ == "__main__":
    _ImmovableControler = ImmovableControler()
    _ImmovableControler.getAll()



