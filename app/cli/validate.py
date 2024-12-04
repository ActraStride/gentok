import json
import os

def get_tree():
    file_path = os.path.join(os.path.dirname(__file__), "validation.json")
    with open(file_path, "r") as file:
        return json.load(file)
    
def validate(**kwargs):
    try:
        input_process = kwargs.get('process')
        input_year = input_process[2:]
        input_subprocess = input_process[:2]
        input_state = kwargs.get('state_tag')
        input_district = kwargs.get('district_tag')
        tree = get_tree()

        if input_year not in tree:
            raise ValueError(f"El año '{input_year}' no es válido.")
            
        year_data = tree[input_year]

        if input_subprocess not in year_data:
            raise ValueError(f"El subproceso '{input_subprocess}' no es válido.")
        
        subprocess_data = year_data[input_subprocess]

        # PUNTO DE PROFUNDIDAD MINIMA REQUERIDA

        if input_state is None:
            return True

        if input_state not in subprocess_data:
            raise ValueError(f"El estado '{input_state}' no es válido.")

        state_data = subprocess_data[input_state]

        if input_district is None:
            return True

        if input_district not in state_data:
            raise ValueError(f"El distrito '{input_district}' no es válido.")
    
        return True
    except Exception as e:
        raise Exception(e)