import google.generativeai as genai
import os
from dotenv import load_dotenv
import unicodedata

load_dotenv()


class GeminiService:

    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def _normalize(self, text):
        return unicodedata.normalize('NFKD', text).encode(
            'ASCII', 'ignore').decode('ASCII').lower()

    def _carregar_documentacao_grm(self):
        """Carrega a documentação da task GRM"""
        try:
            with open('Search Task Evaluation.txt', 'r',
                      encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f'Não foi possível carregar a documentação GRM: {e}'

    def _carregar_produtos_proibidos(self):
        """Carrega a documentação de produtos proibidos/restritos"""
        try:
            with open('Politicas Proibidos - Shopee.txt', 'r',
                      encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f'Não foi possível carregar a documentação de produtos proibidos: {e}'

    def _carregar_regras_ia(self):
        """Carrega regras específicas de formatação e conduta da IA (se existente)"""
        try:
            with open('REGRAS_IA.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f'Não foi possível carregar as regras IA: {e}'

    async def responder_pergunta_grm(self, pergunta):
        """Responde perguntas sobre a task GRM usando a documentação"""
        documentacao = self._carregar_documentacao_grm()
        regras_ia = self._carregar_regras_ia()

        prompt = f"""
        Você é um assistente especializado na task GRM (Search Task Evaluation) da Shopee. 
        Sua função é ajudar marcadores a entenderem as diretrizes e responder dúvidas sobre a task.
        
        Use a documentação e regras abaixo para responder à pergunta do usuário de forma clara e precisa.
        Sempre cite trechos específicos da documentação quando relevante.
        Siga RIGOROSAMENTE as regras específicas para IA fornecidas.
        
        DOCUMENTAÇÃO GRM:
        {documentacao}
        
        REGRAS ESPECÍFICAS PARA IA:
        {regras_ia}
        
        PERGUNTA DO USUÁRIO: {pergunta}
        
        Responda de forma estruturada e amigável, explicando os conceitos de forma clara.
        Se a pergunta for sobre casos específicos, forneça exemplos práticos seguindo exatamente as regras especificadas.
        """

        try:
            response = self.model.generate_content(prompt)
            return {'resposta': response.text, 'status': 'sucesso'}
        except Exception as e:
            return {
                'resposta':
                f'Ocorreu um erro ao processar sua pergunta: {str(e)}',
                'status': 'erro'
            }

    async def explicar_conceito_grm(self, conceito):
        """Explica um conceito específico da task GRM"""
        documentacao = self._carregar_documentacao_grm()
        regras_ia = self._carregar_regras_ia()

        prompt = f"""
        Você é um assistente especializado na task GRM (Search Task Evaluation) da Shopee.
        Explique o conceito "{conceito}" de forma detalhada e clara, usando a documentação fornecida.
        Siga RIGOROSAMENTE as regras específicas para IA fornecidas.
        
        DOCUMENTAÇÃO GRM:
        {documentacao}
        
        REGRAS ESPECÍFICAS PARA IA:
        {regras_ia}
        
        Conceito a ser explicado: {conceito}
        
        Forneça:
        1. Definição clara do conceito
        2. Exemplos práticos seguindo as regras específicas
        3. Como aplicar na prática
        4. Casos especiais ou exceções (se houver)
        5. Formatação exata conforme especificado nas regras
        """

        try:
            response = self.model.generate_content(prompt)
            return {'resposta': response.text, 'status': 'sucesso'}
        except Exception as e:
            return {
                'resposta':
                f'Ocorreu um erro ao explicar o conceito: {str(e)}',
                'status': 'erro'
            }

    async def analisar_caso_grm(self, keyword, produtos):
        """Analisa um caso GRM focando em produtos proibidos/restritos e marcação individual"""
        documentacao = self._carregar_documentacao_grm()
        produtos_proibidos = self._carregar_produtos_proibidos()
        regras_ia = self._carregar_regras_ia()

        prompt = f"""
        Você é um assistente especializado na task GRM (Search Task Evaluation) da Shopee.
        NÃO decida ou recomende SKIP aqui. Apenas analise produtos e cite políticas de proibidos/restritos quando aplicável.
        
        DOCUMENTAÇÃO GRM:
        {documentacao}
        
        PRODUTOS PROIBIDOS/RESTRITOS:
        {produtos_proibidos}
        
        REGRAS ESPECÍFICAS PARA IA (OBRIGATÓRIO SEGUIR):
        {regras_ia}
        
        CASO PARA ANÁLISE:
        Keyword: {keyword}
        Produtos encontrados: {produtos}
        
        ESTRUTURA DA RESPOSTA:
        
        **1. MARCAÇÃO INDIVIDUAL DOS PRODUTOS:**
        [Para cada produto, uma linha com: "Produto X: Relevante/Meio Relevante/Irrelevante > [motivos específicos]"]
        
        **2. PRODUTOS PROIBIDOS IDENTIFICADOS:**
        [Se algum produto for PROIBIDO, listar o produto e citar as políticas específicas da Shopee que se aplicam]
        
        REGRAS CRÍTICAS:
        - Marcar relevância de cada produto para a keyword
        - Se produto for PROIBIDO: marcar como "Irrelevante > item retornado PROIBIDO" E mostrar políticas aplicáveis
        - Seguir EXATAMENTE o formato das regras IA
        - SEMPRE citar políticas específicas para produtos proibidos
        """

        try:
            response = self.model.generate_content(prompt)
            return {'resposta': response.text, 'status': 'sucesso'}
        except Exception as e:
            return {
                'resposta': f'Ocorreu um erro ao analisar o caso: {str(e)}',
                'status': 'erro'
            }

    async def verificar_produto_proibido(self, produto):
        """Verifica se um produto é proibido ou restrito na Shopee"""
        produtos_proibidos = self._carregar_produtos_proibidos()

        prompt = f"""
        Você é um assistente especializado em políticas de produtos da Shopee.
        Verifique se o produto "{produto}" é proibido ou restrito baseado na documentação oficial.
        
        DOCUMENTAÇÃO DE PRODUTOS PROIBIDOS/RESTRITOS:
        {produtos_proibidos}
        
        PRODUTO PARA VERIFICAÇÃO: {produto}
        
        ESTRUTURA DA RESPOSTA:
        
        **STATUS:** [PROIBIDO/RESTRITO/PERMITIDO]
        
        **CLASSIFICAÇÃO:** [Se PROIBIDO ou RESTRITO, explicar detalhadamente o motivo]
        
        **POLÍTICAS APLICÁVEIS:** [Citar as seções específicas das políticas da Shopee que se aplicam a este produto]
        
        **RECOMENDAÇÃO GRM:** [Como marcar este produto se encontrado em uma task: "Irrelevante > item retornado PROIBIDO" ou orientação específica]
        
        Seja específico e cite exatamente as políticas relevantes da documentação oficial.
        """

        try:
            response = self.model.generate_content(prompt)
            return {'resposta': response.text, 'status': 'sucesso'}
        except Exception as e:
            return {
                'resposta': f'Ocorreu um erro ao verificar o produto: {str(e)}',
                'status': 'erro'
            }

    async def processar_mensagem_geral(self, mensagem):
        """Processa mensagens gerais usando contexto GRM e políticas"""
        documentacao = self._carregar_documentacao_grm()
        produtos_proibidos = self._carregar_produtos_proibidos()
        regras_ia = self._carregar_regras_ia()

        prompt = f"""
        Você é o Bot GRM, assistente especializado na task GRM (Search Task Evaluation) da Shopee.
        Responda à mensagem do usuário de forma útil e contextual.
        Siga RIGOROSAMENTE as regras específicas para IA quando aplicável.
        
        DOCUMENTAÇÃO GRM:
        {documentacao}
        
        PRODUTOS PROIBIDOS/RESTRITOS:
        {produtos_proibidos}
        
        REGRAS ESPECÍFICAS PARA IA:
        {regras_ia}
        
        MENSAGEM DO USUÁRIO: {mensagem}
        
        Responda de forma natural e helpful, usando o contexto GRM quando relevante.
        - Se a mensagem envolver análise de produtos/casos: NÃO decida SKIP. Foque em relevância por produto e cite políticas de proibidos/restritos quando aplicável, seguindo o formato das regras.
        - Se a mensagem for sobre SKIP (como funciona, quando aplicar, reasons): EXPLIQUE o conceito e as reasons aceitas conforme a documentação GRM, com exemplos, sem decidir SKIP para um caso específico.
        """

        try:
            response = self.model.generate_content(prompt)
            return {'resposta': response.text, 'status': 'sucesso'}
        except Exception as e:
            return {
                'resposta': f'Ocorreu um erro ao processar sua mensagem: {str(e)}',
                'status': 'erro'
            }
