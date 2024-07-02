from crud import read_csv, update_csv, write_csv, append_csv
from distributor_validators import *
import tempfile
import os

def test_csv_operations():
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')

    try:
        initial_data = [
            {'name': 'Alice', 'age': '30', 'city': 'New York'},
            {'name': 'Bob', 'age': '25', 'city': 'Los Angeles'}
        ]
        
        append_data = [
            {'name': 'Charlie', 'age': '22', 'city': 'Chicago'}
        ]

        updated_data = [
            {'name': 'Alice', 'age': '31', 'city': 'San Francisco'},
            {'name': 'Bob', 'age': '26', 'city': 'Los Angeles'}
        ]

        write_csv(temp_file.name, initial_data)
        assert read_csv(temp_file.name) == initial_data

        append_csv(temp_file.name, append_data)
        expected_append_result = initial_data + append_data
        assert read_csv(temp_file.name) == expected_append_result

        update_csv(temp_file.name, updated_data)
        assert read_csv(temp_file.name) == updated_data
    
    finally:
        temp_file.close()
        os.remove(temp_file.name)


