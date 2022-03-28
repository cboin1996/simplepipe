##
# DScD Pandoc Presentation
#
# @file
# @version 0.1
# @author Blair Drummond

PDF_NAME = ../slides
WATCH = ../content.md
ASSETS = ../assets

build: .build/titlepage.pdf .build/content.pdf
	pdfunite .build/titlepage.pdf .build/content.pdf $(PDF_NAME).pdf
	rm -rf .build

dev: $(WATCH)
	@echo "Watching $(WATCH) for changes"
	inotifywait -m $(WATCH) -e modify | while read path action file; do \
		make build; \
	done;

template:
	cp -n .template/* .

.build/titlepage.pdf: $(WATCH)
	@echo Make the title page
	@mkdir -p .build
	pandoc -s -t beamer --template .DScD-titlepage.beamer -o .build/titlepage.pdf $(WATCH)

.build/content.pdf: $(WATCH)
	@echo Make the title page
	@mkdir -p .build
	pandoc -s -t beamer --template .DScD.beamer -o .build/content.pdf $(WATCH) -f markdown+implicit_figures

# end
