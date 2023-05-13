__author__ = "Julián Arenas-Guerrero"
__credits__ = ["Julián Arenas-Guerrero"]

__license__ = "Apache-2.0"
__maintainer__ = "Julián Arenas-Guerrero"
__email__ = "julian.arenas.guerrero@upm.es"


from uuid import uuid4

from .constants import XSD_STRING


def iri(iri):
    return f'<{iri}>'


def blanknode():
    return f'_:{uuid4().hex}'


def literal(literal, datatype=None, lang=None):
    # TODO: escape sequences
    literal = f'"{literal}"'

    if datatype and lang:
        raise TypeError('A literal cannot have a datatype and a language tag.')

    if lang:
        literal += f'@{lang}'
    elif datatype and datatype != XSD_STRING:
        literal += f'^^<{datatype}>'

    return literal


def is_iri(iri):
    return iri.startswith('<')


def is_literal(literal):
    return literal.startswith('"')


def is_blanknode(blanknode):
    return blanknode.startswith('_:')


invalid_iri_characters = {'<', '>', '"', ' ', '{', '}', '|', '\\', '^', '`'}

def is_valid_iri(iri):
    if iri[0] != '<' or iri[-1] != '>':
        return False

    return invalid_iri_characters.isdisjoint(iri[1:-1])


def is_valid_literal(literal):
    if literal[0] != '"':
        return False
    if literal[-1] == '"':
        return True

    datatype_lang = literal[1:].split('"')[-1]
    if datatype_lang.startswith('^^') and is_valid_iri(datatype_lang[2:]):
        return True
    if datatype_lang.startswith('@') and is_valid_langtag(datatype_lang[1:]):
        return True

    return False


def is_valid_langtag(lang):
    # the place to look for valid language subtags is the IANA Language Subtag Registry
    if lang.replace('-', '').isalpha():
        return True
    return False


def is_valid_blanknode(blanknode):
    if blanknode[:2] != '_:':
        # Check that the blanknode is valid according to RDF 1.1 N-Triples, Section 2.4
        return False
    if blanknode[2] in ['.', '-', '·', '‿', '⁀']:
        return False
    if blanknode[-1] == '.':
        return False
    return True
