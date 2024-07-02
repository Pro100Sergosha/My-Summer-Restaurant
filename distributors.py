from parametres import parametres
from creator import folder_path

from distributor_validators import validate_distributor_inputs

path = folder_path()

# Path to the distributors CSV file
distributor_path = f'{path}/{parametres[5]["name"]}'

def create_new_distributor():
    """
    Prompts the user to input details for creating a new distributor. Validates each input using the
    respective validation functions and appends the new distributor's details to the distributors CSV file
    if all inputs are valid.
    """
    from crud import append_csv, read_csv
    
    while True:
        inputs = {}
        input_texts = ['Enter company id: ', 'Enter company name: ', 'Enter company address: ', 'Enter distributor name: ', 'Enter distributor phone number: ']
        
        for inp in input_texts:
            # Prompt the user for input
            txt = input(inp)
            
            # Validate the input
            validated_data = validate_distributor_inputs(txt, input_texts, inp)
            if validated_data[0]:
                # Store the valid input in the inputs dictionary
                inputs[parametres[5]['headers'][input_texts.index(inp)]] = validated_data[1]
            else:
                # If validation fails, break out of the loop
                break
        
        # Check if all inputs are valid
        if len(inputs.keys()) == len(input_texts):
            # Append the new distributor's details to the CSV file
            append_csv(distributor_path, [inputs])
            return False, print('Distributor added successfully!')
