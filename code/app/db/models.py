from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, ForeignKeyConstraint

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Texts(Base):
    __tablename__ = "texts"

    text_id	= Column(Integer, primary_key=True)
    text_year = Column(Integer)
    text_name = Column(String)
    original_text_name = Column(String)
    text_mark = Column(String)
    text_date = Column(String)
    student_department = Column(String)
    cefr_level = Column(String)
    student_moniker	= Column(String)
    text_ielts = Column(Boolean)
    student_sex = Column(String)
    student_study_year = Column(Integer)
    text_work_type = Column(String)
    text_task_id = Column(String)
    text_graph_desc = Column(String)
    text_words = Column(Integer)
    text_sentences = Column(Integer)
    text_ann_checked = Column(Boolean)
    json_time_stamp = Column(Float)
    text_ann_tags = Column(Integer)
    ann_time_stamp = Column(Float)

class Sentences(Base):
    __tablename__ = "sentences"

    text_id = Column(Integer, primary_key=True)
    sentence_id = Column(Integer, primary_key=True)
    sentence_tokens = Column(String)
    sentence_poses = Column(String)
    sentence_lemmas = Column(String)
    sentence_token_spaces = Column(String)
    sentence_orig_tokens = Column(String)
    sentence_orig_token_spaces = Column(String)
    sentence_token_deps = Column(String)
    sentence_token_heads = Column(String)
    sentence_token_spacy_poses = Column(String)
    sentence_token_spacy_tags = Column(String)

    __table_args__ = (ForeignKeyConstraint([text_id],
                                        [Texts.text_id]),
                    {})

class TokenizedTexts(Base):
    __tablename__ = "tokenized_texts"

    text_id = Column(Integer, primary_key=True)
    sentence_id = Column(Integer, primary_key=True)	
    token_id = Column(Integer, primary_key=True)
    token_inx = Column(Integer)
    token = Column(String)
    pos = Column(String)
    new_pos = Column(String)
    lemma = Column(String)
    token_start = Column(Integer)	
    token_end = Column(Integer)
    token_space = Column(Integer)
    token_start_in_sentence = Column(Integer)
    token_dep = Column(String)
    token_head = Column(Integer)
    token_spacy_pos = Column(String)
    token_spacy_tag = Column(String)

    __table_args__ = (ForeignKeyConstraint([text_id, sentence_id],
                                           [Sentences.text_id, Sentences.sentence_id]),
                      {})

class Mistakes(Base):
    __tablename__ = "mistakes"

    mistake_id = Column(Integer, primary_key=True)
    text_id = Column(Integer, primary_key=True)	
    sentence_id = Column(Integer, primary_key=True)
    ann_id = Column(String)
    mistake_type = Column(String)
    error_span = Column(String)
    error_span_poses = Column(String)
    cause = Column(String)
    correction = Column(String)
    first_token_id = Column(String)
    last_token_id = Column(String)
    correction_first_token_id = Column(Integer)
    correction_last_token_id = Column(Integer)
    mistake_corrected = Column(Boolean)
    correction_tokens = Column(String)
    correction_poses = Column(String)
    correction_lemmas = Column(String)
    correction_token_spaces = Column(Float)
    ref_1 = Column(Integer)
    ref_2 = Column(Integer)
    span_start = Column(String)
    span_end = Column(String)

    __table_args__ = (ForeignKeyConstraint([text_id, sentence_id], 
                                        [Sentences.text_id, Sentences.sentence_id]),
                    {})

class Corrections(Base):
    __tablename__ = "corrections"

    mistake_id = Column(Integer, primary_key=True)
    text_id = Column(Integer, primary_key=True)	
    sentence_id = Column(Integer, primary_key=True)
    correction_token_id = Column(Integer, primary_key=True)
    correction_token = Column(String)
    correction_pos = Column(String)
    correction_lemma = Column(String)
    first_token_id = Column(String)
    correction_start_inx = Column(Integer)

    __table_args__ = (ForeignKeyConstraint([mistake_id, text_id, sentence_id],
                                        [Mistakes.mistake_id, Mistakes.text_id, Mistakes.sentence_id]),
                    {})