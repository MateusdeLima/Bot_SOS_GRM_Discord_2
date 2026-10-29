# 🤖 Bot GRM - Assistente de Search Task Evaluation

Este bot Discord foi desenvolvido para auxiliar marcadores da task GRM (Search Task Evaluation) da Shopee, fornecendo respostas rápidas e precisas baseadas na documentação oficial e políticas de produtos proibidos.

## 📋 Funcionalidades

- **Perguntas Gerais**: Responda dúvidas sobre a task GRM
- **Explicação de Conceitos**: Entenda conceitos específicos como Bad Cases, SKIP, etc.
- **Análise de Casos**: Receba orientações sobre como marcar casos específicos
- **Verificação de Produtos Proibidos**: Verifique se produtos são proibidos/restritos na Shopee
- **Análise Integrada**: Análise GRM com verificação automática de produtos proibidos
- **Resposta por Menção**: Mencione o bot com @ para perguntas rápidas
- **Mensagens Privadas**: Converse diretamente com o bot via DM
- **Interface Amigável**: Comandos simples e respostas organizadas

## 🚀 Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com:
```
DISCORD_TOKEN=seu_token_do_discord
GEMINI_API_KEY=sua_chave_api_do_gemini
```

### 3. Documentação Necessária
Certifique-se de que os seguintes arquivos estão na raiz do projeto:
- `Search Task Evaluation.txt` - Documentação GRM
- `Politicas Proibidos - Shopee.txt` - Políticas de produtos proibidos

### 4. Executar o Bot
```bash
python src/main.py
```

## 📖 Comandos Disponíveis

### `!ajuda`
Mostra todos os comandos disponíveis e exemplos de uso.

### `!pergunta <sua pergunta>`
Faça qualquer pergunta sobre a task GRM.

**Exemplos:**
- `!pergunta Como marcar produtos meio-relevantes?`
- `!pergunta Quando devo usar SKIP?`
- `!pergunta O que são Bad Cases?`
- `!pergunta Como produtos proibidos afetam a marcação GRM?`

### `!explicar <conceito>`
Explica um conceito específico da task GRM de forma detalhada.

**Exemplos:**
- `!explicar Bad Cases`
- `!explicar SKIP`
- `!explicar Wrong Item`
- `!explicar Prohibited or Restricted Products`

### `!analisar <keyword> <produtos>`
Analisa um caso específico de marcação, incluindo verificação automática de produtos proibidos.

**Exemplos:**
- `!analisar "iPhone 15" "iPhone 15 Pro, iPhone 14, Capa iPhone"`
- `!analisar "Nike Air Max" "Nike Air Max 90, Adidas Ultraboost, Tênis Nike"`
- `!analisar "faca" "Faca de cozinha, Faca de acampamento, Faca decorativa"`

### `!verificar <produto>`
Verifica se um produto específico é proibido ou restrito na Shopee.

**Exemplos:**
- `!verificar "faca de cozinha"`
- `!verificar "perfume fracionado"`
- `!verificar "galinha viva"`
- `!verificar "uniforme exército brasileiro"`

### Mencione com @
Mencione o bot com @ seguido de sua pergunta para uma resposta rápida.

**Exemplos:**
- `@BotGRM O que são produtos proibidos?`
- `@BotGRM Como marcar quando é Wrong Brand?`
- `@BotGRM Verificar se faca é proibida`

### Mensagem Privada
Envie mensagem privada para conversar diretamente com o bot.

**Exemplos:**
- `Como marcar produtos meio-relevantes?`
- `O que são Bad Cases?`
- `Verificar se faca é proibida`
- `Analisar iPhone 15`

## 🎯 Casos de Uso

### Para Novos Marcadores
- Use `!ajuda` para entender os comandos
- Use `!explicar` para aprender conceitos básicos
- Use `!pergunta` para tirar dúvidas específicas
- Use `!verificar` para entender produtos proibidos

### Para Casos Complexos
- Use `!analisar` para receber orientações completas (incluindo verificação de proibidos)
- Use `!verificar` para confirmar status de produtos específicos
- Use `!pergunta` para esclarecer dúvidas sobre casos especiais

### Para Consulta Rápida
- Use `!explicar` para revisar conceitos rapidamente
- Use `!verificar` para consultas rápidas sobre produtos
- Use `!pergunta` para consultas pontuais
- Use menção com @ para perguntas rápidas
- Use mensagem privada para conversas diretas

### Para Análise de Produtos Proibidos
- Use `!verificar` para produtos específicos
- Use `!analisar` para casos que podem envolver produtos proibidos
- Use `!pergunta` para dúvidas sobre políticas de proibição

## 🔧 Estrutura do Projeto

```
Bot_SOS_GRM_Discord/
├── src/
│   ├── main.py                 # Arquivo principal do bot
│   └── services/
│       └── gemini_service.py   # Serviço de IA do Gemini
├── Search Task Evaluation.txt  # Documentação GRM
├── Politicas Proibidos - Shopee.txt  # Políticas de produtos proibidos
├── requirements.txt            # Dependências Python
├── config_example.txt          # Exemplo de configuração
└── README.md                   # Este arquivo
```

## 🤝 Contribuição

Para contribuir com melhorias no bot:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste as funcionalidades
5. Envie um pull request

## 📞 Suporte

Em caso de dúvidas ou problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se as variáveis de ambiente estão configuradas
3. Certifique-se de que os arquivos de documentação estão presentes
4. Verifique os logs do bot para identificar erros

## 📝 Notas

- O bot usa a API do Google Gemini para processar as respostas
- Todas as respostas são baseadas na documentação oficial da task GRM e políticas da Shopee
- O bot pode dividir respostas longas em múltiplas mensagens automaticamente
- Use aspas para keywords e produtos com espaços nos comandos
- A verificação de produtos proibidos é integrada automaticamente na análise GRM
- Produtos proibidos podem ser motivo para SKIP com razão "Prohibited or Restricted Products"

## 🔍 Funcionalidades Integradas

### Análise GRM + Verificação de Proibidos
O comando `!analisar` agora inclui automaticamente:
- Verificação se a keyword é proibida/restrita
- Verificação se os produtos são proibidos/restritos
- Recomendações para SKIP por produtos proibidos
- Análise completa de relevância considerando políticas

### Verificação Específica de Produtos
O comando `!verificar` fornece:
- Status do produto (Proibido/Restrito/Permitido)
- Justificativa baseada nas políticas
- Impacto na task GRM
- Recomendações para marcação

### Resposta Inteligente
O bot pode responder de múltiplas formas:
- **Comandos**: Use `!comando` para funcionalidades específicas
- **Menção**: Use `@BotGRM pergunta` para respostas rápidas
- **DM**: Envie mensagem privada para conversas diretas
- **Análise Automática**: O bot identifica o tipo de pergunta e responde adequadamente
