#!/usr/bin/env python3
"""
Script para adicionar imagens, vídeo e referência da reportagem às notícias
"""

import os
import sys
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import News, Imagem
from django.contrib.contenttypes.models import ContentType

def adicionar_imagens_e_video():
    """Adiciona imagens, vídeo e referência da reportagem às notícias"""
    
    print("🖼️ Adicionando imagens, vídeo e referências...")
    print("=" * 60)
    
    # Buscar nossas notícias específicas
    noticia_cafe = News.objects.filter(news_title__icontains="9ª Festa do Café").first()
    noticia_angus = News.objects.filter(news_title__icontains="Novilhada Angus").first()
    
    # URLs de imagens de exemplo
    imagem_cafe_url = "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=800&h=600&fit=crop"
    imagem_angus_url = "https://images.unsplash.com/photo-1500595046743-cd271d694e30?w=800&h=600&fit=crop"
    
    def baixar_imagem(url, nome_arquivo):
        """Baixa uma imagem da URL e retorna um arquivo temporário"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Criar arquivo temporário
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            
            return File(img_temp, name=f"{nome_arquivo}.jpg")
        except Exception as e:
            print(f"❌ Erro ao baixar imagem: {e}")
            return None
    
    # Atualizar notícia do Angus com vídeo e referência
    if noticia_angus:
        print(f"📰 Atualizando notícia do Angus...")
        
        # Atualizar o conteúdo com referência da reportagem
        novo_conteudo = """
        <h2>Novilhada Angus da Agropecuária AH alcança resultados excepcionais</h2>
        
        <p>A Agropecuária AH tem se destacado no cenário da pecuária brasileira com resultados impressionantes em sua criação de novilhas Angus. Recentemente, o rebanho surpreendeu ao alcançar um ganho médio de <strong>1 arroba por mês</strong>, atingindo <strong>17,5 arrobas aos 17 meses</strong>.</p>
        
        <h3>Resultados Excepcionais</h3>
        <p>Este resultado coloca a Agropecuária AH entre as propriedades de referência na criação de bovinos Angus no Brasil. O ganho de peso consistente demonstra a excelência em genética, nutrição e manejo aplicados na propriedade.</p>
        
        <h3>Fatores do Sucesso</h3>
        <p>O sucesso é resultado de uma combinação de fatores:</p>
        <ul>
            <li><strong>Genética de qualidade:</strong> Seleção rigorosa de reprodutores</li>
            <li><strong>Nutrição balanceada:</strong> Dieta específica para cada fase</li>
            <li><strong>Manejo adequado:</strong> Cuidados sanitários e ambientais</li>
            <li><strong>Monitoramento constante:</strong> Acompanhamento de indicadores</li>
        </ul>
        
        <h3>Reconhecimento Nacional</h3>
        <p>Estes resultados têm chamado a atenção de especialistas e produtores de todo o país, consolidando a Agropecuária AH como referência na pecuária de corte brasileira.</p>
        
        <div class="alert alert-info" style="margin: 2rem 0; padding: 1.5rem; border-left: 4px solid #17a2b8;">
            <h4><i class="fas fa-newspaper"></i> Reportagem Original</h4>
            <p><strong>Fonte:</strong> Canal Rural - Giro do Boi</p>
            <p><strong>Data:</strong> Agosto de 2025</p>
            <p><strong>Link:</strong> <a href="https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses" target="_blank" rel="noopener">Ver reportagem completa no Canal Rural</a></p>
        </div>
        """
        
        noticia_angus.news_description = novo_conteudo
        noticia_angus.news_video = "aAkurCTifE0"  # ID do vídeo do YouTube (exemplo)
        noticia_angus.save()
        
        print(f"   ✅ Conteúdo atualizado com referência da reportagem")
        print(f"   ✅ Vídeo adicionado: {noticia_angus.news_video}")
        
        # Adicionar imagem
        if noticia_angus.news_galery.exists():
            print("   ⚠️ Notícia já tem imagem, removendo...")
            noticia_angus.news_galery.all().delete()
        
        img_file = baixar_imagem(imagem_angus_url, "novilhada_angus")
        if img_file:
            content_type = ContentType.objects.get_for_model(News)
            imagem = Imagem.objects.create(
                imagem=img_file,
                descricao="Novilhada Angus da Agropecuária AH",
                main_image=True,
                content_type=content_type,
                object_id=noticia_angus.id
            )
            print(f"   ✅ Imagem adicionada: {imagem.imagem.name}")
        else:
            print("   ❌ Falha ao adicionar imagem")
    else:
        print("❌ Notícia do Angus não encontrada")
    
    print()
    
    # Atualizar notícia do café
    if noticia_cafe:
        print(f"📰 Atualizando notícia do Café...")
        
        # Atualizar o conteúdo
        novo_conteudo = """
        <h2>9ª Festa do Café da Fazenda Ouro Verde: Renovação e Celebração</h2>
        
        <p>No último dia <strong>16 de Agosto</strong> celebramos, na fazenda Ouro Verde, nossa <strong>9ª Festa do Café</strong>. Com ela, renovamos nossas energias, encerramos um ciclo e já iniciamos outro.</p>
        
        <h3>Um Momento de Conquistas e Reflexão</h3>
        <p>Regada a muita comida, música e diversão, celebramos nossas conquistas. No ano em que a fazenda Ouro Verde completa 10 anos, aproveitamos esse momento para refletir: nada na fazenda funciona por si só, mas é sempre o resultado de interações complexas entre os elementos naturais solo, plantas, animais e seres humanos. Todos estes elementos são partes integrantes da fazenda e devem ser geridos juntos para garantir o bem estar do todo, formando o organismo agrícola.</p>
        
        <h3>Reconhecimento e Propósito</h3>
        <p>Com esse espírito, também realizamos nessa oportunidade a premiação por tempo de serviço aos nossos trabalhadores, que dedicam parte de sua vida para que nossa empresa e nosso país caminhem para frente.</p>
        
        <p>Agradecemos a todos envolvidos e seguimos em busca de nosso propósito: desfrutamos de sistemas de produção rentáveis que promovem a regeneração do solo e a qualidade de vida das pessoas.</p>
        
        <div class="alert alert-success" style="margin: 2rem 0; padding: 1.5rem; border-left: 4px solid #28a745;">
            <h4><i class="fas fa-calendar-check"></i> Evento Realizado</h4>
            <p><strong>Data:</strong> 16 de Agosto de 2025</p>
            <p><strong>Local:</strong> Fazenda Ouro Verde</p>
            <p><strong>Participantes:</strong> Equipe AH, parceiros e comunidade local</p>
        </div>
        """
        
        noticia_cafe.news_description = novo_conteudo
        noticia_cafe.save()
        
        print(f"   ✅ Conteúdo atualizado")
        
        # Adicionar imagem
        if noticia_cafe.news_galery.exists():
            print("   ⚠️ Notícia já tem imagem, removendo...")
            noticia_cafe.news_galery.all().delete()
        
        img_file = baixar_imagem(imagem_cafe_url, "festa_cafe")
        if img_file:
            content_type = ContentType.objects.get_for_model(News)
            imagem = Imagem.objects.create(
                imagem=img_file,
                descricao="9ª Festa do Café da Fazenda Ouro Verde",
                main_image=True,
                content_type=content_type,
                object_id=noticia_cafe.id
            )
            print(f"   ✅ Imagem adicionada: {imagem.imagem.name}")
        else:
            print("   ❌ Falha ao adicionar imagem")
    else:
        print("❌ Notícia do Café não encontrada")
    
    print()
    print("✅ Processo concluído!")
    print()
    print("🔍 Resumo das atualizações:")
    print("-" * 60)
    
    if noticia_angus:
        print(f"📰 Angus:")
        print(f"   - Vídeo: {noticia_angus.news_video}")
        print(f"   - Imagens: {noticia_angus.news_galery.count()}")
        print(f"   - Referência da reportagem: Adicionada")
    
    if noticia_cafe:
        print(f"📰 Café:")
        print(f"   - Imagens: {noticia_cafe.news_galery.count()}")
        print(f"   - Conteúdo: Atualizado")

if __name__ == "__main__":
    adicionar_imagens_e_video()
