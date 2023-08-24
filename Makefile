# DIRS: Directories we need to build. The results should be in a subdirectory of
#       the same name. (e.g. setup/setup)
# FILES: Files we need to get from the base folder.
# HFILES: Hidden files we need to get from the base folder. These will be moved
#         into the build folder preprended with a period.
DIRS:=setup generator scalc vcalc gazprea
FILES:=index.html $(patsubst base/%,%,$(wildcard base/css/*)) $(patsubst base/%,%,$(wildcard base/engineering/*))
HFILES:=htaccess

# Created variables used in the build process, don't touch these.
HFILESDOT:=$(foreach file, $(HFILES), .$(file))
PDFS:=$(foreach file, $(DIRS), $(file).pdf)

.PHONY: all github clean 

all:
	$(foreach dir, $(DIRS), $(MAKE) html -C $(dir);)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_static/css/fonts;)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_static/fonts;)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_sources/;)
	$(foreach dir, $(DIRS), $(MAKE) latexpdf -C $(dir);)

github: all
	rm -rf _site
	mkdir _site
	mkdir _site/css
	mkdir _site/engineering
	$(foreach dir, $(DIRS), mkdir _site/$(dir);)
	$(foreach dir, $(DIRS), cp -r $(dir)/_build/html/* _site/$(dir);)
	$(foreach dir, $(DIRS), cp -r $(dir)/_build/latex/$(dir).pdf _site/$(dir).pdf;)
	$(foreach file, $(FILES), cp base/$(file) _site/$(file);)
	touch _site/.nojekyll

clean:
	$(foreach dir, $(DIRS), $(MAKE) -C $(dir) clean;)
	rm -rf .build .build.tar.gz
