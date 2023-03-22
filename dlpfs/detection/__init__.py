from typing import Any, Dict, Iterator, List

from ..transformation import compile_transformation

import logging

import re

try:
    import re2
except ImportError:
    import re as re2


def compile_policies(ruleSpecs, use_re2: bool):
    logging.info(f'Loading specs from {ruleSpecs}')
    return [
        {
            'rules': [build_rule(r, use_re2) for r in rule['pattern']],
            'transformation': compile_transformation(rule['transformation'])
        } for rule in ruleSpecs['rules']
    ]


def _build_terms(terms: List[str]):
    return [t.strip() for t in terms]


def _build_regex(terms: List[str]):
    return '|'.join([f'({term})' for term in terms])


class LookUpMatcher():
    def __init__(self, index, term):
        self.index = index
        self.term = term

    def start(self) -> int:
        return self.index

    def end(self) -> int:
        return self.index + len(self.term)

    def group(self, _: int = 0) -> str:
        return self.term


class LookUp():
    def __init__(self, terms: List[str]):
        self.terms = _build_terms(terms)

    def finditer(self, text: str) -> Iterator[LookUpMatcher]:
        for term in self.terms:
            last_index = -1
            while True:
                last_index = text.find(term, last_index + 1)
                if -1 == last_index:
                    break
                yield LookUpMatcher(last_index, term)

    def sub(self, fun, text: str) -> str:
        for m in self.finditer(text):
            # logging.info('match: {m}')
            text = text[0:m.start()] + fun(m) + text[m.end():]
        return text


def build_rule(rule_spec: Dict[str, Any], use_re2: bool = True):
    t = rule_spec['type']
    spec = rule_spec['spec']

    if t == 're' or t == 're2':
        if use_re2:
            return re2.compile(spec)
        else:
            return re.compile(spec)

    if t == 'lookup':
        return LookUp(spec)

    if t == 'lookup2':
        if use_re2:
            return re2.compile(_build_regex(spec))
        else:
            return re.compile(_build_regex(spec))

    raise ValueError(f'Unknown pattern type {t}')
