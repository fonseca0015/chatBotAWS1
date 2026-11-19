"""
test_voice.py - Teste Local do Canal de Voz (ElevenLabs + RAG ERP Helpper)

Este script simula o canal telefônico/voz do ERP Helpper:
1. Recebe a dúvida do usuário (fala simulada).
2. Consulta a Search API (local ou AWS) para resgatar o contexto RAG.
3. Sintetiza uma resposta oral concisa via GPT-4o-mini (sem markdown/links).
4. Envia o texto para a API do ElevenLabs (Text-to-Speech).
5. Salva o áudio gerado em 'resposta_voz.mp3' para audição imediata.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Rachel (padrão) ou voz customizada
SEARCH_API_URL = os.getenv("SEARCH_API_URL", "http://127.0.0.1:5000/search")

def buscar_contexto(pergunta):
    """Consulta a Search API para recuperar trechos da documentação."""
    print(f"\n[1/4] Consultando Search API em '{SEARCH_API_URL}'...")
    req = urllib.request.Request(
        SEARCH_API_URL,
        data=json.dumps({"pergunta": pergunta}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            docs = json.loads(resp.read().decode("utf-8"))
            print(f"      Recuperados {len(docs)} documentos da base de conhecimento.")
            contexto = "\n\n".join([f"Doc {i+1} ({d.get('titulo')}): {d.get('texto_completo', '')[:500]}" for i, d in enumerate(docs[:3])])
            return contexto
    except Exception as e:
        print(f"      [AVISO] Falha ao consultar Search API: {str(e)}")
        print("      Usando fallback de conhecimento geral...")
        return "Manual do UNO ERP: Verifique parâmetros fiscais e regras da SEFAZ para notas fiscais."

def gerar_resposta_voz(pergunta, contexto):
    """Gera resposta ultra-objetiva e conversacional para o canal de voz."""
    print("\n[2/4] Gerando resposta adaptada para voz (GPT-4o-mini)...")
    if not OPENAI_API_KEY:
        return "Olá! Para a rejeição 201 no UNO ERP, acerte a numeração do lote no módulo de faturamento e retransmita a nota fiscal."
    
    prompt = f"""
    Você é o assistente por voz do UNO ERP. Responda à dúvida do usuário com base no contexto abaixo.
    DIRETRIZES DE VOZ:
    - Fale de maneira natural, cordial e fluida, como se estivesse em uma ligação telefônica.
    - Seja ULTRA-OBJETIVO: máximo 2 ou 3 frases curtas (menos de 250 caracteres).
    - NÃO use markdown, NÃO use asteriscos, NÃO use listas numeradas e NÃO cite URLs.
    
    CONTEXTO:
    {contexto}
    
    PERGUNTA DO USUÁRIO:
    {pergunta}
    """
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.3
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        texto = res["choices"][0]["message"]["content"].strip()
        print(f"      Texto gerado para fala:\n      \"{texto}\"")
        return texto

def sintetizar_audio_elevenlabs(texto, arquivo_saida="resposta_voz.mp3"):
    """Envia o texto para a API do ElevenLabs e salva o áudio MP3."""
    print(f"\n[3/4] Sintetizando voz via ElevenLabs API (Voice ID: {ELEVENLABS_VOICE_ID})...")
    
    if not ELEVENLABS_API_KEY:
        print("      [ERRO] ELEVENLABS_API_KEY não configurada no arquivo .env!")
        print("      Cadastre uma chave gratuita em https://elevenlabs.io/ e adicione ao seu .env:")
        print("      ELEVENLABS_API_KEY=sua_chave_aqui")
        return False
        
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    start_time = time.time()
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            audio_bytes = resp.read()
            with open(arquivo_saida, "wb") as f:
                f.write(audio_bytes)
            elapsed = time.time() - start_time
            print(f"\n[4/4] Áudio gerado com sucesso em {elapsed:.2f}s!")
            print(f"      Arquivo salvo: {os.path.abspath(arquivo_saida)} ({len(audio_bytes) / 1024:.1f} KB)")
            print("      Dê play no arquivo 'resposta_voz.mp3' para ouvir a IA falar!")
            return True
    except urllib.error.HTTPError as e:
        print(f"      [ERRO ELEVENLABS] HTTP {e.code}: {e.reason}")
        print(e.read().decode("utf-8", errors="ignore"))
        return False
    except Exception as e:
        print(f"      [ERRO] Falha na síntese de áudio: {str(e)}")
        return False

if __name__ == "__main__":
    pergunta_teste = sys.argv[1] if len(sys.argv) > 1 else "Como resolver rejeição 201 da nota fiscal?"
    print("=" * 65)
    print(" 🎙️ SIMULAÇÃO DO CANAL DE VOZ - ERP HELPPER (ELEVENLABS + RAG)")
    print("=" * 65)
    print(f"Dúvida do usuário: \"{pergunta_teste}\"")
    
    contexto = buscar_contexto(pergunta_teste)
    texto_resposta = gerar_resposta_voz(pergunta_teste, contexto)
    sintetizar_audio_elevenlabs(texto_resposta)
