from dotenv import load_dotenv
from mysql_schema_manager.modules.migration.managers.migration_manager import MigrationManager

""" Script for generating SQL scripts
"""


if __name__ == '__main__':
    load_dotenv()
    try:
        migration_manager = MigrationManager()
        file_name = migration_manager.generate_file()
        print(f"File generated: {file_name}")
    except Exception as e:
        print(f"Error generating file: {str(e)}")
