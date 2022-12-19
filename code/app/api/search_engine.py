from app.db.models import TokenizedTexts, Sentences, Texts
from app.db.utils import exec_statement
from sqlalchemy import select, and_


def select_token(token):
    stmt = select(Texts.text_name, Sentences.sentence_tokens,
                  TokenizedTexts.token, TokenizedTexts.token_start,
                  TokenizedTexts.token_end) \
        .join(Sentences, Texts.text_id == Sentences.text_id) \
        .join(TokenizedTexts,
              and_(Sentences.text_id == TokenizedTexts.text_id,
                   Sentences.sentence_id == TokenizedTexts.sentence_id)) \
        .where(TokenizedTexts.token == token)
    descriptions = stmt.column_descriptions
    result = exec_statement(stmt)
    return [{description["name"]: row[i] for i, description in enumerate(descriptions)} for row in result]
