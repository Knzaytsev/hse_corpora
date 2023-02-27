from app.db.models import Texts, Sentences, Mistakes, TokenizedTexts
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import aliased


class CorpusSearch():
    prefix = ''
    _include_by = True

    def __init__(self, form):
        self.form = form

    def create_condition(self):
        condition = []
        if self._include_by:
            by_search = self.column_mapper[self.form['by']].op(
                '~')('^' + self.form['value'] + '$')
            condition = [by_search]

        if self.form['conditions']:
            condition += [or_(*[and_(*[self.column_mapper[condition].in_(value)
                                       for condition, value in conditions.items() if value])
                                for conditions in self.form['conditions']])]
        return and_(*condition)

    def create_search_field(self):
        search_field = select(*self.columns) \
            .where(self.create_condition())

        return search_field


class WordsSearch(CorpusSearch):
    prefix = 'tokenized_'

    column_mapper = {
        'lemma': TokenizedTexts.lemma,
        'token': TokenizedTexts.token,
        'dep': TokenizedTexts.token_dep,
        'pos': TokenizedTexts.token_spacy_pos,
    }

    columns = [TokenizedTexts.lemma, TokenizedTexts.token,
               TokenizedTexts.token_inx, TokenizedTexts.token_spacy_pos,
               TokenizedTexts.text_id, TokenizedTexts.text_year,
               TokenizedTexts.sentence_id, TokenizedTexts.task_id]


class MistakesSearch(CorpusSearch):
    prefix = 'mistakes_'

    column_mapper = {
        'error_span_token': Mistakes.error_span,
        'error_span_poses': Mistakes.error_span_poses,
        'correction_token': Mistakes.correction,
        'correction_poses': Mistakes.correction_poses,
        'correction_lemmas': Mistakes.correction_lemmas,
        'mistake_type': Mistakes.mistake_type,
        'mistake_cause': Mistakes.cause
    }

    columns = [
        Mistakes.text_id, Mistakes.text_year,
        Mistakes.sentence_id, Mistakes.task_id,
        Mistakes.error_span, Mistakes.correction,
    ]

    def create_search_field(self):
        self.columns += [self.column_mapper[column]
                         for condition in self.form['conditions']
                         for column in condition.keys() 
                         if self.column_mapper[column] not in self.columns]
        self._include_by = False
        return super().create_search_field()


class SearchFactory():
    search_modules = {
        'mistake': MistakesSearch
    }

    def join_fields(self, fields):
        init_field = fields[0]
        stmt = select(*fields)
        for field in fields[1:]:
            stmt = stmt.join(field, and_(init_field.c.text_id == field.c.text_id, init_field.c.text_year == field.c.text_year,
                                         init_field.c.sentence_id == field.c.sentence_id, init_field.c.task_id == field.c.task_id))
        return stmt

    def create_statement(self, forms):
        fields = []
        prefix_cnt = dict()

        for form in forms:
            search_class = self.search_modules.get(
                form['by'], WordsSearch)(form)

            if search_class.prefix not in prefix_cnt:
                prefix_cnt[search_class.prefix] = 0

            fields.append(aliased(search_class.create_search_field().subquery(),
                                  name=search_class.prefix + str(prefix_cnt[search_class.prefix])))
            prefix_cnt[search_class.prefix] += 1

        joined_fields = aliased(self.join_fields(
            fields).subquery(), name="fields")

        # return joined_fields
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
