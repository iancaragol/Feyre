from datetime import datetime
from os import environ
from azure.data.tables import TableClient, TableServiceClient
from azure.core.exceptions import ResourceExistsError, HttpResponseError

# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/tables/azure-data-tables/samples/sample_create_client.py
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/tables/azure-data-tables/samples/sample_insert_delete_entities.py

class TableHelper:
    def __init__(self):
        self.partition_key = "Development" #getenv("ENV")
        # self.connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix={}".format(
        #     self.account_name, self.access_key, self.endpoint_suffix
        # )
        self.endpoint = environ.get("TABLE_ENDPOINT")
        self.connection_string = environ.get("TABLE_CONNECTION_STRING")

    def create_table_client(self, table_name : str):
        """
        Returns an Azure Storage Table Client for table_name
        """
        table_client = TableClient.from_connection_string(
            conn_str = self.connection_string,
            table_name = table_name
        )

        return table_client

    def create_table_service(self):
        """
        Returns an Azure Storage Table Service Client for the storage account
        """
        table_service = TableServiceClient.from_connection_string(
            conn_str = self.connection_string
        )
        return table_service

    def insert_entity(self, table_name : str, entity_json : dict):
        """
        Inserts entity_json into table_name
        """

        # TODO(IAN) Add some sort of error handling/retry logic here.
        # Also a good place to emit the latency to grafana
        table_client = self.create_table_client(table_name = table_name)
        try:
            entity_json_formatted = self.format_entity(table_name = table_name, entity_json = entity_json)
            resp = table_client.create_entity(entity = entity_json_formatted)
            return entity_json_formatted["RowKey"]
        except Exception as e:
            print("An exception occurred. Retrying!")
            print(str(e))

    def get_entity(self, table_name : str, row_key : str = None):
        """
        Gets the entity at row_key in table_name.

        Returns the entity as a dictionary.

        https://docs.microsoft.com/en-us/rest/api/storageservices/Querying-Tables-and-Entities?redirectedfrom=MSDN
        """
        table_client = self.create_table_client(table_name)

        if table_name == "stats":
            # For stats table, we always get the most recent one
            filter = f"PartitionKey eq '{self.partition_key}'"
            # results_per_page = 1means we will only get one result per page
            # This is the same as taking the top value
            entities = table_client.query_entities(query_filter = filter, results_per_page = 1)  
            first_entity = next(entities) # entities is a generator, so we call next once to get the top entity       
            return dict(first_entity)

        elif table_name == "users":
            # IDK what to do here
            return None

        elif table_name == "characters":
            # For characters, should get the character list based on user_id
            return None

        elif table_name == "prefixes":
            # For prefixes, our row key should be the guild id
            return None

    def format_entity(self, table_name : str, entity_json : dict):
        """
        Formats the entity json by adding the ParitionKey, RowKey, and a timestamp as neccessary (based on table_name)
        """
        if table_name == "stats":
            entity_json[u"PartitionKey"] = self.partition_key # Partition Key is the ENV, so Development/Production

            # Allows us to quickly get the most recent entry 
            # https://stackoverflow.com/questions/40593939/how-to-retrieve-latest-record-using-rowkey-or-timestamp-in-azure-table-storage
            now = datetime.utcnow()
            ticks = self.reverse_ticks(now)
            entity_json[u"RowKey"] = f"{ticks:0>19}" # Zero pad the string, so 2 -> 0000..0002

            # Add datetime, so we can graph this data
            entity_json["insert_timestamp"] = now.timestamp()
            return entity_json 

        elif table_name == "users":
            # Not sure what to do here
            # Users is just a giant list of unique values
            # So there may be a better way than table to store it?
            # Or it just has a row_key == user_id
            return None

        elif table_name == "characters":
            # For characters, our row key should probably be the user id
            return None

        elif table_name == "prefixes":
            # For prefixes, our row key should be the guild id
            return None

        return None

    def reverse_ticks(self, dt : datetime):
        """
        Returns the max datetime - now in ticks

        Using this value as RowKey means that entry will always be on top of the table.
        """
        return int((datetime.max - dt).total_seconds() * 10000000)

# Leaving this here for easy devbox testing.
# if __name__ == "__main__":
#     example = {
#         "ability": str(3)
#         }

#     th = TableHelper()
#     th.insert_entity("stats", example)

#     e = th.get_entity("stats")
#     print(e)