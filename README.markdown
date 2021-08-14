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

# Package the site
cd site; tar -cavf ericperko-website.tar.gz public/
