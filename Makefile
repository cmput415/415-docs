# DIRS: Directories we need to build. The results should be in a subdirectory of
#       the same name. (e.g. setup/setup)
# FILES: Files we need to get from the base folder.
# HFILES: Hidden files we need to get from the base folder. These will be moved
#         into the build folder preprended with a period.
DIRS:=setup
FILES:=
HFILES:=htaccess

# Created variables used in the build process, don't touch these.
HFILESDOT:=$(foreach file, $(HFILES), .$(file))

.PHONY: all remoteinstall clean

all:
	@$(foreach dir, $(DIRS), $(MAKE) -C $(dir))

remoteinstall: all
	@$(foreach dir, $(DIRS), $(MAKE) -C $(dir))
	@# Make the build directory and zip it.
	mkdir .build
	$(foreach dir, $(DIRS), cp -r $(dir)/$(dir)_html .build/$(dir))
	$(foreach file, $(HFILES), cp base/$(file) .build/.$(file))
	$(foreach file, $(FILES), cp base/$(file) .build/$(file))
	tar -czf .build.tar.gz -C .build $(DIRS) $(HFILESDOT) $(FILES)

	@# Move to ohaton and install it.
	scp .build.tar.gz c415@ohaton.cs.ualberta.ca:~/.build.tar.gz
	ssh c415@ohaton.cs.ualberta.ca \
		'tar -xzf .build.tar.gz -C /compsci/webdocs/c415/web_docs/;'\
		'rm -f .build.tar.gz'

	@# Clean up.
	rm -rf .build .build.tar.gz

clean:
	$(MAKE) -C setup/ clean
	rm -rf .build .build.tar.gz
