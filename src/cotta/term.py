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


def validate_subject(s):
    if is_valid_iri(s):
        return
    elif is_valid_blanknode(s):
        return
    raise TypeError(f'The subject term `{s}` is not a valid IRI or blank node.')


def validate_object(o):
    if is_valid_literal(o):
        return
    elif is_valid_iri(o):
        return
    elif is_valid_blanknode(o):
        return
    raise TypeError(f'The object term `{o}` is not a valid IRI, literal or blank node.')


def validate_predicate(p):
    if not is_iri(p) or not is_valid_iri(p):
        raise TypeError(f'The predicate term `{p}` is not a valid IRI.')


def validate_named_graph(g):
    if not g:
        return
    if not is_iri(g) or not is_valid_iri(g):
        raise ValueError(f'The named graph term `{g}` is not a valid IRI.')


def remove_xsd_string(literal):
    if literal.endswith(f'"^^<{XSD_STRING}>'):
        return literal[:-43]
    else:
        return literal


def get_literal_lexical_form(literal):
    if is_literal(literal):
        if literal.endswith('"'):    # no datatype nor language tag
            return literal
        elif literal.endswith('>'):   # has datatype
            return '"^^<'.join(literal.split('"^^<')[:-1]) + '"'
        # has language tag
        return '"@'.join(literal.split('"@')[:-1]) + '"'

    raise TypeError(f'`{literal}` is not a valid literal.')


def get_literal_datatype(literal):
    if is_literal(literal):
        if literal.endswith('>'):
            return '<' + literal.split('"^^<')[-1]
        # has no datatype
        return None

    raise TypeError(f'`{literal}` is not a valid literal.')


def get_literal_langtag(literal):
    if is_literal(literal):
        if not literal.endswith('"') and not literal.endswith('>'):
            return '@' + literal.split('@')[-1]
        # has no langtag
        return None

    raise TypeError(f'`{literal}` is not a valid literal.')


def decode_escape_sequence(rdf_term):
    if not is_literal(rdf_term) or '\\' not in rdf_term:
        return rdf_term

    rdf_term = rdf_term.replace('\\n', '\n')
    rdf_term = rdf_term.replace('\\r', '\r')
    rdf_term = rdf_term.replace('\\t', '\t')
    rdf_term = rdf_term.replace('\\"', '"')
    rdf_term = rdf_term.replace('\\\\', '\\')

    return rdf_term


def encode_escape_sequence(rdf_term):
    rdf_term = rdf_term.replace('\\', '\\\\')
    rdf_term = rdf_term.replace('\n', '\\n')
    rdf_term = rdf_term.replace('\r', '\\r')
    rdf_term = rdf_term.replace('\t', '\\t')
    rdf_term = rdf_term.replace('"', '\\"')

    return rdf_term
