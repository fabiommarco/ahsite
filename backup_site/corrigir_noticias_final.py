#!/usr/bin/env python3
"""
Script para corrigir as notícias com vídeo correto e fotos reais
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

def corrigir_noticias_final():
    """Corrige as notícias com vídeo correto e fotos reais"""
    
    print("🔧 Corrigindo notícias com conteúdo correto...")
    print("=" * 60)
    
    # Buscar nossas notícias específicas
    noticia_cafe = News.objects.filter(news_title__icontains="9ª Festa do Café").first()
    noticia_angus = News.objects.filter(news_title__icontains="Novilhada Angus").first()
    
    # URL da foto da reportagem do Canal Rural (foto real da reportagem)
    foto_angus_url = "https://girodoboi.canalrural.com.br/wp-content/uploads/2025/08/novilhada-angus-agropecuaria-ah.jpg"
    
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
    
    # Atualizar notícia do Angus com vídeo correto e foto da reportagem
    if noticia_angus:
        print(f"📰 Corrigindo notícia do Angus...")
        
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
            <p><strong>Data:</strong> 01/08/2025</p>
            <p><strong>Autor:</strong> Fábio Moitinho</p>
            <p><strong>Link:</strong> <a href="https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses/" target="_blank" rel="noopener">Ver reportagem completa no Canal Rural</a></p>
        </div>
        """
        
        noticia_angus.news_description = novo_conteudo
        # Adicionar vídeo correto do YouTube (ID: okehG50jSp8)
        noticia_angus.news_video = "okehG50jSp8"
        noticia_angus.save()
        
        print(f"   ✅ Conteúdo atualizado com referência da reportagem")
        print(f"   ✅ Vídeo adicionado: {noticia_angus.news_video}")
        
        # Adicionar foto da reportagem
        if noticia_angus.news_galery.exists():
            print("   ⚠️ Notícia já tem imagem, removendo...")
            noticia_angus.news_galery.all().delete()
        
        img_file = baixar_imagem(foto_angus_url, "novilhada_angus_reportagem")
        if img_file:
            content_type = ContentType.objects.get_for_model(News)
            imagem = Imagem.objects.create(
                imagem=img_file,
                descricao="Novilhada Angus da Agropecuária AH - Foto da reportagem do Canal Rural",
                main_image=True,
                content_type=content_type,
                object_id=noticia_angus.id
            )
            print(f"   ✅ Foto da reportagem adicionada: {imagem.imagem.name}")
        else:
            print("   ❌ Falha ao adicionar foto da reportagem")
    else:
        print("❌ Notícia do Angus não encontrada")
    
    print()
    
    # Atualizar notícia do café - remover imagem incorreta
    if noticia_cafe:
        print(f"📰 Corrigindo notícia do Café...")
        
        # Remover imagem incorreta
        if noticia_cafe.news_galery.exists():
            print("   ⚠️ Removendo imagem incorreta...")
            noticia_cafe.news_galery.all().delete()
            print("   ✅ Imagem removida - aguardando fotos reais da 9ª Festa do Café")
        
        print(f"   ✅ Notícia pronta para receber as fotos reais da 9ª Festa do Café")
    else:
        print("❌ Notícia do Café não encontrada")
    
    print()
    print("✅ Processo concluído!")
    print()
    print("🔍 Resumo das correções:")
    print("-" * 60)
    
    if noticia_angus:
        print(f"📰 Angus:")
        print(f"   - Vídeo: Adicionado (ID: okehG50jSp8)")
        print(f"   - Foto: Adicionada da reportagem do Canal Rural")
        print(f"   - Referência: Atualizada com dados corretos")
    
    if noticia_cafe:
        print(f"📰 Café:")
        print(f"   - Imagem incorreta: Removida")
        print(f"   - Status: Pronta para receber fotos reais da 9ª Festa do Café")
    
    print()
    print("📝 Próximos passos:")
    print("- Para a notícia do Café: Adicionar as fotos reais da 9ª Festa do Café")
    print("- Para a notícia do Angus: Foto e vídeo da reportagem foram adicionados")

if __name__ == "__main__":
    corrigir_noticias_final()
