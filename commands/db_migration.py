from dotenv import load_dotenv
from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_schema_manager.modules.migration.data.change_log_data import ChangeLogData
from mysql_schema_manager.modules.migration.data.migration_data import MigrationData
from mysql_schema_manager.modules.migration.managers.change_log_manager import ChangeLogManager
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager

""" Script for running database migrations
"""


if __name__ == '__main__':
    load_dotenv()
    try:
        print("Establishing connection...")
        connection_manager: ConnectionManager = ConnectionManager("migration_connection_pool")
        change_log_manager: ChangeLogManager = ChangeLogManager(
            change_log_data=ChangeLogData(
                connection_manager=connection_manager
            )
        )
        migration_manager = MigrationManager(
            migration_data=MigrationData(
                connection_manager=connection_manager
            ),
            change_log_manager=change_log_manager
        )
        print("Connection established. Running migration...")
        migration_result = migration_manager.run()
        change_logs = migration_result.get_change_logs()
        for change_log in change_logs:
            print(f"{change_log.get_file_name()} executed...")
        if not migration_result.get_status():
            print(migration_result.get_message())
        print("Migration complete...")
    except Exception as e:
        print(str(e))
