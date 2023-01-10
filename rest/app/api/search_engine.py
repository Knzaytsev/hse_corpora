from app.db.models import TokenizedTexts, Sentences, Texts
from app.db.utils import exec_statement
from sqlalchemy import select, and_, or_

column_mapper = {
    'lemma': TokenizedTexts.lemma,
    'token': TokenizedTexts.token,
    'dep': TokenizedTexts.token_dep,
    'pos': TokenizedTexts.token_spacy_pos,
}


def create_condition(forms):
    return or_(
        *[and_(*[column_mapper[condition].op("~")('^' + value + '$')
                 for conditions in form['conditions']
                 for condition, value in conditions.items()])
          for form in forms]
    )

def get_token_span(sentence, token_inx, token):
    sentence = sentence.split(' ')
    token_end = len(' '.join(sentence[:token_inx + 1]))
    token_start = token_end - len(token)
    return token_start, token_end

def exec_search(forms):
    stmt = select(Texts.text_name, TokenizedTexts.lemma, TokenizedTexts.token, 
                  TokenizedTexts.token_inx, TokenizedTexts.token_spacy_pos, Sentences.sentence_tokens,
                  ) \
        .join(Sentences, and_(Texts.text_id == Sentences.text_id,
                              Texts.text_year == Sentences.text_year, 
                              Texts.task_id == Sentences.task_id)) \
        .join(TokenizedTexts,
              and_(Sentences.text_id == TokenizedTexts.text_id,
                   Sentences.text_year == TokenizedTexts.text_year,
                   Sentences.sentence_id == TokenizedTexts.sentence_id, 
                   Sentences.task_id == TokenizedTexts.task_id)) \
        .where(create_condition(forms))

    descriptions = stmt.column_descriptions
    result = exec_statement(stmt)

    rows = list()
    for row in result:
        columns = dict()
        for i, description in enumerate(descriptions):
            column, value = description["name"], row[i]
            columns[column] = value

        token_start, token_end = get_token_span(columns['sentence_tokens'], columns['token_inx'], columns['token'])
        columns['token_start'] = token_start
        columns['token_end'] = token_end

        rows.append(columns)
    return rows
