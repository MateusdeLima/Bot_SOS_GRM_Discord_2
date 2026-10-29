import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from services.gemini_service import GeminiService

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

gemini_service = GeminiService()

@bot.event
async def on_ready():
    print(f'Bot GRM está online como {bot.user}')
    print('Comandos disponíveis:')
    print('!ajuda - Mostra todos os comandos disponíveis')
    print('!pergunta <sua pergunta> - Faz uma pergunta sobre a task GRM')
    print('!explicar <conceito> - Explica um conceito específico da task GRM')
    print('!analisar <keyword> <produtos> - Analisa um caso específico de marcação')
    print('!verificar <produto> - Verifica se um produto é proibido/restrito')
    print('Mencione o bot com @ para perguntas gerais')
    print('Envie mensagem privada para conversar diretamente')

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return

    # Processa comandos normais primeiro
    await bot.process_commands(message)

    # Verifica se o bot foi mencionado
    if bot.user.mentioned_in(message):
        await processar_menção(message)
    
    # Verifica se é mensagem privada
    elif isinstance(message.channel, discord.DMChannel):
        await processar_mensagem_privada(message)

async def processar_menção(message):
    """Processa quando o bot é mencionado com @"""
    try:
        # Remove a menção do bot da mensagem
        conteudo = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
        
        if not conteudo:
            embed = discord.Embed(
                title="🤖 Olá! Sou o Bot GRM",
                description="Mencionei-me! Como posso ajudar você com a task GRM?",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Você pode:",
                value="• Fazer perguntas sobre GRM\n• Pedir explicações de conceitos\n• Verificar produtos proibidos\n• Analisar casos de marcação",
                inline=False
            )
            embed.add_field(
                name="Comandos úteis:",
                value="`!ajuda` - Ver todos os comandos\n`!pergunta <pergunta>` - Fazer pergunta\n`!verificar <produto>` - Verificar produto",
                inline=False
            )
            await message.reply(embed=embed)
            return

        # Mostra que está processando
        await message.add_reaction('🤔')
        
        resposta = await gemini_service.processar_mensagem_geral(conteudo)
        
        if resposta['status'] == 'sucesso':
            resposta_texto = resposta['resposta']
            if len(resposta_texto) > 2000:
                partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                for i, parte in enumerate(partes):
                    embed = discord.Embed(
                        title=f"📋 Resposta GRM (Parte {i+1}/{len(partes)})",
                        description=parte,
                        color=discord.Color.green()
                    )
                    if i == 0:
                        embed.add_field(name="Pergunta", value=conteudo[:100] + "..." if len(conteudo) > 100 else conteudo, inline=False)
                    await message.reply(embed=embed)
            else:
                embed = discord.Embed(
                    title="📋 Resposta GRM",
                    description=resposta_texto,
                    color=discord.Color.green()
                )
                embed.add_field(name="Pergunta", value=conteudo, inline=False)
                await message.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await message.reply(embed=embed)
            
    except Exception as e:
        await message.reply(f"❌ Ocorreu um erro ao processar sua mensagem: {str(e)}")

async def processar_mensagem_privada(message):
    """Processa mensagens privadas"""
    try:
        conteudo = message.content.strip()
        
        if not conteudo:
            embed = discord.Embed(
                title="🤖 Olá! Sou o Bot GRM",
                description="Enviei uma mensagem privada! Como posso ajudar você com a task GRM?",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Você pode:",
                value="• Fazer perguntas sobre GRM\n• Pedir explicações de conceitos\n• Verificar produtos proibidos\n• Analisar casos de marcação",
                inline=False
            )
            embed.add_field(
                name="Exemplos:",
                value="• 'Como marcar produtos meio-relevantes?'\n• 'O que são Bad Cases?'\n• 'Verificar se faca é proibida'\n• 'Analisar iPhone 15'",
                inline=False
            )
            await message.channel.send(embed=embed)
            return

        # Mostra que está processando
        await message.add_reaction('🤔')
        
        resposta = await gemini_service.processar_mensagem_geral(conteudo)
        
        if resposta['status'] == 'sucesso':
            resposta_texto = resposta['resposta']
            if len(resposta_texto) > 2000:
                partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                for i, parte in enumerate(partes):
                    embed = discord.Embed(
                        title=f"📋 Resposta GRM (Parte {i+1}/{len(partes)})",
                        description=parte,
                        color=discord.Color.green()
                    )
                    if i == 0:
                        embed.add_field(name="Pergunta", value=conteudo[:100] + "..." if len(conteudo) > 100 else conteudo, inline=False)
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="📋 Resposta GRM",
                    description=resposta_texto,
                    color=discord.Color.green()
                )
                embed.add_field(name="Pergunta", value=conteudo, inline=False)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)
            
    except Exception as e:
        await message.channel.send(f"❌ Ocorreu um erro ao processar sua mensagem: {str(e)}")

