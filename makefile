VENV = venv
PYTHON = python3
PIP = $(VENV)/bin/pip

# Cores
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
BLUE = \033[0;34m
NC = \033[0m # No Color

setup:
	@echo "$(BLUE)==> Verificando ambiente...$(NC)"

	@command -v $(PYTHON) >/dev/null 2>&1 || (echo "$(RED)❌ Python não encontrado$(NC)" && exit 1)

	@if ! dpkg -s python3-venv >/dev/null 2>&1; then \
		echo "$(YELLOW)⚠️  python3-venv não encontrado. Instalando...$(NC)"; \
		sudo apt update && sudo apt install -y python3-venv python3-pip; \
	else echo "$(GREEN)✔ python3-venv já instalado$(NC)"; fi

	@echo "$(BLUE)==> Preparando ambiente virtual...$(NC)"

	@if [ ! -d "$(VENV)" ]; then \
		echo "$(YELLOW)Criando venv...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✔ Ambiente virtual criado$(NC)"; \
	else echo "$(GREEN)✔ Venv já existe$(NC)"; fi

	@if [ ! -f "$(PIP)" ]; then \
		echo "$(RED)❌ pip não encontrado no venv$(NC)"; \
		exit 1; fi

	@echo "$(BLUE)==> Instalando dependências...$(NC)"
	@$(PIP) install -r requirements.txt

	@echo "$(GREEN)✅ Setup finalizado com sucesso!$(NC)"

run:
	@clear
	@$(VENV)/bin/python main.py

clean:
	@echo "$(YELLOW)Removendo ambiente virtual...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✔ Ambiente limpo$(NC)"

help:
	@echo ""
	@echo "$(BLUE)Comandos disponíveis$(NC)"
	@echo "----------------------------------------"
	@echo "$(GREEN)setup$(NC)  → Prepara o ambiente:"
	@echo "          • Instala dependências do sistema (se necessário)"
	@echo "          • Cria o ambiente virtual (venv)"
	@echo "          • Instala as dependências do projeto"
	@echo ""
	@echo "$(GREEN)run$(NC)    → Executa o projeto (main.py)"
	@echo ""
	@echo "$(GREEN)clean$(NC)  → Remove o ambiente virtual"
	@echo ""
	@echo "$(GREEN)help$(NC)   → Mostra estes comandos disponíveis"
	@echo ""