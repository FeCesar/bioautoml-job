from enum import Enum


class ProcessTypes(Enum):

    DNA_RNA = {
        'type': 'AFEM_PARAMETERS',
        'reference': 'BioAutoML-feature.py'
    }

    PROTEIN = {
        'type': 'AFEM_PARAMETERS',
        'reference': 'BioAutoML-feature-protein.py'
    }

    WITH_NUMERICAL_MAPPING_DNA_RNA = {
        'type': 'AFEM_PARAMETERS',
        'reference': 'BioAutoML-feature-mapping.py'
    }

    BINARY_PROBLEMS = {
        'type': 'METALEARNING_PARAMETERS',
        'reference': 'BioAutoML-binary.py'
    }

    MULTICLASS_PROBLEMS = {
        'type': 'METALEARNING_PARAMETERS',
        'reference': 'BioAutoML-multiclass.py'
    }

    IFEATURE_PROTEIN = {
        'type': 'AFEM_PARAMETERS',
        'reference': 'BioAutoML+iFeature-protein.py'
    }
