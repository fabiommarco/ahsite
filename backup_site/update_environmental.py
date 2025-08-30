import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import EnvironmentalResponsability

texto = '''<b>Agroenergia: Preservação e Responsabilidade Socioambiental</b><br><br>
Na atualidade, a questão ambiental permeia todas as atividades desenvolvidas por qualquer empresa. É dever das empresas zelar pela sanidade ambiental, através do desenvolvimento de técnicas cada vez mais limpas e com melhor retorno socioambiental para sua comunidade abrangente.<br><br>
Neste viés, a Agropecuária AH vem inovando e aprimorando seus métodos de produção para ser uma empresa cada vez mais sustentável.<br><br>
A AH possui um projeto de autossuficiência energética, baseado no aproveitamento dos dejetos suínos para a produção de biogás por meio de biodigestores e geração de energia elétrica. Além da eletricidade, o processo resulta em biofertilizante para o uso em pastagem e na agricultura.<br><br>
Desta forma, a AH utiliza ao máximo seu potencial energético e garante que, além de cumprir toda a legislação, seus resíduos são reaproveitados, evitando riscos ao meio ambiente.<br><br>
Na Agropecuária AH, os dejetos da suinocultura não são passivos ambientais, e sim insumos para suprir suas demandas energéticas e de fertilização do solo.<br><br>
<b>Monitoramento ambiental</b><br><br>
A Agropecuária AH realiza monitoramento contínuo da qualidade ambiental em suas propriedades visando a preservação do meio ambiente.<br><br>
São coletadas amostras de solo, água, efluentes e das culturas para controle dos riscos de contaminação. Todos os processos são acompanhados por profissionais da área ambiental.<br><br>
<b>Compostagem</b><br><br>
Visando o aproveitamento do potencial energético e produtivo, a Agropecuária AH investe no desenvolvimento do próprio composto orgânico com o intuito de aproveitar os resíduos provenientes das atividades desenvolvidas. Sejam eles dejetos suínos, casca de café, esterco de confinamento ou restos de colheitas, tudo é analisado para a formulação de um composto orgânico que, diferentemente dos fertilizantes comuns que trabalham apenas na linha da nutrição, também contribui para o desenvolvimento de uma fauna microbiótica e prolonga a disponibilidade de nutrientes no solo. Além da contribuição ambiental, uma vez que diminui a exploração dos recursos naturais e gera uma destinação adequada para os resíduos, há ainda uma diminuição dos custos e a melhoria da condição natural do solo no médio e longo prazo.<br><br>
<b>Controle das atividades produtivas e de preservação</b><br><br>
A Agropecuária AH conta com um eficiente sistema de gestão que possibilita o controle em tempo real de todas as suas atividades produtivas, utilizando índices de produtividade e qualidade, evitando desperdícios de insumos e consequente risco de contaminação.<br><br>
Além disso, todas as propriedades contam com um complexo mapeamento das áreas de produção e de preservação ambiental, racionalizando recursos e localizando o potencial de cada área. Isso auxilia na identificação das possíveis alterações na paisagem, permitindo uma ação rápida e localizada das equipes.<br><br>
<b>Conscientização ambiental</b><br><br>
Além das atividades de cunho ambiental desenvolvidas pela Fundação AH como o reaproveitamento de material reciclado, os funcionários recebem treinamento para manejo e disposição adequadas dos resíduos gerados, tanto nos escritórios quanto nas áreas produtivas e nas colônias. A separação dos resíduos é estimulada e todo o material orgânico gerado é destinado para a adubação do solo.<br><br>
A empresa não utiliza materiais descartáveis em seu dia a dia: tomar café ou água somente em canecas e xícaras, diminuindo a utilização de plástico e a quantidade de resíduo gerado.<br><br>
Nas rotinas do escritório, a impressão de documentos é realizada somente em último caso, dando prioridade para a troca e armazenagem de arquivos digitais.'''

try:
    environmental = EnvironmentalResponsability.objects.latest('id')
    environmental.environ_description = texto
    environmental.save()
    print("Registro atualizado com sucesso!")
except EnvironmentalResponsability.DoesNotExist:
    print("Nenhum registro encontrado para atualizar.") 