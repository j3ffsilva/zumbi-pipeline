#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import glob
import config
import argparse
from sklearn import metrics
from util import filehelper as fh
from classifiers.racial_classifier import RacialClassifier

def read_file(filename):
	file_id = extract_file_id(filename)
	text = fh.read(filename)
	text = re.sub(r"[ \n\t]+", " ", text)
	return file_id, text

def extract_file_id(filename):
	m = re.search(r'_\d+\.', filename)
	if (not m):
		return None
	file_id = m.group(0)
	return re.sub(r"[_\.]", "", file_id)

def read_all_articles():
	articles = dict()
	for filename in get_filenames():
		file_id, text = read_file(filename)
		if (not file_id):
			continue
		articles[file_id] = text
	return articles

def get_filenames():
	return glob.glob(config.SCRAPER_OUTPUT_DIR + "article_*")

def calc_prob():
	rc = RacialClassifier()
	rc.calc_terms_probs(read_all_articles())

def score_all():
	rc = RacialClassifier()
	articles = read_all_articles()
	for article_id in articles:
		text = articles[article_id]
		_, score = rc.score(text=text)
		if (score > 2.0):
			print("{}\t{}".format(str(1), text))
		else:
			print("{}\t{}".format(str(0), text))

def train_nb():
	rc = RacialClassifier()
	rc.train_nb()
	#print(X_test)
	#y_pred = model.predict(X_test)
	#print(metrics.f1_score(y_test, y_pred))
	y_pred = rc.predict(text=new_articles())
	print(y_pred)

