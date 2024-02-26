SRC_DIR			=	souper

CMD_SYS_PY		:=	python3

DIR_VENV		:=	venv

CMD_BLACK		:=	$(DIR_VENV)/bin/black
CMD_ISORT		:=	$(DIR_VENV)/bin/isort
CMD_PIP			:=	$(DIR_VENV)/bin/pip
CMD_PYLINT		:=	$(DIR_VENV)/bin/pylint
CMD_PYREVERSE	:=	$(DIR_VENV)/bin/pyreverse

SOURCES			:=	\
					"$(SRC_DIR)" \
					"run.py" \

.PHONY: help
help:
	@echo "+-----------------+"
	@echo "| souper makefile |"
	@echo "+-------+---------+-------+"
	@echo "|       | for development |"
	@echo "|       +-----------------+"
	@echo "|                         |"
	@echo "|> black                  | run black on $(SRC_DIR)"
	@echo "|> isort                  | run isort on $(SRC_DIR)"
	@echo "|> pylint                 | run pylint on $(SRC_DIR)"
	@echo "|> pyreverse              | run pyreverse on $(SRC_DIR)"
	@echo "|"
	@echo "|>                        | run isort, black & pylint"
	@echo "+"


$(DIR_VENV):
	$(CMD_SYS_PY) -m venv "$(DIR_VENV)"
	$(CMD_PIP) install -U pip setuptools

$(CMD_BLACK): $(DIR_VENV)
	$(CMD_PIP) install -U black
$(CMD_ISORT): $(DIR_VENV)
	$(CMD_PIP) install -U isort
$(CMD_PYLINT) $(CMD_PYREVERSE): $(DIR_VENV)
	$(CMD_PIP) install -U pylint


.PHONY: black
black: $(CMD_BLACK)
	$(CMD_BLACK) --line-length 79 $(SOURCES)

.PHONY: isort
isort: $(CMD_ISORT)
	$(CMD_ISORT) --line-length 79 --profile "black" $(SOURCES)

.PHONY: pylint
pylint: $(CMD_PYLINT)
	$(CMD_PYLINT) \
		--disable C0114 \
		--disable C0115 \
		--disable C0116 \
		--output-format colorized \
		$(SOURCES)

.PHONY: pyreverse
pyreverse: $(CMD_PYREVERSE)
	[ ! -d "graph" ] && mkdir -v "graph" || true
	$(CMD_PYREVERSE) \
		--all-ancestors \
		--all-associated \
		--filter-mode "ALL" \
		--filter-mode="ALL" \
		--module-names "y" \
		--output "png" \
		--output-directory "graph" \
			$(SOURCES)

.PHONY: action
action: isort black pylint