@bot.command()
async def ajuda(ctx):
    """Mostra todos os comandos disponíveis"""
    embed = discord.Embed(
        title="🤖 Bot GRM - Assistente de Search Task Evaluation",
        description="Olá! Sou seu assistente para a task GRM da Shopee. Aqui estão os comandos disponíveis:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="!pergunta <sua pergunta>",
        value="Faça qualquer pergunta sobre a task GRM e eu responderei baseado na documentação oficial.",
        inline=False
    )
    
    embed.add_field(
        name="!explicar <conceito>",
        value="Explica um conceito específico da task GRM de forma detalhada.",
        inline=False
    )
    
    embed.add_field(
        name="!analisar <keyword> <produtos>",
        value="Analisa um caso específico de marcação, incluindo verificação de produtos proibidos.",
        inline=False
    )
    
    embed.add_field(
        name="!verificar <produto>",
        value="Verifica se um produto específico é proibido ou restrito na Shopee.",
        inline=False
    )
    
    embed.add_field(
        name="Mencione com @",
        value="Mencione o bot com @ seguido de sua pergunta para uma resposta rápida.",
        inline=False
    )
    
    embed.add_field(
        name="Mensagem Privada",
        value="Envie mensagem privada para conversar diretamente com o bot.",
        inline=False
    )
    
    embed.add_field(
        name="Exemplos de uso:",
        value="""
        `!pergunta Como marcar produtos meio-relevantes?`
        `!explicar Bad Cases`
        `!analisar "iPhone 15" "iPhone 15 Pro, iPhone 14, Capa iPhone"`
        `!verificar "faca de cozinha"`
        `@BotGRM O que são produtos proibidos?`
        """,
        inline=False
    )
    
    embed.set_footer(text="Use !ajuda a qualquer momento para ver esta mensagem novamente")
    
    await ctx.send(embed=embed)

@bot.command()
async def pergunta(ctx, *, pergunta: str):
    """Responde perguntas sobre a task GRM"""
    try:
        # Mostra que o bot está processando
        await ctx.send("🤔 Processando sua pergunta...")
        
        resposta = await gemini_service.responder_pergunta_grm(pergunta)
        
        if resposta['status'] == 'sucesso':
            # Divide a resposta se for muito longa
            resposta_texto = resposta['resposta']
            if len(resposta_texto) > 2000:
                # Divide em partes menores
                partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                for i, parte in enumerate(partes):
                    embed = discord.Embed(
                        title=f"📋 Resposta GRM (Parte {i+1}/{len(partes)})",
                        description=parte,
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Pergunta", value=pergunta[:100] + "..." if len(pergunta) > 100 else pergunta, inline=False)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="📋 Resposta GRM",
                    description=resposta_texto,
                    color=discord.Color.green()
                )
                embed.add_field(name="Pergunta", value=pergunta, inline=False)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao processar sua pergunta: {str(e)}")

