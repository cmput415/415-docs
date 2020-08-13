# DIRS: Directories we need to build. The results should be in a subdirectory of
#       the same name. (e.g. setup/setup)
# FILES: Files we need to get from the base folder.
# HFILES: Hidden files we need to get from the base folder. These will be moved
#         into the build folder preprended with a period.
DIRS:=setup generator scalc vcalc gazprea
FILES:=
HFILES:=htaccess

# Created variables used in the build process, don't touch these.
HFILESDOT:=$(foreach file, $(HFILES), .$(file))
PDFS:=$(foreach file, $(DIRS), $(file).pdf)

.PHONY: all remoteinstall github clean

all:
	$(foreach dir, $(DIRS), $(MAKE) html -C $(dir);)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_static/css/fonts;)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_static/fonts;)
	$(foreach dir, $(DIRS), rm -rf $(dir)/_build/html/_sources/;)
	$(foreach dir, $(DIRS), $(MAKE) latexpdf -C $(dir);)

remoteinstall: all
	@# Make the build directory and zip it.
	mkdir .webdocs_build
	$(foreach dir, $(DIRS), cp -r $(dir)/_build/html/ .webdocs_build/$(dir);)
	$(foreach dir, $(DIRS), cp -r $(dir)/_build/latex/$(dir).pdf \
		.webdocs_build/$(dir).pdf;)
	$(foreach file, $(HFILES), cp base/$(file) .webdocs_build/.$(file);)
	$(foreach file, $(FILES), cp base/$(file) .webdocs_build/$(file);)
	tar -czf .build.tar.gz -C .webdocs_build $(DIRS) $(HFILESDOT) $(FILES) $(PDFS)

	@# Move to ohaton and install it.
	scp .build.tar.gz c415@ohaton.cs.ualberta.ca:~/.build.tar.gz
	ssh c415@ohaton.cs.ualberta.ca \
		'tar -xzf .build.tar.gz -C /compsci/webdocs/c415/web_docs/;'\
		'rm -f .build.tar.gz'

	@# Clean up.
	rm -rf .webdocs_build .build.tar.gz

github: all
	mkdir -p .github_build
	$(foreach dir, $(DIRS), mkdir .github_build/$(dir);)
	$(foreach dir, $(DIRS), cp -r -t .github_build/$(dir) $(dir)/_build/html/*;)
	touch .github_build/.nojekyll

clean:
	$(foreach dir, $(DIRS), $(MAKE) -C $(dir) clean;)
	rm -rf .build .build.tar.gz
