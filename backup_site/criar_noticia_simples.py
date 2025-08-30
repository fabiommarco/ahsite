#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simples para criar notícia sobre novilhada Angus da Agropecuária AH
Insere diretamente no banco SQLite
"""

import sqlite3
import datetime
import re
from urllib.parse import quote

def slugify(text):
    """Cria um slug a partir do texto"""
    # Remove acentos e caracteres especiais
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def criar_noticia_angus():
    """Cria notícia sobre a novilhada Angus da Agropecuária AH"""
    
    # Dados da notícia baseados no link fornecido
    titulo = "Novilhada Angus da Agropecuária AH surpreende com ganho de 1 arroba por mês"
    
    descricao = """
    <h2>Novilhada Angus impressiona com 17,5 arrobas aos 17 meses</h2>
    
    <p>A <strong>Agropecuária AH</strong>, através da <strong>Fazenda Córrego Azul</strong> em <strong>Brasilândia (MS)</strong>, está chamando atenção no setor pecuário com resultados excepcionais em sua criação de novilhas Angus.</p>
    
    <h3>Resultados Impressionantes</h3>
    
    <p>O pecuarista <strong>Helder Hofig</strong> e sua equipe conseguiram um feito notável: suas novilhas Angus estão ganhando <strong>uma arroba por mês</strong>, alcançando <strong>17,5 arrobas aos 17 meses de idade</strong>.</p>
    
    <p>Esses resultados foram apresentados pelo <strong>Alexandre Scaff Raffi</strong>, gerente da unidade CPG da Friboi de Campo Grande (MS), que destacou a qualidade excepcional do lote de novilhas Angus crioulas da fazenda.</p>
    
    <h3>Sistema de Produção</h3>
    
    <p>O sucesso é resultado de um sistema integrado que inclui:</p>
    
    <ul>
        <li><strong>Melhoramento genético intra-rebanho</strong> com acompanhamento do professor doutor José Bento Ferraz da USP de Pirassununga</li>
        <li><strong>Pastoreio Racional Voisin</strong> para a fase de cria</li>
        <li><strong>Confinamento</strong> para terminação</li>
        <li>Aprovação no <strong>Protocolo 1953</strong> da Friboi</li>
    </ul>
    
    <h3>Protocolo 1953</h3>
    
    <p>O Protocolo 1953, lançado em 2018, privilegia pecuaristas que trabalham para obter animais que garantem carne macia, saborosa e suculenta. Entre os requisitos estão:</p>
    
    <ul>
        <li>Mínimo de 50% de sangue de raças taurinas</li>
        <li>Machos castrados com até dois dentes incisivos</li>
        <li>Novilhas com até quatro dentes</li>
        <li>Maturidade e acabamento adequados</li>
    </ul>
    
    <h3>Reconhecimento da Qualidade</h3>
    
    <p>Essa novilhada representa o que há de mais moderno na pecuária brasileira, demonstrando que investimento em genética, manejo adequado e tecnologia podem resultar em produtos de altíssima qualidade, valorizando tanto o produtor quanto o consumidor final.</p>
    
    <p>A <strong>Agropecuária AH</strong> continua se destacando como referência em pecuária de precisão e qualidade no Mato Grosso do Sul.</p>
    """
    
    # Criar slug a partir do título
    slug = slugify(titulo)
    
    # Data atual
    data_atual = datetime.datetime.now()
    
    try:
        # Conectar ao banco SQLite
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Verificar se a tabela app_news existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_news'")
        if not cursor.fetchone():
            print("❌ Tabela app_news não encontrada!")
            return None
        
        # Verificar a estrutura da tabela
        cursor.execute("PRAGMA table_info(app_news)")
        columns = cursor.fetchall()
        print("📋 Estrutura da tabela app_news:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - NOT NULL: {col[3]}")
        
        # Inserir a notícia com todos os campos necessários
        cursor.execute("""
            INSERT INTO app_news (
                news_date, 
                news_title, 
                news_slug, 
                news_description, 
                news_video,
                news_galery_title,
                language, 
                parent_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data_atual, 
            titulo, 
            slug, 
            descricao, 
            '',  # news_video vazio
            'Galeria de Imagens',  # news_galery_title
            'pt', 
            None  # parent_id
        ))
        
        # Obter o ID da notícia criada
        noticia_id = cursor.lastrowid
        
        # Commit das alterações
        conn.commit()
        conn.close()
        
        print(f"✅ Notícia criada com sucesso!")
        print(f"📰 ID: {noticia_id}")
        print(f"📰 Título: {titulo}")
        print(f"🔗 Slug: {slug}")
        print(f"📅 Data: {data_atual}")
        print(f"🌐 Idioma: pt")
        
        return noticia_id
        
    except Exception as e:
        print(f"❌ Erro ao criar notícia: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Criando notícia sobre novilhada Angus da Agropecuária AH...")
    print("📝 Baseado nas informações do Giro do Boi")
    print("🔗 Fonte: https://girodoboi.canalrural.com.br/pecuaria/certificacoes-e-qualidade/novilhada-angus-surpreende-por-ganhar-1-arroba-por-mes-175-arrobas-aos-17-meses")
    print()
    
    noticia_id = criar_noticia_angus()
    
    if noticia_id:
        print("\n🎉 Notícia criada com sucesso no banco de dados!")
        print("📝 A notícia está disponível no sistema.")
        print("💡 Para visualizar, acesse o painel administrativo do Django.")
    else:
        print("\n💥 Falha ao criar a notícia.")
        exit(1)
