#!/usr/bin/env python
"""
Script para criar a tabela app_aboutcompany manualmente
"""
import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from django.db import connection
from app.models import AboutCompany

def create_aboutcompany_table():
    """Cria a tabela app_aboutcompany manualmente"""
    
    with connection.cursor() as cursor:
        # Verificar se a tabela já existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'app_aboutcompany'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            print("Tabela app_aboutcompany já existe!")
            return
        
        # Criar a tabela app_aboutcompany
        cursor.execute("""
            CREATE TABLE app_aboutcompany (
                id BIGSERIAL PRIMARY KEY,
                ac_content TEXT NOT NULL,
                gallery_title VARCHAR(200),
                language VARCHAR(5) NOT NULL DEFAULT 'pt',
                parent_id BIGINT REFERENCES app_aboutcompany(id)
            );
        """)
        
        # Criar a sequência para o ID
        cursor.execute("""
            CREATE SEQUENCE IF NOT EXISTS app_aboutcompany_id_seq
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1;
        """)
        
        # Definir a sequência como propriedade da coluna id
        cursor.execute("""
            ALTER TABLE app_aboutcompany ALTER COLUMN id SET DEFAULT nextval('app_aboutcompany_id_seq');
            ALTER SEQUENCE app_aboutcompany_id_seq OWNED BY app_aboutcompany.id;
        """)
        
        print("Tabela app_aboutcompany criada com sucesso!")

if __name__ == '__main__':
    create_aboutcompany_table()

    about = AboutCompany.objects.get(id=1)  # ou o id correto
    about.ac_content = """<h2>Manifesto da Agropecuária AH</h2>
    <p>Na Agropecuária AH, acreditamos que produzir alimentos é mais do que uma atividade econômica — é um compromisso com a terra, as pessoas e as futuras gerações. Nossa Missão é "Cultivar o solo, produzir e comercializar bons alimentos, desenvolvendo as pessoas e a terra". Nossos valores – responsabilidade, transparência, humildade, respeito e empatia – orientam tudo o que fazemos, guiando nossa conduta em todas as situações. 
    Minha história se confunde com a da Agropecuária AH, e é com alegria que hoje vejo meus filhos e netos participando desse mesmo sonho ao lado de uma equipe que cresceu conosco ao longo de décadas. Temos orgulho dessa história, construída com trabalho, resiliência e inovação. Em todas as fases, buscamos aumentar a produtividade com responsabilidade e manter nossas fazendas organizadas, sustentáveis e produtivas.
    Valorizamos profundamente nossas raízes. Pecuária, suinocultura, cafeicultura e agricultura fazem parte do nosso caminho, sempre guiado pela paixão pela terra e pelo respeito aos ciclos da natureza. Tomamos decisões com visão de longo prazo, mesmo quando isso significa abrir mão de ganhos imediatos em nome de princípios que consideramos inegociáveis.
    Tenho também muito orgulho da Fundação AH — gerida por minha família com o apoio de voluntários e profissionais dedicados. Quando observo as crianças da fundação, tenho a certeza de que estamos contribuindo para um futuro melhor.
    Helder Höfig
    """
    about.save() 