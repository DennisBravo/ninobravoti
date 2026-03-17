# Nino Bravo TI - Deploy e Versionamento

## Estrutura do Projeto

```
bravoti-sentinel/
├── app.py                 # Streamlit (Nino Web)
├── webhook_api.py         # FastAPI (WhatsApp/Digisac)
├── nino_core.py           # Nucleo de IA
├── config.py              # Configuracoes
├── requirements.txt       # Deps completas
├── requirements_api.txt   # Deps apenas API
├── startup.sh             # API + Streamlit
├── startup_api.sh         # Apenas API
└── .gitignore
```

## Como Versionar (Git)

### 1. Ver o que mudou
```powershell
git status
```

### 2. Adicionar arquivos
```powershell
git add .
# ou arquivos especificos:
git add webhook_api.py nino_core.py
```

### 3. Fazer commit
```powershell
git commit -m "Descricao das alteracoes"
```

### 4. Enviar para o GitHub
```powershell
git push origin main
```

## Como Atualizar o Projeto no GitHub

```powershell
cd "c:\Users\DennisBravo.AzureAD\OneDrive - Bravo Ti\Área de Trabalho\Nino IA\bravoti-sentinel"

git add .
git status
git commit -m "Limpeza: consolidacao requirements, arquivos faltantes, .gitignore"
git push origin main
```

## Deploys

- **Nino Web (Streamlit)**: usa `requirements.txt` e `startup.sh`
- **API Webhook (Azure)**: usa `requirements_api.txt` e `startup_api.sh`
