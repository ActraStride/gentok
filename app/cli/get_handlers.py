from app.templates.proceso_2024 import Proceso2024

proceso_2024 = Proceso2024()

subprocess_functions = {
    'pr2024': lambda **kwargs: proceso_2024.mine_presidential_election(**kwargs),
}
