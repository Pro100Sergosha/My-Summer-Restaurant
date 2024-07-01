import csv



def read_csv(filename):
    with open(filename) as file:
        file = csv.DictReader(file)
        return list(file)




def write_csv(filename,data):
    headers = list(data[0].keys())
    with open(filename,"w",newline="") as file:
        write = csv.DictWriter(file,fieldnames=headers)
        write.writeheader()
        for line in data:
            write.writerow(line)

