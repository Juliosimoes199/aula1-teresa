from dotenv import load_dotenv
from flask import Flask, jsonify, request
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv(override=True)

APP_NAME = "demo"


def get_weather(city: str) -> dict:
    """Devolve o tempo atual de uma cidade (dados simulados)."""
    dados = {
        "lisboa": "24°C, céu limpo",
        "porto": "19°C, chuva fraca",
        "são paulo": "27°C, nublado",
    }
    return {"city": city, "weather": dados.get(city.lower(), "sem dados")}


def soma(a: int, b: int) -> int:
    """Soma dois valores.

    Args:
        a: primeiro valor
        b: segundo valor
    """
    return a + b


def desconto(valor: float) -> float:
    """Devolve o valor a ser descontado.

    Args:
        valor: valor inserido
    """
    if valor > 500:
        return valor * 0.15
    if valor > 200:
        return valor * 0.10
    return 0


agent = Agent(
    name="assistente_tempo",
    model="gemini-flash-latest",
    instruction=(
        """Responde em português. Usa a ferramenta get_weather para perguntas sobre o tempo.
        Usa a ferramenta soma para perguntas sobre somas. 
        Usa a ferramenta desconto para calcular o desconto de um valor."""
    ),
    tools=[get_weather, soma, desconto],
)

session_service = InMemorySessionService() # instancioando a memória do agente
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service) # criando o executável do agente

app = Flask(__name__)

# Criando uma sessão para o agente
async def garantir_sessao(user_id: str, session_id: str):
    sessao = await session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    if sessao is None:
        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )


@app.post("/chat")
async def chat():
    dados = request.get_json(silent=True) or {} # Pegando os dados que serão inseridos nesse endpoint
    # Armazenando os dados em cada variável
    pergunta = dados.get("pergunta")
    user_id = dados.get("user_id", "u1")
    session_id = dados.get("session_id", "s1")

    # Verifica se a variável "pergunta" esta vazia ou não
    if not pergunta:
        return jsonify({"erro": "O campo 'pergunta' é obrigatório."}), 400

    # Executando a sessão
    await garantir_sessao(user_id, session_id)

    # Tratando as mensagens dos usuários para um formato que o bot entenda
    mensagem = types.Content(role="user", parts=[types.Part(text=pergunta)])
    
    ferramentas = [] # Criando uma variável para armazenar as ferramentas que o bot usou se caso queira saber quais ferramentas ele usou na conversa
    resposta = None

    # Processando a mensagem do usuário para o bot gerar uma resposta em seguida
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=mensagem
    ):
        for call in event.get_function_calls():
            ferramentas.append({"nome": call.name, "args": dict(call.args)})
        if event.is_final_response() and event.content:
            resposta = event.content.parts[0].text

    # Retornando um json final contendo a reposta do bot, a sessão da conversa e a lista de ferramentas usando pelo bot
    return jsonify(
        {
            "session_id": session_id,
            "resposta": resposta,
            "ferramentas_usadas": ferramentas,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
