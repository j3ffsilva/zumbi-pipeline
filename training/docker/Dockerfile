# Dockerfile for prodigy, just place your linux-wheel (prodigy-1.10.7-cp36.cp37.cp38-cp36m.cp37m.cp38-linux_x86_64.whl) in same directoty as
# this dockerfile and:
# > docker build . -t prodigy
# > docker run -it -p 8080:8080 -v ${PWD}:/work prodigy bash
# > 
# NORMAL RUN
# > prodigy ner.manual zumbi_ner blank:pt ./all_articles.jsonl --label PER,GOV,COM,EDU,VEIC,NPO,LOC,TEM,LEG,FAC,CUR,WRK --patterns ./NER-patterns.jsonl
#
# > BERT RUN
# > prodigy bert.ner.manual zumbi_ner ./all_articles.jsonl --label PER,GOV,COM,EDU,VEIC,NPO,LOC,TEM,LEG,FAC,CUR,WRK --tokenizer-vocab ./bert-base-uncased-vocab.txt --lowercase --hide-wp-prefix -F transformers_tokenizers.py
# 
# TRAIN
# prodigy train ner zumbi_ner pt_core_news_lg

FROM python:3.6
RUN mkdir /prodigy
WORKDIR /prodigy
COPY ./prodigy-1.10.7-cp36.cp37.cp38-cp36m.cp37m.cp38-linux_x86_64.whl /prodigy
COPY ./all_articles.jsonl /prodigy
COPY ./transformers_tokenizers.py /prodigy
COPY ./NER-patterns.jsonl /prodigy
RUN pip install prodigy-1.10.7-cp36.cp37.cp38-cp36m.cp37m.cp38-linux_x86_64.whl
RUN python -m spacy download pt_core_news_lg
EXPOSE 8080
RUN mkdir /work
ENV PRODIGY_HOME /work
WORKDIR /work