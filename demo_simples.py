import asyncio

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv(override=True)


def get_weather(city: str) -> dict:
    """Devolve o tempo atual de uma cidade (dados simulados)."""
    dados = {
        "lisboa": "24°C, céu limpo",
        "porto": "19°C, chuva fraca",
        "são paulo": "27°C, nublado",
    }
    return {"city": city, "weather": dados.get(city.lower(), "sem dados")}

def soma(a, b) -> int:
    """ Essa função soma dois valores a e b 
    
    args:
      a: int- primeiro valor
      b: int- segundo valor
    """
    
    return a + b


def desconto(valor) -> int:
    """ Essa função retornar o valor a ser descontado

    Args:
        valor: int- valor inserido

    Returns:
        O valor a ser descontado
    """
    
    if valor > 200:
        desconto = valor * (10/100)
        return desconto
    
    elif valor > 500:
        desconto = valor * (15/100)
        return desconto

agent = Agent(
    name="assistente_tempo",
    model="gemini-flash-latest",
    instruction="Responde em português. Usa a ferramenta get_weather para perguntas sobre o tempo. *soma*: Usa a ferramenta soma para perguntas sobre somas. *desconto*: Retorna o desconto de um determinado valor",
    tools=[get_weather, soma, desconto],
)


async def main():
    session_service = InMemorySessionService() # Declaração da sessão de memória
    runner = Runner(agent=agent, app_name="demo", session_service=session_service) # criamos o executavel do agente
    await session_service.create_session(app_name="demo", user_id="u1", session_id="s1") # Criamos a sessão

    while True:
        
        pergunta = input("Digite a pergunta:")
        print(f"Utilizador: {pergunta}\n")


        mensagem = types.Content(role="user", parts=[types.Part(text=pergunta)]) # 
        async for event in runner.run_async(user_id="u1", session_id="s1", new_message=mensagem):
            for call in event.get_function_calls():
                print(f"[tool] {call.name}({call.args})")
            if event.is_final_response() and event.content:
                print(f"\nAgente: {event.content.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
