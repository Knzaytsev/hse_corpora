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


def exec_search(forms):
    stmt = select(Texts.text_name, Sentences.sentence_tokens,
                  TokenizedTexts.token, TokenizedTexts.token_spacy_pos, TokenizedTexts.lemma,
                  TokenizedTexts.token_start_in_sentence.label('token_start'),
                  (TokenizedTexts.token_start_in_sentence +
                   (TokenizedTexts.token_end - TokenizedTexts.token_start)).label('token_end')) \
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
    return [{description["name"]: row[i] for i, description in enumerate(descriptions)} for row in result]
