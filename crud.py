import csv

def read_csv(filename):
    with open(filename) as file:
        file = csv.DictReader(file)
        return list(file)


    
def write_csv(filename, data):
    headers = list(data[0].keys())
    with open(filename, "w", newline="") as file:
        write = csv.DictWriter(file,fieldnames=headers)
        write.writeheader()
        for line in data:
            write.writerow(line)


def append_csv(filename, data):
    from utils import check_create_headers
    headers = list(data[0].keys())
    with open(filename, "a", newline="") as file:
        write = csv.DictWriter(file,fieldnames=headers)
        check_create_headers(filename, data)
        for line in data:
            write.writerow(line)


def update_csv(filename, updated_data):
    rows = [row for row in updated_data]
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
