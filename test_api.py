"""
test_api.py - Script de Teste Automatizado do ERP Helpper
Permite validar o funcionamento da rota /search (Local ou AWS) e do Webhook do n8n.
"""
import sys
import json
import urllib.request
import urllib.error

DEFAULT_LOCAL_URL = "http://127.0.0.1:5000/search"
DEFAULT_AWS_URL = "http://44.203.191.31:5000/search"
DEFAULT_N8N_URL = "https://unoerpai.app.n8n.cloud/webhook/c7683d30-5ffb-448b-a9cb-2dac0ac443bb"

def testar_endpoint(url, payload, nome="Endpoint"):
    print(f"\n" + "=" * 60)
    print(f"Testando {nome}: {url}")
    print(f"Payload: {json.dumps(payload, ensure_ascii=False)}")
    print("=" * 60)
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            print(f"✅ Status HTTP: {status}")
            try:
                parsed = json.loads(body)
                print(f"Retorno recebido com sucesso! ({len(parsed)} registros ou campos)")
                print(json.dumps(parsed, indent=2, ensure_ascii=False)[:500] + "\n...")
            except json.JSONDecodeError:
                print(f"Retorno bruto: {body[:300]}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}: {e.reason}")
        print(e.read().decode("utf-8", errors="ignore")[:300])
        return False
    except urllib.error.URLError as e:
        print(f"⚠️ Falha de Conexão: {e.reason}")
        return False
    except Exception as e:
        print(f"⚠️ Erro inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    query_teste = {"pergunta": "Como tratar a rejeição 201?"}
    
    alvo = sys.argv[1] if len(sys.argv) > 1 else "local"
    
    if alvo == "aws":
        testar_endpoint(DEFAULT_AWS_URL, query_teste, "Search API na AWS")
    elif alvo == "n8n":
        testar_endpoint(DEFAULT_N8N_URL, query_teste, "Webhook do n8n")
    else:
        sucesso_local = testar_endpoint(DEFAULT_LOCAL_URL, query_teste, "Search API Local")
        if not sucesso_local:
            print("\n💡 Dica: Verifique se 'python main.py' está rodando na porta 5000.")
            print("Para testar a AWS diretamente, execute: python test_api.py aws")
            print("Para testar o n8n diretamente, execute: python test_api.py n8n")
