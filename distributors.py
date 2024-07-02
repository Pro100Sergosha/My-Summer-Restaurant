from parametres import parametres
from creator import folder_path

from distributor_validators import validate_distributor_inputs

path = folder_path()

distributor_path = f'{path}/{parametres[7]['name']}'


def create_new_distributor():
    from crud import append_csv, read_csv
    while True:
        inputs = {}
        input_texts = ['Enter company id: ', 'Enter company name: ', 'Enter company address: ','Etner distributor name: ','Enter distributor phone number: ']
        for inp in input_texts:
            txt = input(inp)
            validated_data = validate_distributor_inputs(txt, input_texts, inp)
            if validated_data[0]:
                inputs[parametres[7]['headers'][input_texts.index(inp)]] = validated_data[1]
            else:
                break
        if len(inputs.keys()) == len(input_texts):
            append_csv(distributor_path, [inputs])
            return False, print(f'Distributor added successfuly!')

