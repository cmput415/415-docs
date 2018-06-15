# SRC: The file name for the latex file
# 		 	$(SRC).tex should be the name of the latex file
# CSS: name of the custom css file to be appended to the generated one
# 		 DO NOT allow the name of the src file to be the same as the CSS
# Do not include extension in SRC. 
SRC=setup
CFG=setup
CSS=custom_css.css


all:
	htlatex $(SRC).tex "$(CFG),3,next" "" 
	pdflatex -interaction=nonstopmode -file-line-error-style $(SRC)
	mkdir -p $(SRC)
	mv -f $(SRC)*.html $(SRC)
	mv -f $(SRC).css $(SRC)
	mv -f $(SRC).pdf $(SRC)
	cp static $(SRC) -r
	cat $(CSS) >> $(SRC)/$(SRC).css
	rm -f $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi $(SRC).idv 
	rm -f $(SRC).tmp $(SRC).xref $(SRC).out	$(SRC).lg $(SRC).log 

html: $(SRC).tex
	htlatex $(SRC).tex "$(CFG),3,next" "" 
	mkdir -p $(SRC)
	mv -f $(SRC)*.html $(SRC)
	mv -f $(SRC).css $(SRC)
	cp static $(SRC) -r
	cat $(CSS) >> $(SRC)/$(SRC).css
	rm -f $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi $(SRC).idv 
	rm -f $(SRC).tmp $(SRC).xref $(SRC).out	$(SRC).lg $(SRC).log 

pdf: $(SRC).tex
	pdflatex -interaction=nonstopmode -file-line-error-style $(SRC)
	mkdir -p $(SRC)
	mv -f $(SRC).pdf $(SRC)
	rm -f $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi $(SRC).idv 
	rm -f $(SRC).tmp $(SRC).xref $(SRC).out	$(SRC).lg $(SRC).log 

clean:
	rm -f $(SRC)*.html $(SRC).4ct $(SRC).4tc $(SRC).aux $(SRC).div $(SRC).dvi
	rm -f $(SRC).tmp $(SRC).xref $(SRC).out $(SRC).pdf $(SRC).idv $(SRC).lg
	rm -f $(SRC).css $(SRC).log 
	rm -rf $(SRC)
