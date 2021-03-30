#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def read_lines(filename):
	with open(filename, 'r') as file:
		return file.read().split('\n')

def split_text_and_target(filename):
	text, target = [], []
	lines = read_lines(filename)
	for line in lines:
		cols = line.split('\t')
		text.append(cols[1])
		target.append(cols[0])
	return np.array(text), np.array(target)

def train_nb():
	X, y = split_text_and_target('output/articles-scores.tsv')
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
	count = CountVectorizer()
	bag_of_words = count.fit_transform(X_train)
	# Create feature matrix
	features = bag_of_words.toarray()
	# Use multinomial naive bayes
	classifier = MultinomialNB()
	# Train model
	model = classifier.fit(features, y_train)
	return model, X_test, y_test

def new_articles():
	articles = []
	#articles.append("SÃO PAULO O governo João Doria (PSDB) publicou neste sábado (27) decreto que declara a educação atividade essencial, elevando a pressão para a reabertura das escolas mesmo à revelia das prefeituras. A norma adiciona ao decreto que disciplina a volta às aulas um artigo com a seguinte redação: “ficam reconhecidas como essenciais as atividades desenvolvidas no âmbito da rede pública e das instituições privadas de ensino”. Em nota, o Movimento Escolas Abertas, que reúne pais com essa bandeira, principalmente da rede particular, afirmou que a norma agora impede prefeitos de fechar os colégios. Esse, no entanto, não é o único entendimento possível do texto, já que o parágrafo 1º do artigo do decreto estadual em questão condiciona a retomada das aulas na rede estadual e privada à inexistência de ato fundamentado pela prefeitura em sentido contrário. Ou seja, o município pode vetar a reabertura, desde que embase a decisão. A interpretação de qualquer forma, deve ser alvo de disputa judicial. Como mostrou a Folha, escolas particulares de educação infantil preparam uma ofensiva judicial caso o prefeito Bruno Covas (PSDB) decida prorrogar o fechamento das unidades de ensino na capital paulista. Covas decidiu por medida mais restritiva do que a prevista pelo governo estadual para as escolas durante a fase emergencial. O prefeito proibiu qualquer atividade presencial nas unidades públicas e privadas do município até 4 de abril. Pelo plano estadual, as unidades de ensino podem continuar abertas, desde que atendam até 35% dos alunos matriculados, com a recomendação de restringir ao máximo as ações presenciais e atender só os alunos mais vulneráveis. A divergência entre o estado e a prefeitura da capital paulista vem desde o ano passado. Em setembro, o governo paulista liberou a volta às aulas presenciais, mas o município barrou, permitindo apenas atividades extracurriculares a partir de outubro. Representando pais de alunos da rede pública, o movimento Famílias Pela Vida criticou o decreto editado pela gestão Dória e reclamou que as famílias não foram consultadas para a edição da norma. “Essa decisão foi tomada depois de intenso lobby do Movimento Escolas Abertas, que representa famílias de escolas particulares e tem contatos privilegiados no meio político”, diz texto divulgado pelo grupo. Os integrantes do coletivo afirmam ser um escárnio priorizar a abertura de qualquer atividade em meio ao aumento de casos de Covid. Eles pedem educação remota de qualidade, com equipamentos para todos; auxílio emergencial; aumento da testagem; aquisição de vacinas e lockdown para frear o avanço da doença. O fechamento das escolas está associado a problemas de saúde mental para crianças e adolescentes, a lacunas de aprendizagem e a desigualdade educacional. Por outro lado, boletim epidemiológico recente da Secretaria estadual da Educação afirma que “a manutenção de baixas taxas de infecção na comunidade é fator crítico para manter as escolas abertas durante a pandemia”.")
	articles.append("Teste teste.")
	return articles

def main():
	new_article = np.array(new_articles())
	model, X_test, y_test = train_nb()
	y_pred = model.predict(new_article)
	print(y_pred)
	#y_pred = model.predict(X_test)
	#metrics.f1_score(y_test, y_pred)
	#print(model.predict(new_article))

main()