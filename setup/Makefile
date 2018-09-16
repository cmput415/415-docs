# Original author: Marcus Karpoff
# Modifications: Braedy Kuzma

# SRC: The file name for the main latex file
# 		 	$(SRC).tex should be the name of the latex file
# XSRC: Extra source files the main file depends on. This is used for checking
#       if we need to rebuild, so you can include images, subfiles, and the like
#       here. Therefore, DO include the file extension.
# CSS: name of the custom css file to be appended to the generated one
# 		 DO NOT allow the name of the src file to be the same as the CSS
# FILES: The name of constant files that need to be present in the html build.
# HFILES: The name of constant files that need to be present in the html build
#         but should be prepended by a period.
# Do not include extension in SRC.
# Adding new static files is as simple as dropping them in the directory. They
# will automatically be added to the build.
SRC:=setup
XSRC:=envs/csc.tex envs/macos.tex envs/ubuntu.tex envs/windows.tex
CFG:=setup
CSS:=custom_css.css
FILES:=
HFILES:=htaccess

# Created variables used in the build process, don't touch these.
HTML_DIR:=$(SRC)_html
HTML_DEST:=$(HTML_DIR)/$(SRC).html
PDF_DIR:=$(SRC)_pdf
PDF_DEST:=$(PDF_DIR)/$(SRC).pdf
HFILESDOT:=$(foreach file, $(HFILES), .$(file))
STATICS:=$(shell find static -type f)
DEPENDS:=$(SRC).tex $(XSRC) $(FILES) $(HFILES) $(CSS) $(CFG).cfg

.PHONY: all html pdf clean

all: html pdf


# Depend on the result files so we don't rebuild unless there's an actual change
# with the original tex file. HTML_DEST is a little misleading because it only
# checks for the existence of the $(SRC).html file, but as long as someone isn't
# willfully breaking the build, this is enough.
html: $(HTML_DEST) $(STATICS:%=$(HTML_DIR)/%)
pdf: $(PDF_DEST)

# ------ HTML TARGETS
# Building the HTML files.
$(HTML_DEST): $(DEPENDS)
	htlatex $(SRC).tex "$(CFG),3,next" ""
	mkdir -p $(HTML_DIR)
	mv -f $(SRC)*.html $(HTML_DIR)
	mv -f $(SRC).css $(HTML_DIR)
	$(foreach file, $(FILES), cp $(file) $(HTML_DIR)/$(file))
	$(foreach file, $(HFILES), cp $(file) $(HTML_DIR)/.$(file))
	cat $(CSS) >> $(HTML_DIR)/$(SRC).css
	rm -f $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi $(SRC).idv\
		$(SRC).tmp $(SRC).xref $(SRC).out	$(SRC).lg $(SRC).log

# Copying the statics over
$(foreach file, $(STATICS), $(HTML_DIR)/%): %
	@mkdir -p $(@D)
	cp $< $@

# ------ PDF TARGETS
# Building the PDF file.
$(PDF_DEST): $(DEPENDS)
	pdflatex -interaction=nonstopmode -file-line-error-style $(SRC)
	mkdir -p $(PDF_DIR)
	mv -f $(SRC).pdf $(PDF_DIR)
	rm -f $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi $(SRC).idv\
		$(SRC).tmp $(SRC).xref $(SRC).out	$(SRC).lg $(SRC).log

clean:
	rm -f $(SRC)*.html $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi
	rm -f $(SRC).tmp $(SRC).xref $(SRC).out $(SRC).pdf $(SRC).idv $(SRC).lg
	rm -f $(SRC).css $(SRC).log
	rm -f $(SRC)*x.png
	rm -rf $(HTML_DIR) $(PDF_DIR)
