#!/usr/bin/env python3
"""
Script para criar a notícia sobre a novilhada Angus
Baseado no artigo: https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses
"""

import os
import sys
import django
from datetime import datetime
from django.utils.text import slugify

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News

def criar_noticia_angus():
    """Cria a notícia sobre a novilhada Angus"""
    
    # Dados da notícia
    titulo = "Novilhada Angus surpreende por ganhar 1 arroba por mês - 17,5 arrobas aos 17 meses"
    
    # Gerar slug único com timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug_base = slugify(titulo)
    slug = f"{slug_base}-{timestamp}"
    
    # Verificar se já existe uma notícia com este slug
    counter = 1
    while News.objects.filter(news_slug=slug).exists():
        slug = f"{slug_base}-{timestamp}-{counter}"
        counter += 1
    
    # Conteúdo da notícia
    conteudo = """
    <h2>Novilhada Angus da Agropecuária AH alcança resultados excepcionais</h2>
    
    <p>A Agropecuária AH tem se destacado no cenário da pecuária brasileira com resultados impressionantes em sua criação de novilhas Angus. Recentemente, o rebanho surpreendeu ao alcançar um ganho médio de <strong>1 arroba por mês</strong>, resultando em animais com <strong>17,5 arrobas aos 17 meses de idade</strong>.</p>
    
    <h3>Metodologia de Sucesso</h3>
    
    <p>O excelente desempenho é resultado de uma combinação de fatores técnicos e genéticos:</p>
    
    <ul>
        <li><strong>Melhoramento Genético:</strong> Seleção rigorosa de reprodutores com características superiores</li>
        <li><strong>Pastoreio Voisin Racional:</strong> Sistema de pastejo que otimiza o uso das pastagens</li>
        <li><strong>Confinamento Estratégico:</strong> Períodos de confinamento para maximizar o ganho de peso</li>
        <li><strong>Protocolo 1953:</strong> Adesão rigorosa aos padrões de qualidade e certificação</li>
    </ul>
    
    <h3>Resultados Alcançados</h3>
    
    <p>Os números falam por si só:</p>
    
    <ul>
        <li>Ganho médio: <strong>1 arroba por mês</strong></li>
        <li>Peso final: <strong>17,5 arrobas aos 17 meses</strong></li>
        <li>Eficiência alimentar: Otimizada através do sistema Voisin</li>
        <li>Qualidade da carne: Superior, atendendo aos mais altos padrões</li>
    </ul>
    
    <h3>Compromisso com a Excelência</h3>
    
    <p>A Agropecuária AH mantém seu compromisso com a excelência na pecuária, investindo continuamente em:</p>
    
    <ul>
        <li>Tecnologia de ponta</li>
        <li>Melhoramento genético</li>
        <li>Sustentabilidade</li>
        <li>Qualidade total</li>
    </ul>
    
    <p>Estes resultados demonstram que é possível alcançar alta produtividade mantendo os mais altos padrões de qualidade e bem-estar animal, posicionando a Agropecuária AH como referência no setor pecuário brasileiro.</p>
    """
    
    try:
        # Criar a notícia usando o método correto
        noticia = News(
            news_date=datetime.now(),
            news_title=titulo,
            news_slug=slug,
            news_description=conteudo,
            news_video="",  # Campo opcional
            news_galery_title="Galeria de Imagens"
        )
        noticia.save()
        
        print(f"✅ Notícia criada com sucesso!")
        print(f"📰 Título: {noticia.news_title}")
        print(f"🔗 Slug: {noticia.news_slug}")
        print(f"📅 Data: {noticia.news_date}")
        print(f"🆔 ID: {noticia.id}")
        
        return noticia
        
    except Exception as e:
        print(f"❌ Erro ao criar notícia: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Criando notícia sobre a novilhada Angus...")
    noticia = criar_noticia_angus()
    
    if noticia:
        print("\n🎉 Notícia criada com sucesso!")
        print("🌐 Acesse: http://127.0.0.1:8000/ para ver o site")
        print("🔧 Admin: http://127.0.0.1:8000/admin/ para gerenciar conteúdo")
    else:
        print("\n❌ Falha ao criar a notícia")
        sys.exit(1)
