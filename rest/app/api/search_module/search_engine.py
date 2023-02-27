from app.api.constants import (POSTFIX_PATTERN, SENTENCE_TOKENS, TOKEN,
                               TOKEN_END, TOKEN_INX, TOKEN_START)
from app.api.search_module.models import SearchFactory
from app.db.utils import exec_statement


def get_token_span(sentence, token_inx, token):
    sentence = sentence.split(' ')
    token_end = len(' '.join(sentence[:token_inx + 1]))
    token_start = token_end - len(token)
    return token_start, token_end


def exec_search(forms):
    stmt = SearchFactory().create_statement(forms)

    result = exec_statement(stmt)
    
    rows = list()
    for row in result:
        row = dict(row)

        offset = 0
        for i, form in enumerate(forms):
            if form['by'] in ['mistake']:
                offset += 1
                continue
            postfix = POSTFIX_PATTERN(i - offset)

            token_start, token_end = get_token_span(
                row[SENTENCE_TOKENS], row[TOKEN_INX + postfix], row[TOKEN + postfix])
            row[TOKEN_START + postfix] = token_start
            row[TOKEN_END + postfix] = token_end

        rows.append(row)
    return rows
