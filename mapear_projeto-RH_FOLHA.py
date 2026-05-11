# mensagem de teste
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 1. CONFIGURAÇÕES DE AUDITORIA (REGRAS RH FOLHA)
# ==============================================================================
RAIZ_PROJETO = Path(r"C:\Users\yokad\Desktop\RH FOLHA TESTE")
PASTA_PRODUCAO = RAIZ_PROJETO / "PRODUCAO_CONGELADA"
SAIDA_AUDITORIA = RAIZ_PROJETO / "OUTPUTS_PARA_CHAT"
SAIDA_AUDITORIA.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
ARQUIVO_MANIFESTO = SAIDA_AUDITORIA / f"MANIFESTO_DNA_PROJETO_{TIMESTAMP}.json"
ARQUIVO_RESUMO_TXT = SAIDA_AUDITORIA / f"RESUMO_LOCALIZACAO_MOTORES_{TIMESTAMP}.txt"

# Termos técnicos que definem o motor oficial (Parte A e Parte B)
ASSINATURAS_TECNICAS = {
    "MOTOR_LEITURA_A": "PATCH2_A_V2_20260427_220321",
    "MOTOR_CURADORIA_B": "PATCH_B_V2_20260427_221853",
    "PARSER_PDF": "pdfplumber",
    "BASE_V51": "BASE_FUNCIONARIOS_FOLHA_NOME_FLAG_V51"
}

def realizar_investigacao_forense():
    inventario = []
    
    print(f"Iniciando Varredura Forense em: {RAIZ_PROJETO}...")
    
    # 2. MAPEAMENTO DE ARQUIVOS .PY E .IPYNB
    for root, dirs, files in os.walk(RAIZ_PROJETO):
        for file in files:
            if file.endswith(('.py', '.ipynb')):
                caminho_completo = Path(root) / file
                try:
                    conteudo = ""
                    if file.endswith('.ipynb'):
                        with open(caminho_completo, 'r', encoding='utf-8') as f:
                            nb = json.load(f)
                            for cell in nb.get('cells', []):
                                if cell['cell_type'] == 'code':
                                    conteudo += "".join(cell['source'])
                    else:
                        conteudo = caminho_completo.read_text(encoding='utf-8')

                    # Identificação de Motor Congelado
                    tags_encontradas = []
                    for id_motor, assinatura in ASSINATURAS_TECNICAS.items():
                        if assinatura in conteudo or assinatura in str(caminho_completo):
                            tags_encontradas.append(id_motor)
                    
                    if tags_encontradas:
                        inventario.append({
                            "ARQUIVO": file,
                            "CAMINHO": str(caminho_completo),
                            "MOTORES_DETECTADOS": tags_encontradas,
                            "STATUS": "CONGELADO/FUNCIONAL" if "PATCH" in str(caminho_completo) else "RASCUNHO"
                        })
                except Exception as e:
                    continue

    # 3. GERAÇÃO DE EVIDÊNCIAS (OUTPUT PARA O GEMINI CLI)
    df_investigacao = pd.DataFrame(inventario)
    
    # Salvar Manifesto JSON (Dados Técnicos)
    with open(ARQUIVO_MANIFESTO, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=4)

    # Salvar Resumo Estruturado (Para o Usuário Copiar e Colar)
    with open(ARQUIVO_RESUMO_TXT, 'w', encoding='utf-8') as f:
        f.write(f"=== MANIFESTO DE DNA DO PROJETO - OPERAÇÃO RH FOLHA ===\n")
        f.write(f"Data da Investigação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        f.write("LOCALIZAÇÃO DOS MOTORES OFICIAIS:\n")
        for item in inventario:
            if item['STATUS'] == "CONGELADO/FUNCIONAL":
                f.write(f"\n[MODELO {item['MOTORES_DETECTADOS']}]\n")
                f.write(f"CAMINHO: {item['CAMINHO']}\n")
        f.write("\n" + "="*60 + "\n")
        f.write("FIM DO MANIFESTO ANONIMIZADO.\n")

    print(f"\n[OK] INVESTIGAÇÃO CONCLUÍDA!")
    print(f"ARQUIVO QUE VOCÊ DEVE ENVIAR AO GEMINI/CHATGPT PARA CONTEXTO:")
    print(f"**{ARQUIVO_RESUMO_TXT}**")
    print(f"**{ARQUIVO_MANIFESTO}**")

if __name__ == "__main__":
    realizar_investigacao_forense()