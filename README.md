
# AutoScene Director — Troca de Cena por Janela Ativa (Script Python)

Alternativa simples para troca automática de cena com base na **janela ativa** (Windows). Útil para alternar cenas ao focar um jogo, navegador, editor etc.

## Recursos
- Mapeamento `padrão -> cena`, exemplo:
  - `chrome -> Cena Navegador`
  - `obs64.exe -> Cena OBS`
  - `VALORANT  -> Cena Jogo`
- Polling configurável (ms).
- Opção de ignorar trechos repetidos para evitar trocas constantes.

## Instalação
1. **OBS → Ferramentas → Scripts** → **+** → selecione `autoscene_director.py`.
2. Configure o campo **Mapeamentos**: um por linha, no formato `padrao => Cena Alvo`.
3. Defina o **Intervalo (ms)** e marque **Ativo**.

> Suporta Windows (usa `ctypes` para obter a janela em foco). Em macOS/Linux, o script permanece carregado, mas a detecção pode não funcionar.

## Licença
MIT.