def new_articles():
	articles = []
	# Texto não relacionado
	#articles.append("SÃO PAULO O governo João Doria (PSDB) publicou neste sábado (27) decreto que declara a educação atividade essencial, elevando a pressão para a reabertura das escolas mesmo à revelia das prefeituras. A norma adiciona ao decreto que disciplina a volta às aulas um artigo com a seguinte redação: “ficam reconhecidas como essenciais as atividades desenvolvidas no âmbito da rede pública e das instituições privadas de ensino”. Em nota, o Movimento Escolas Abertas, que reúne pais com essa bandeira, principalmente da rede particular, afirmou que a norma agora impede prefeitos de fechar os colégios. Esse, no entanto, não é o único entendimento possível do texto, já que o parágrafo 1º do artigo do decreto estadual em questão condiciona a retomada das aulas na rede estadual e privada à inexistência de ato fundamentado pela prefeitura em sentido contrário. Ou seja, o município pode vetar a reabertura, desde que embase a decisão. A interpretação de qualquer forma, deve ser alvo de disputa judicial. Como mostrou a Folha, escolas particulares de educação infantil preparam uma ofensiva judicial caso o prefeito Bruno Covas (PSDB) decida prorrogar o fechamento das unidades de ensino na capital paulista. Covas decidiu por medida mais restritiva do que a prevista pelo governo estadual para as escolas durante a fase emergencial. O prefeito proibiu qualquer atividade presencial nas unidades públicas e privadas do município até 4 de abril. Pelo plano estadual, as unidades de ensino podem continuar abertas, desde que atendam até 35% dos alunos matriculados, com a recomendação de restringir ao máximo as ações presenciais e atender só os alunos mais vulneráveis. A divergência entre o estado e a prefeitura da capital paulista vem desde o ano passado. Em setembro, o governo paulista liberou a volta às aulas presenciais, mas o município barrou, permitindo apenas atividades extracurriculares a partir de outubro. Representando pais de alunos da rede pública, o movimento Famílias Pela Vida criticou o decreto editado pela gestão Dória e reclamou que as famílias não foram consultadas para a edição da norma. “Essa decisão foi tomada depois de intenso lobby do Movimento Escolas Abertas, que representa famílias de escolas particulares e tem contatos privilegiados no meio político”, diz texto divulgado pelo grupo. Os integrantes do coletivo afirmam ser um escárnio priorizar a abertura de qualquer atividade em meio ao aumento de casos de Covid. Eles pedem educação remota de qualidade, com equipamentos para todos; auxílio emergencial; aumento da testagem; aquisição de vacinas e lockdown para frear o avanço da doença. O fechamento das escolas está associado a problemas de saúde mental para crianças e adolescentes, a lacunas de aprendizagem e a desigualdade educacional. Por outro lado, boletim epidemiológico recente da Secretaria estadual da Educação afirma que “a manutenção de baixas taxas de infecção na comunidade é fator crítico para manter as escolas abertas durante a pandemia”.")

	# Texto relacionado
	#articles.append("Embora impliquem em possibilidade de incidência da responsabilidade penal, os conceitos jurídicos de injúria racial e racismo são diferentes. O primeiro está contido no Código Penal brasileiro e o segundo, previsto na Lei nº 7.716/1989. Enquanto a injúria racial consiste em ofender a honra de alguém valendo-se de elementos referentes à raça, cor, etnia, religião ou origem, o crime de racismo atinge uma coletividade indeterminada de indivíduos, discriminando toda a integralidade de uma raça. Ao contrário da injúria racial, o crime de racismo é inafiançável e imprescritível. A injúria racial está prevista no artigo 140, parágrafo 3º, do Código Penal, que estabelece a pena de reclusão de um a três anos e multa, além da pena correspondente à violência, para quem cometê-la. De acordo com o dispositivo, injuriar seria ofender a dignidade ou o decoro utilizando elementos de raça, cor, etnia, religião, origem ou condição de pessoa idosa ou portadora de deficiência. Em geral, o crime de injúria está associado ao uso de palavras depreciativas referentes à raça ou cor com a intenção de ofender a honra da vítima. Um exemplo recente de injúria racial ocorreu no episódio em que torcedores do time do Grêmio, de Porto Alegre, insultaram um goleiro de raça negra chamando-o de “macaco” durante o jogo. No caso, o Ministério Público entrou com uma ação no Tribunal de Justiça do Rio Grande do Sul (TJRS), que aceitou a denúncia por injúria racial, aplicando, na ocasião, medidas cautelares como o impedimento dos acusados de frequentar estádios. Após um acordo no Foro Central de Porto Alegre, a ação por injúria foi suspensa. Já o crime de racismo, previsto na Lei nº 7.716/1989, implica em conduta discriminatória dirigida a um determinado grupo ou coletividade e, geralmente, refere-se a crimes mais amplos. Nesses casos, cabe ao Ministério Público a legitimidade para processar o ofensor. A lei enquadra uma série de situações como crime de racismo, por exemplo, recusar ou impedir acesso a estabelecimento comercial, impedir o acesso às entradas sociais em edifícios públicos ou residenciais e elevadores ou às escadas de acesso, negar ou obstar emprego em empresa privada, entre outros. De acordo com o promotor de Justiça do Tribunal de Justiça do Distrito Federal e Territórios (TJDFT) Thiago André Pierobom de Ávila, são mais comuns no País os casos enquadrados no artigo 20º da legislação, que consiste em “praticar, induzir ou incitar a discriminação ou preconceito de raça, cor, etnia, religião ou procedência nacional”. Apologia - Este mês, por exemplo, a 1ª Turma Criminal do TJDFT manteve uma condenação por crime de racismo de um homem que se autodenomina “skinhead” e que fez apologia ao racismo contra judeus, negros e nordestinos em página da internet. De acordo com os desembargadores, que mantiveram a condenação à unanimidade, “o crime de racismo é mais amplo do que o de injúria qualificada, pois visa a atingir uma coletividade indeterminada de indivíduos, discriminando toda a integralidade de uma raça. No caso, o conjunto probatório ampara a condenação do acusado por racismo”. Ao contrário da injúria racial, cuja prescrição é de oito anos – antes de transitar em julgado a sentença final –, o crime de racismo é inafiançável e imprescritível, conforme determina o artigo 5º da Constituição Federal. Apesar disso, de acordo com o promotor Pierobom, na prática é difícil comprovar o crime quando os vestígios já desapareceram e a memória enfraqueceu. O promotor lembra de um caso em que foi possível reconhecer o crime de racismo após décadas do ato praticado, o Habeas Corpus 82.424, julgado em 2003 no Supremo Tribunal Federal (STF), em que a corte manteve a condenação de um livro publicado com ideias preconceituosas e discriminatórias contra a comunidade judaica, considerando, por exemplo, que o holocausto não teria existido. A denúncia contra o livro foi feita em 1986 por movimentos populares de combate ao racismo e o STF manteve a condenação por considerar o crime de racismo imprescritível.")
	articles.append("Bicampeã olímpica, a central Fabiana foi às redes sociais em defesa do direito dos atletas de se manifestarem politicamente. Depois de a Confederação Brasileira de Vôlei divulgar uma nota de repúdio a Carol Solberg por encerrar uma entrevista ao vivo no domingo falando \"Fora Bolsonaro\" após conquistar a medalha de bronze da primeira etapa do Circuito Brasileiro de Vôlei de Praia ao lado de Talita, Fabiana defendeu o direito de qualquer pessoa expressar suas opiniões em um estado democrático. A central também criticou a CBV por utilizar o termo \"denegrir\" em sua nota, uma palavra de cunho racista. - Difícil entender o que aconteceu. Vamos por partes. Primeiro, denegrir é uma palavra de cunho racista e JAMAIS deveria ser usado em qualquer situação. Estamos lutando dia após dia contra atos racistas, fazendo campanhas educativas e protestos, então seria ótimo repensar o uso de certos termos. Com isso já deixo a dica de além de denegrir não usem “lista negra”, “mulata”, “mercado negro”, “a coisa tá preta”, “serviço de preto”, entre outras mais. Segundo, vivemos (ainda) em um país DEMOCRÁTICO, onde atletas ou qualquer ser humano pode expressar suas convicções, desde que elas não sejam ofensivas, criminosas ou que faltem com respeito. Temos que ter muito cuidado com a censura ou flerte com a volta dela, precisamos estar atentos aos nossos direitos enquanto cidadãos. Portanto, não foi muito feliz a nota escrita pela CBV. Eu como atleta preta, que muito conquistei e representei esse país em todo mundo, não posso me calar diante das coisas que vejo. Sempre vou apoiar a democracia, as liberdades individuais e especialmente todo apoio a causa contra o racismo estrutural e diário que ainda insistimos em conviver achando “normal”. #blacklivesmatter #vidaspretasimportam #liberdade O Globoesporte.com entrou em contato com a CBV sobre a postagem e o uso do termo denegrir na nota de repúdio, mas ainda não teve uma resposta. Muitos atletas do vôlei estão se posicionado sobre o caso, tanto a favor como contra a manifestação de Carol Solberg. A Comissão Nacional de Atletas do Vôlei de Praia da Confederação Brasileira de Vôlei soltou, nesta segunda-feira, uma nota oficial assinada pelo seu presidente, Emanuel Rego, criticando a fala de Carol, medalhista de bronze na primeira etapa do Circuito Nacional. - A Comissão Nacional de Atletas vem, através desta, ressaltar que não é favorável a nenhum tipo de manifestação de cunho político em competições esportivas. Por isso, a mesma lamenta o ato realizado pela atleta Carol Solberg neste domingo (20.09) - em jogo válido pela primeira etapa do Circuito Brasileiro Open de Vôlei de praia temporada 2020/21 - e lutaremos ao máximo para que esse tipo de situação não aconteça novamente - está escrito na nota oficial. Carol Solberg grita \"fora, Bolsonaro\" após o terceiro lugar no vôlei de praia Além da Comissão de atletas, a própria CBV se manifestou também em nota. Disse que é contra manifestações de cunho político e ressaltou ainda: \"Aproveitamos ainda para demonstrar toda nossa tristeza e insatisfação, tendo em vista que essa primeira etapa do CBVP OPEN 2020/2021, considerada um marco no retorno das competições dos esportes olímpicos, por tamanha importância, não poderia ser manchada por um ato totalmente impensado praticado pela referida atleta\". As finais disputadas no domingo, incluindo a decisão do terceiro lugar vencida pela dupla de Carol Solberg, marcaram a retomada do vôlei de praia brasileiro ainda durante a pandemia do coronavírus. Com estrutura e protocolos inspirados na bolha da NBA, atletas disputaram um torneio em isolamentos após testarem negativo para a Covid-19 no Centro de Treinamento da CBV, em Saquarema. 1 de 1 Carol Solberg na disputa de bronze do Circuito Brasileiro — Foto: CBV Carol Solberg na disputa de bronze do Circuito Brasileiro — Foto: CBV")
	return articles

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--prob", type=str,
						help="Calc racial term probability")
	parser.add_argument("-s", "--score", type=str,
						help="Score")
	parser.add_argument("-t", "--train", type=str,
						help="Train")
	parser.add_argument("-y", "--pred", type=str,
						help="Train")
	args = parser.parse_args()
	if (args.prob):
		print("calc_prob")
		calc_prob()
	elif (args.score):
		score_all()
	elif (args.train):
		train_nb()
	elif (args.pred):
		pass
	else:
		print("Wrong usage")