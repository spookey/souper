SOUP_DIR	=	souper
APP_NAME	=	souper

CMD_DELETE	:=	rm -vf
CMD_FIND	:=	find
CMD_ISORT	:=	isort
CMD_PYLINT	:=	pylint
CMD_PYREV	:=	pyreverse

PLOTS		:=	$(patsubst %,%_$(APP_NAME).png,classes packages)


.PHONY: help
.PHONY: clean cleanplot cleanpyc
.PHONY: lint plot
.PHONY: sort


help:
	@echo "souper makefile"
	@echo "\t"	"for development"
	@echo
	@echo "clean"		"\t\t"	"cleanup all files"
	@echo "cleanplot"	"\t"	"clean generated graphics"
	@echo "cleanpyc"	"\t"	"clean .pyc and __pycache__ files"
	@echo "lint"		"\t\t"	"run pylint on code"
	@echo "plot"		"\t\t"	"generate graphics with pyreverse"
	@echo "sort"		"\t\t"	"sort imports with isort"


clean: cleanplot cleanpyc

cleanplot:
	@$(CMD_DELETE) $(PLOTS)

cleanpyc:
	@$(CMD_FIND) "$(SOUP_DIR)" \
		-name '*.pyc' -delete -print \
			-o \
		-name '__pycache__' -delete -print \


define _pylint_msg_tpl
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export _pylint_msg_tpl

lint:
	@$(CMD_PYLINT) \
		--disable "C0111" \
		--disable "RP0401" \
		--msg-template="$$_pylint_msg_tpl" \
		--output-format="colorized" \
			"$(SOUP_DIR)"


$(PLOTS): plot
plot:
	@$(CMD_PYREV) \
		--output png \
		--all-ancestors \
		--module-names=y \
		--project="$(APP_NAME)" \
		--filter-mode="ALL" \
			"$(SOUP_DIR)"


sort:
	@$(CMD_ISORT) \
		--combine-star \
		--force-sort-within-sections \
		--multi-line 5 \
		--apply \
		--recursive \
			"$(SOUP_DIR)"
