MD_SRC = $(wildcard *.md)
PDF_DST = $(MD_SRC:.md=.pdf)

all: $(PDF_DST)

%.pdf: %.md
	pandoc -o $@ $<

