from params import params
from crud import append_csv, read_csv
from distributor_validators import validate_distributor_inputs

distributor_path = f'files/{params[0]['name']}'


def create_new_distributor(input_texts):
    while True:
        inputs = {}
        for inp in input_texts:
            txt = input(inp)
            validated_data = validate_distributor_inputs(txt, input_texts, inp)
            if validated_data[0]:
                inputs[params[0]['headers'][input_texts.index(inp)]] = validated_data[1]
            else:
                break
        if len(inputs.keys()) == len(input_texts):
            append_csv(distributor_path, [inputs])
            return print(f'Distributor added successfuly!')



# if __name__ == '__main__':
#     create_new_distributor(['Enter company id: ', 
#                            'Enter company name: ', 
#                            'Enter company address: ',
#                            'Etner distributor name: ',
#                            'Enter distributor phone number: '])