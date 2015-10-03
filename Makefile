SHELL := /bin/bash

HASH=`git rev-parse --short HEAD`
DATE=`date -Iseconds`

SRC_DIR = src
PDF_DIR = pdfs

MD_SRCS = $(wildcard $(SRC_DIR)/*.md)
# PDFS = $(addprefix $(PDF_DIR)/,$($(noitdir MD_SRCS):.md=.pdf))
PDFS = $(patsubst $(SRC_DIR)/%.md,$(PDF_DIR)/%.pdf,$(MD_SRCS))

.PHONY: all
all: $(PDFS)

$(PDFS): | $(PDF_DIR)

$(PDF_DIR):
	mkdir -p $@

$(PDF_DIR)/%.pdf: $(SRC_DIR)/%.md
	pandoc --latex-engine=xelatex -f markdown -V geometry="paper=a4paper,margin=2cm" -o $@ <(cat $< <(echo -e "\n [^1]: Generated from kit-maintenance-docs.git@${HASH} at ${DATE}"))

.PHONY: clean
clean:
	-rm -fr $(PDF_DIR)
