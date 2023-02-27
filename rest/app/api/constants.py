from app.db.models import TokenizedTexts

column_mapper = {
    'lemma': TokenizedTexts.lemma,
    'token': TokenizedTexts.token,
    'dep': TokenizedTexts.token_dep,
    'pos': TokenizedTexts.token_spacy_pos,
}

PREFIX = "tokenized_"
POSTFIX_PATTERN = lambda x: '_' + str(x) if x > 0 else ''

SENTENCE_TOKENS = 'sentence_tokens'
TOKEN_POS = 'token_spacy_pos'
TOKEN_INX = 'token_inx'
LEMMA = 'lemma'
TOKEN = 'token'
TOKEN_START = 'token_start'
TOKEN_END = 'token_end'
TEXT_NAME = 'text_name'
ERROR_SPAN = 'error_span'
CORRECTION = 'correction'
MISTAKE_TYPE = 'mistake_type'
MISTAKE_CAUSE = 'cause'
NUM_FIELDS = 'num_fields'

WORDS_COLUMNS = [
    TOKEN_INX, TOKEN, TOKEN_START, TOKEN_END, TOKEN_POS, LEMMA
]

MISTAKES_COLUMNS = [
    MISTAKE_TYPE, MISTAKE_CAUSE, ERROR_SPAN, CORRECTION
]

MODEL_FIELDS = [
    TEXT_NAME, LEMMA, TOKEN_POS, SENTENCE_TOKENS, 
    TOKEN_INX, TOKEN, TOKEN_START, TOKEN_END, 
    ERROR_SPAN, CORRECTION,
    NUM_FIELDS,
]