@bot.command()
async def explicar(ctx, *, conceito: str):
    """Explica um conceito específico da task GRM"""
    try:
        await ctx.send(f"📚 Explicando o conceito: {conceito}")
        
        resposta = await gemini_service.explicar_conceito_grm(conceito)
        
        if resposta['status'] == 'sucesso':
            resposta_texto = resposta['resposta']
            if len(resposta_texto) > 2000:
                partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                for i, parte in enumerate(partes):
                    embed = discord.Embed(
                        title=f"📖 Explicação: {conceito} (Parte {i+1}/{len(partes)})",
                        description=parte,
                        color=discord.Color.blue()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f"📖 Explicação: {conceito}",
                    description=resposta_texto,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao explicar o conceito: {str(e)}")

@bot.command()
async def analisar(ctx, keyword: str, *, produtos: str):
    """Analisa um caso específico de marcação GRM incluindo verificação de produtos proibidos"""
    try:
        await ctx.send(f"🔍 Analisando caso: Keyword '{keyword}' com produtos: {produtos}")

        resposta = await gemini_service.analisar_caso_grm(keyword, produtos)

        if resposta['status'] == 'sucesso':
            resposta_texto = resposta['resposta']

            # Nova estrutura: apenas marcação individual e produtos proibidos
            if "**1. MARCAÇÃO INDIVIDUAL DOS PRODUTOS:**" in resposta_texto:
                sections = resposta_texto.split("**2. PRODUTOS PROIBIDOS IDENTIFICADOS:**")
                product_section = sections[0].replace("**1. MARCAÇÃO INDIVIDUAL DOS PRODUTOS:**", "").strip()
                prohibited_section = sections[1].strip() if len(sections) > 1 else None

                embed = discord.Embed(
                    title="📋 Análise do Caso GRM",
                    description=f"**Keyword:** `{keyword}`\n**Produtos:** {produtos[:100]}{'...' if len(produtos) > 100 else ''}",
                    color=discord.Color.blue()
                )

                embed.add_field(
                    name="📊 Marcação Individual dos Produtos",
                    value=product_section[:1024] if product_section else "Não especificado",
                    inline=False
                )

                if prohibited_section:
                    embed.add_field(
                        name="🚫 Produtos Proibidos e Políticas Aplicáveis",
                        value=prohibited_section[:1024],
                        inline=False
                    )

                embed.set_footer(text="Bot GRM - Foco em produtos proibidos/restritos e relevância")
                await ctx.send(embed=embed)

            else:
                # Fallback para respostas não estruturadas ou longas
                if len(resposta_texto) > 2000:
                    partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                    for i, parte in enumerate(partes):
                        embed = discord.Embed(
                            title=f"🔍 Análise GRM (Parte {i+1}/{len(partes)})",
                            description=parte,
                            color=discord.Color.orange()
                        )
                        if i == 0:
                            embed.add_field(name="Keyword", value=keyword, inline=True)
                            embed.add_field(name="Produtos", value=produtos[:100] + "..." if len(produtos) > 100 else produtos, inline=True)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="🔍 Análise GRM",
                        description=resposta_texto,
                        color=discord.Color.orange()
                    )
                    embed.add_field(name="Keyword", value=keyword, inline=True)
                    embed.add_field(name="Produtos", value=produtos, inline=True)
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao analisar o caso: {str(e)}")

@bot.command()
async def verificar(ctx, *, produto: str):
    """Verifica se um produto é proibido ou restrito na Shopee"""
    try:
        await ctx.send(f"🔍 Verificando produto: {produto}")
        
        resposta = await gemini_service.verificar_produto_proibido(produto)
        
        if resposta['status'] == 'sucesso':
            resposta_texto = resposta['resposta']
            if len(resposta_texto) > 2000:
                partes = [resposta_texto[i:i+1900] for i in range(0, len(resposta_texto), 1900)]
                for i, parte in enumerate(partes):
                    embed = discord.Embed(
                        title=f"🚫 Verificação de Produto (Parte {i+1}/{len(partes)})",
                        description=parte,
                        color=discord.Color.red()
                    )
                    if i == 0:
                        embed.add_field(name="Produto", value=produto, inline=True)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="🚫 Verificação de Produto",
                    description=resposta_texto,
                    color=discord.Color.red()
                )
                embed.add_field(name="Produto", value=produto, inline=True)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ Erro",
                description=resposta['resposta'],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            
    except Exception as e:
        await ctx.send(f"❌ Ocorreu um erro ao verificar o produto: {str(e)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Faltam argumentos para este comando. Use !ajuda para ver como usar.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando não encontrado. Use !ajuda para ver os comandos disponíveis.")
    else:
        await ctx.send(f"❌ Ocorreu um erro: {str(error)}")

bot.run(os.getenv('DISCORD_TOKEN')) 