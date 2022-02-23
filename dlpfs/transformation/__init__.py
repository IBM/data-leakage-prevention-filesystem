from typing import Dict, Optional
from diffprivlib.mechanisms import Binary, Exponential, Gaussian, Laplace


def _build_mechanism(transformation: Dict):
    mech_type = transformation.get('mech', 'Laplace')

    if mech_type == 'Laplace':
        mech = Laplace(
            epsilon=transformation.get('e', 0.1),
            delta=transformation.get('d', 0.0),
            sensitivity=transformation.get('sensitivity', 1.0)
        )

        return lambda s: str(mech.randomise(float(s)))
    if mech_type == 'Binary':
        mech = Binary(
            epsilon=transformation.get('e', 0.1),
            value0=transformation.get('true', 0),
            value1=transformation.get('false', 0),
        )
        return lambda s: mech.randomise(s)
    if mech_type == 'Gaussian':
        mech = Gaussian(
            epsilon=transformation.get('e', 0.1),
            delta=transformation.get('d', 0.0),
            sensitivity=transformation.get('sensitivity', 1)
        )
        return lambda s: str(mech.randomise(float(s)))
    if mech_type == 'Exponential':
        mech = Exponential(
            epsilon=transformation.get('e', 0.1),
            sensitivity=transformation.get('sensitivy', 1),
            candidates=transformation.get('candidates', None),
            utility=transformation.get('utility')
        )
        return lambda s: mech.randomise(s)

    raise Exception(f'Unsupported mechanism type: {mech_type}')


def _build_redact(transformation: Dict):
    char = transformation.get('char', '*')
    return lambda s: char * len(s)


def compile_transformation(transformation: Optional[Dict]):
    if transformation:
        label = transformation['type'].lower() if transformation['type'] else None

        if label == 'redact':
            return _build_redact(transformation)
        if label == 'dp':
            mechanism = _build_mechanism(transformation)
            return mechanism
        if label == 'none':
            return lambda x: x
    return lambda s: '*' * len(s)
