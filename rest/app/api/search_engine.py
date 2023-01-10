from app.db.models import TokenizedTexts, Sentences, Texts
from app.db.utils import exec_statement
from app.api.constants import column_mapper, PREFIX, POSTFIX_PATTERN, SENTENCE_TOKENS, TOKEN_INX, TOKEN, TOKEN_START, TOKEN_END
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import aliased


# 1. Create N search fields
# 2. Join search fields
# 3. Select from joined fields

def create_condition(form):
    return and_(*[column_mapper[condition].op("~")('^' + value + '$')
                  for conditions in form['conditions']
                  for condition, value in conditions.items()])


def create_search_field(form):
    search_field = select(TokenizedTexts.lemma, TokenizedTexts.token,
                          TokenizedTexts.token_inx, TokenizedTexts.token_spacy_pos,
                          TokenizedTexts.text_id, TokenizedTexts.text_year,
                          TokenizedTexts.sentence_id, TokenizedTexts.task_id) \
        .where(create_condition(form))

    return search_field


def join_fields(fields):
    init_field = fields[0]
    stmt = select(*fields)
    for field in fields[1:]:
        stmt = stmt.join(field, and_(init_field.c.text_id == field.c.text_id, init_field.c.text_year == field.c.text_year,
                                     init_field.c.sentence_id == field.c.sentence_id, init_field.c.task_id == field.c.task_id))
    return stmt


def create_statement(forms):
    fields = [aliased(create_search_field(form).subquery(),
                      name=PREFIX + str(i)) for i, form in enumerate(forms)]
    joined_fields = aliased(join_fields(fields).subquery(), name="fields")
    stmt = select(Texts.text_name, joined_fields, Sentences.sentence_tokens) \
        .join(Sentences, and_(Texts.text_id == Sentences.text_id,
                              Texts.text_year == Sentences.text_year,
                              Texts.task_id == Sentences.task_id)) \
        .join(joined_fields,
              and_(Sentences.text_id == joined_fields.c.text_id,
                   Sentences.text_year == joined_fields.c.text_year,
                   Sentences.sentence_id == joined_fields.c.sentence_id,
                   Sentences.task_id == joined_fields.c.task_id))
    return stmt


def get_token_span(sentence, token_inx, token):
    sentence = sentence.split(' ')
    token_end = len(' '.join(sentence[:token_inx + 1]))
    token_start = token_end - len(token)
    return token_start, token_end


def exec_search(forms):
    stmt = create_statement(forms)

    result = exec_statement(stmt)

    rows = list()
    for row in result:
        row = dict(row)

        for i in range(len(forms)):
            postfix = POSTFIX_PATTERN(i)

            token_start, token_end = get_token_span(
                row[SENTENCE_TOKENS], row[TOKEN_INX + postfix], row[TOKEN + postfix])
            row[TOKEN_START + postfix] = token_start
            row[TOKEN_END + postfix] = token_end

        rows.append(row)
    return rows
