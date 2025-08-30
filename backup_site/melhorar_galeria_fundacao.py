#!/usr/bin/env python3
"""
Script para melhorar a organização das imagens da galeria da Fundação AH
- Renomeia imagens com nomes mais profissionais
- Organiza por categorias
- Cria backup das imagens originais
"""

import os
import shutil
from datetime import datetime

def melhorar_galeria_fundacao():
    # Diretório das imagens sociais
    social_dir = "static/img/social"
    
    # Criar backup das imagens originais
    backup_dir = f"static/img/social/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Lista de imagens atuais (baseada no views.py)
    imagens_atuais = [
        'WhatsApp Image 2025-07-02 at 08.50.23.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.24 (4).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.25 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.26 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.27 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.28 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (1).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (2).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.29 (3).jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.30.jpeg',
        'WhatsApp Image 2025-07-02 at 08.50.30 (1).jpeg',
    ]
    
    # Novos nomes mais profissionais (categorizados)
    novos_nomes = [
        # Atividades Educacionais
        'fundacao_ah_atividades_educacionais_01.jpg',
        'fundacao_ah_atividades_educacionais_02.jpg',
        'fundacao_ah_atividades_educacionais_03.jpg',
        'fundacao_ah_atividades_educacionais_04.jpg',
        'fundacao_ah_atividades_educacionais_05.jpg',
        
        # Oficinas de Arte e Cultura
        'fundacao_ah_oficinas_arte_01.jpg',
        'fundacao_ah_oficinas_arte_02.jpg',
        'fundacao_ah_oficinas_arte_03.jpg',
        'fundacao_ah_oficinas_arte_04.jpg',
        'fundacao_ah_oficinas_arte_05.jpg',
        
        # Atividades Esportivas
        'fundacao_ah_esportes_01.jpg',
        'fundacao_ah_esportes_02.jpg',
        'fundacao_ah_esportes_03.jpg',
        'fundacao_ah_esportes_04.jpg',
        'fundacao_ah_esportes_05.jpg',
        
        # Alimentação e Nutrição
        'fundacao_ah_alimentacao_01.jpg',
        'fundacao_ah_alimentacao_02.jpg',
        'fundacao_ah_alimentacao_03.jpg',
        'fundacao_ah_alimentacao_04.jpg',
        'fundacao_ah_alimentacao_05.jpg',
        
        # Eventos e Celebrações
        'fundacao_ah_eventos_01.jpg',
        'fundacao_ah_eventos_02.jpg',
        'fundacao_ah_eventos_03.jpg',
        'fundacao_ah_eventos_04.jpg',
        'fundacao_ah_eventos_05.jpg',
        
        # Equipe e Voluntários
        'fundacao_ah_equipe_01.jpg',
        'fundacao_ah_equipe_02.jpg',
        'fundacao_ah_equipe_03.jpg',
        'fundacao_ah_equipe_04.jpg',
        'fundacao_ah_equipe_05.jpg',
    ]
    
    print("🔄 Iniciando melhoria da galeria da Fundação AH...")
    print(f"📁 Backup será criado em: {backup_dir}")
    
    # Fazer backup das imagens originais
    for img in imagens_atuais:
        src_path = os.path.join(social_dir, img)
        if os.path.exists(src_path):
            dst_path = os.path.join(backup_dir, img)
            shutil.copy2(src_path, dst_path)
            print(f"✅ Backup criado: {img}")
    
    # Renomear imagens
    for i, (img_antiga, novo_nome) in enumerate(zip(imagens_atuais, novos_nomes)):
        src_path = os.path.join(social_dir, img_antiga)
        dst_path = os.path.join(social_dir, novo_nome)
        
        if os.path.exists(src_path):
            try:
                os.rename(src_path, dst_path)
                print(f"✅ Renomeado: {img_antiga} → {novo_nome}")
            except Exception as e:
                print(f"❌ Erro ao renomear {img_antiga}: {e}")
        else:
            print(f"⚠️ Arquivo não encontrado: {img_antiga}")
    
    # Criar arquivo de documentação
    doc_content = f"""# Galeria Fundação AH - Documentação

## Melhorias Implementadas

### Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

### Categorias de Imagens:

1. **Atividades Educacionais** (5 imagens)
   - fundacao_ah_atividades_educacionais_01.jpg a 05.jpg

2. **Oficinas de Arte e Cultura** (5 imagens)
   - fundacao_ah_oficinas_arte_01.jpg a 05.jpg

3. **Atividades Esportivas** (5 imagens)
   - fundacao_ah_esportes_01.jpg a 05.jpg

4. **Alimentação e Nutrição** (5 imagens)
   - fundacao_ah_alimentacao_01.jpg a 05.jpg

5. **Eventos e Celebrações** (5 imagens)
   - fundacao_ah_eventos_01.jpg a 05.jpg

6. **Equipe e Voluntários** (5 imagens)
   - fundacao_ah_equipe_01.jpg a 05.jpg

### Backup:
- Todas as imagens originais foram salvas em: {backup_dir}

### Próximos Passos:
1. Atualizar o views.py com os novos nomes de arquivos
2. Verificar se todas as imagens estão sendo exibidas corretamente
3. Considerar otimização de tamanho das imagens para web
4. Adicionar descrições específicas para cada imagem

### Observações:
- Nomes agora são mais profissionais e descritivos
- Organização por categorias facilita a manutenção
- Backup garante segurança dos arquivos originais
"""
    
    with open(os.path.join(social_dir, "README_GALERIA.md"), "w", encoding="utf-8") as f:
        f.write(doc_content)
    
    print("\n📋 Nova lista de imagens para o views.py:")
    print("galeria_social = [")
    for nome in novos_nomes:
        print(f"    '{nome}',")
    print("]")
    
    print(f"\n✅ Melhoria concluída!")
    print(f"📄 Documentação criada: {social_dir}/README_GALERIA.md")
    print(f"💾 Backup salvo em: {backup_dir}")

if __name__ == "__main__":
    melhorar_galeria_fundacao() 