#!/usr/bin/env python
import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ahsite.settings')
django.setup()

from app.models import AboutCompany

CONTEUDO_COM_IDS = '''<h2 id="sobre-nos" class="titulo-institucional">Sobre a Agropecuária AH</h2>
<div class="row g-4 mb-5">
<div class="col-lg-8">
<div class="card border-0 shadow-sm h-100">
<div class="card-body p-4">
<h3 class="text-success fw-bold mb-3">Nossa História</h3>
<p class="lead">Nossa história teve início em 1950, através do Sr. ARTHUR HÖFFIG, quando realizou aquisição de uma gleba de terras localizadas no município de Brasilândia, que na época fazia parte do Estado de Mato Grosso, que hoje é Mato Grosso do Sul.</p>
<p>A primeira fazenda aberta foi denominada de Boa Esperança. Já no ano de 1973 realiza-se abertura da Fazenda Córrego Azul, berço das atividades da Agropecuária AH.</p>
<p>Pensando no desenvolvimento da região, o Sr Arthur contratou a empresa Coterp e destinou 30 alqueires para edificar a cidade, que é Brasilândia.</p>
<p>E, no decorrer das três últimas décadas, entre desafios, ímpeto inovador e empreendedorismo, moldamos nosso crescimento e evoluímos nosso desempenho.</p>
<p>Desde então, a Agropecuária AH, vem ampliando suas unidades de produção e área de produção, expandindo sua atuação aos Estados do Mato Grosso, Minas Gerais e Goiás.</p>
</div>
</div>
</div>
<div class="col-lg-4">
<div class="card border-0 shadow-sm h-100 bg-success text-white">
<div class="card-body p-4 text-center">
<h4 class="fw-bold mb-3">Negócio</h4>
<p class="display-6 fw-bold">Agropecuária</p>
</div>
</div>
</div>
</div>

<div class="row g-4 mb-5">
<div class="col-md-6">
<div class="card border-0 shadow-sm h-100">
<div class="card-body p-4 text-center">
<h3 class="text-success fw-bold mb-3">Nossa Missão</h3>
<blockquote class="blockquote">
<p class="mb-0 fst-italic">"Cultivar o solo, produzir e comercializar bons alimentos, desenvolvendo as pessoas e a terra"</p>
</blockquote>
</div>
</div>
</div>
<div class="col-md-6">
<div class="card border-0 shadow-sm h-100">
<div class="card-body p-4 text-center">
<h3 class="text-success fw-bold mb-3">Nossa Visão 2027</h3>
<blockquote class="blockquote">
<p class="mb-0 fst-italic">"Seremos referência na produção de alimentos de qualidade, com equilíbrio económico, social e ambiental."</p>
</blockquote>
</div>
</div>
</div>
</div>

<div class="row g-4 mb-5">
<div class="col-md-6">
<div class="card border-0 shadow-sm h-100">
<div class="card-body p-4">
<h3 class="text-success fw-bold mb-3">Produtos</h3>
<div class="row g-2">
<div class="col-6">
<div class="d-flex align-items-center p-2 bg-light rounded">
<i class="fas fa-cow text-success me-2"></i>
<span>Bovinos</span>
</div>
</div>
<div class="col-6">
<div class="d-flex align-items-center p-2 bg-light rounded">
<i class="fas fa-piggy-bank text-success me-2"></i>
<span>Suínos</span>
</div>
</div>
<div class="col-6">
<div class="d-flex align-items-center p-2 bg-light rounded">
<i class="fas fa-coffee text-success me-2"></i>
<span>Café</span>
</div>
</div>
<div class="col-6">
<div class="d-flex align-items-center p-2 bg-light rounded">
<i class="fas fa-seedling text-success me-2"></i>
<span>Grãos</span>
</div>
</div>
</div>
</div>
</div>
</div>
<div class="col-md-6">
<div class="card border-0 shadow-sm h-100">
<div class="card-body p-4">
<h3 class="text-success fw-bold mb-3">Clientes</h3>
<ul class="list-unstyled">
<li class="mb-2"><i class="fas fa-building text-success me-2"></i>Frigoríficos de Bovinos e Suínos</li>
<li class="mb-2"><i class="fas fa-industry text-success me-2"></i>Torrefadoras e Exportadores de Café</li>
<li class="mb-2"><i class="fas fa-truck text-success me-2"></i>Comerciantes e Exportadores de Grãos</li>
</ul>
</div>
</div>
</div>
</div>

<h2 id="manifesto" class="titulo-institucional">Manifesto da Agropecuária AH</h2>
<div class="card border-0 shadow-sm mb-5">
<div class="card-body p-4">
<div class="row">
<div class="col-lg-10">
<p class="lead mb-4">Na Agropecuária AH, acreditamos que produzir alimentos é mais do que uma atividade econômica — é um compromisso com a terra, as pessoas e as futuras gerações. Nossa Missão é "Cultivar o solo, produzir e comercializar bons alimentos, desenvolvendo as pessoas e a terra". Nossos valores – responsabilidade, transparência, humildade, respeito e empatia – orientam tudo o que fazemos, guiando nossa conduta em todas as situações.</p>
<p>Minha história se confunde com a da Agropecuária AH, e é com alegria que hoje vejo meus filhos e netos participando desse mesmo sonho ao lado de uma equipe que cresceu conosco ao longo de décadas. Temos orgulho dessa história, construída com trabalho, resiliência e inovação. Em todas as fases, buscamos aumentar a produtividade com responsabilidade e manter nossas fazendas organizadas, sustentáveis e produtivas.</p>
<p>Valorizamos profundamente nossas raízes. Pecuária, suinocultura, cafeicultura e agricultura fazem parte do nosso caminho, sempre guiado pela paixão pela terra e pelo respeito aos ciclos da natureza. Tomamos decisões com visão de longo prazo, mesmo quando isso significa abrir mão de ganhos imediatos em nome de princípios que consideramos inegociáveis.</p>
<p>Tenho também muito orgulho da Fundação AH — gerida por minha família com o apoio de voluntários e profissionais dedicados. Quando observo as crianças da fundação, tenho a certeza de que estamos contribuindo para um futuro melhor.</p>
</div>
<div class="col-lg-2 text-center">
<div class="border-start border-success ps-3">
<p class="fw-bold text-success mb-1">Helder Höfig</p>
<p class="small text-muted">Presidente</p>
</div>
</div>
</div>
</div>
</div>

<h2 id="valores-detalhados" class="titulo-institucional">Nossos Valores</h2>
<div class="row g-4 mb-5">
<div class="col-md-6 col-lg-4">
<div class="card h-100 border-0 shadow-sm hover-card">
<div class="card-body p-4 text-center">
<div class="mb-3">
<i class="fas fa-handshake fa-2x text-success"></i>
</div>
<h4 class="fw-bold text-success">RESPONSABILIDADE</h4>
<p class="mb-0">Respondemos por nossas ações, assumindo as consequências das nossas decisões.</p>
</div>
</div>
</div>
<div class="col-md-6 col-lg-4">
<div class="card h-100 border-0 shadow-sm hover-card">
<div class="card-body p-4 text-center">
<div class="mb-3">
<i class="fas fa-eye fa-2x text-success"></i>
</div>
<h4 class="fw-bold text-success">TRANSPARÊNCIA</h4>
<p class="mb-0">Falamos sempre a verdade para nossos clientes, fornecedores, trabalhadores, parceiros, comunidade e demais partes interessadas. Priorizamos a clareza em todos os processos e comunicações.</p>
</div>
</div>
</div>
<div class="col-md-6 col-lg-4">
<div class="card h-100 border-0 shadow-sm hover-card">
<div class="card-body p-4 text-center">
<div class="mb-3">
<i class="fas fa-heart fa-2x text-success"></i>
</div>
<h4 class="fw-bold text-success">HUMILDADE</h4>
<p class="mb-0">Temos consciência das nossas limitações e não nos consideramos superiores aos outros. Reconhecemos que sempre há espaço para aprender, melhorar e crescer.</p>
</div>
</div>
</div>
<div class="col-md-6 col-lg-4">
<div class="card h-100 border-0 shadow-sm hover-card">
<div class="card-body p-4 text-center">
<div class="mb-3">
<i class="fas fa-users fa-2x text-success"></i>
</div>
<h4 class="fw-bold text-success">RESPEITO</h4>
<p class="mb-0">Trabalhamos de forma colaborativa, tratando as pessoas, os animais e o meio ambiente com dignidade e calor humano. Valorizamos a diversidade de ideias e culturas em todas as relações.</p>
</div>
</div>
</div>
<div class="col-md-6 col-lg-4">
<div class="card h-100 border-0 shadow-sm hover-card">
<div class="card-body p-4 text-center">
<div class="mb-3">
<i class="fas fa-hands-helping fa-2x text-success"></i>
</div>
<h4 class="fw-bold text-success">EMPATIA</h4>
<p class="mb-0">Nos colocamos no lugar do outro para compreender suas necessidades e emoções, fortalecendo laços de confiança e colaboração.</p>
</div>
</div>
</div>
</div>

<h2 class="titulo-institucional">Linha do Tempo</h2>
<div class="card border-0 shadow-sm mb-5">
<div class="card-body p-4">
<div class="row align-items-center">
<div class="col-lg-8">
<p class="lead mb-0">São mais de 75 anos de história e muitos fatos empresariais marcantes de expansão, inovação ou responsabilidade social, impactando positivamente os resultados, imagem e valor social da Agropecuária AH.</p>
</div>
<div class="col-lg-4 text-center">
<div class="display-4 fw-bold text-success">75+</div>
<p class="text-muted">Anos de História</p>
</div>
</div>
</div>
</div>
'''

def atualizar_manifesto():
    about = AboutCompany.objects.first()
    if about:
        # Substitui o conteúdo atual pelo novo manifesto
        about.ac_content = CONTEUDO_COM_IDS
        about.save()
        print('Manifesto atualizado com sucesso!')
    else:
        print('Nenhum registro encontrado na tabela AboutCompany.')

def adiciona_classe_titulos():
    about = AboutCompany.objects.first()
    if about:
        conteudo = about.ac_content
        # Adiciona a classe nos h2 e h3 (mantendo ids)
        conteudo = re.sub(r'<h2(.*?)>', r'<h2\1 class="titulo-institucional">', conteudo)
        conteudo = re.sub(r'<h3(.*?)>', r'<h3\1 class="titulo-institucional">', conteudo)
        about.ac_content = conteudo
        about.save()
        print('Classe adicionada em todos os títulos!')
    else:
        print('Nenhum registro encontrado na tabela AboutCompany.')

if __name__ == "__main__":
    atualizar_manifesto()
    adiciona_classe_titulos() 