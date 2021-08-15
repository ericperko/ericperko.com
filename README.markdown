ericperko.com
=============

Backend code for Eric Perko's personal web site.

Built with Hugo

# Clone
git clone --recursive <URL to this git repo>
git submodule update --init --recursive

# Required dependencies
hugo == 0.87.0 (extended)

sudo snap install hugo --channel=extended

# Update the theme
git submodule update --remote

# Start a live server
cd site; hugo server -D

# Build the site
cd site; hugo -D

# Package the site & deploy
*Assumes that ssh keys have been setup properly*

cd site; rsync -avhnz --progress --delete public/ ericperko_ericperko@ssh.phx.nearlyfreespeech.net:/home/public/

Remove the **-n** to actually transfer the site.

# Misc Notes

Adding a theme:  git submodule add https://github.com/yoshiharuyamashita/blackburn.git site/themes/blackburn

Other Blackburn-based sites:
- https://masalmon.eu/bio/