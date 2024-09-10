import re


def caseValidator(self, patronMuni, municipio):
        patternMuni = re.compile(rf'{patronMuni}')
        if not patternMuni.match(str(municipio)):
            raise ValueError(f"Cambie el Municipio para que concuerde con el patron {patronMuni}")

