# 🛒 Sistema de Gerenciamento da Equipe de Compras

## 📋 Visão Geral

Foi criado um sistema completo para gerenciar a equipe de compras através do painel administrativo do Django.

## 🗄️ Estrutura do Banco de Dados

### Modelo: `EquipeCompras`

**Campos disponíveis:**
- **Nome**: Nome completo do membro
- **E-mail**: Email corporativo
- **Telefone**: Número de telefone
- **Ramal**: Ramal interno (opcional)
- **Cargo**: Função na empresa
- **Local/Unidade**: Local de trabalho
- **Ativo**: Se o membro está ativo na equipe
- **Ordem de Exibição**: Ordem na lista (1, 2, 3...)
- **Data de Criação**: Data automática
- **Data de Atualização**: Data automática

## 🔧 Como Usar

### 1. Acessar o Painel Admin
- URL: `http://seu-site.com/admin/`
- Faça login com suas credenciais

### 2. Gerenciar Equipe de Compras
- No menu lateral, clique em **"Membros da Equipe de Compras"**
- Você verá uma lista com todos os membros

### 3. Adicionar Novo Membro
1. Clique em **"ADICIONAR MEMBRO DA EQUIPE DE COMPRAS"**
2. Preencha os campos:
   - **Nome**: Nome completo
   - **E-mail**: Email corporativo
   - **Telefone**: Número com DDD
   - **Ramal**: Ramal interno (se houver)
   - **Cargo**: Função na empresa
   - **Local/Unidade**: Local de trabalho
   - **Ativo**: Marque se está ativo
   - **Ordem de Exibição**: Número para ordenar (1, 2, 3...)
3. Clique em **"SALVAR"**

### 4. Editar Membro Existente
1. Na lista, clique no nome do membro
2. Modifique os campos desejados
3. Clique em **"SALVAR"**

### 5. Excluir Membro
1. Na lista, clique no nome do membro
2. Clique em **"EXCLUIR"** (canto inferior direito)
3. Confirme a exclusão

### 6. Ativar/Desativar Rapidamente
- Na lista principal, use a coluna **"Ativo"** para marcar/desmarcar
- Use a coluna **"Ordem"** para alterar a ordem de exibição

## 📊 Funcionalidades do Admin

### Lista Principal
- **Nome**: Nome do membro
- **E-mail**: Email corporativo
- **Telefone**: Telefone completo (com ramal)
- **Cargo**: Função na empresa
- **Local**: Local de trabalho
- **Ativo**: Status ativo/inativo
- **Ordem**: Ordem de exibição

### Filtros Disponíveis
- **Ativo**: Filtrar por status
- **Local**: Filtrar por local/unidade
- **Cargo**: Filtrar por função

### Busca
- Busca por: Nome, Email, Cargo, Local

### Edição Rápida
- **Ativo**: Marcar/desmarcar diretamente na lista
- **Ordem**: Alterar ordem diretamente na lista

## 🚀 Configuração Inicial

### 1. Aplicar Migração
```bash
python manage.py migrate
```

### 2. Criar Dados Iniciais (Opcional)
```bash
python criar_equipe_compras.py
```

### 3. Acessar Admin
- Acesse o painel administrativo
- Vá em "Membros da Equipe de Compras"
- Adicione os membros da sua equipe

## 📝 Exemplo de Uso

### Adicionando um Novo Membro:
1. **Nome**: João Silva
2. **E-mail**: joao.silva@ah.agr.br
3. **Telefone**: +55 (67) 3546-1467
4. **Ramal**: 235
5. **Cargo**: Analista de Compras
6. **Local**: Brasilândia/MS
7. **Ativo**: ✅
8. **Ordem**: 4

### Editando um Membro:
1. Clique em "Alexandre Brazoloto"
2. Altere o ramal de "234" para "235"
3. Clique em "SALVAR"

### Desativando um Membro:
1. Na lista, desmarque a coluna "Ativo"
2. O membro ficará inativo mas não será excluído

## 🔄 Integração com Formulário

Os dados da equipe de compras são automaticamente integrados ao formulário de contato da página de compras. O sistema busca os membros ativos e os disponibiliza como opções de destinatário.

## 📞 Suporte

Para dúvidas ou problemas:
- Email: ti@ah.agr.br
- Telefone: +55 (67) 3546-1467

---

**Desenvolvido por:** Equipe de TI - Agropecuária AH  
**Data:** 2025  
**Versão:** 1.0 