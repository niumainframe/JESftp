#!/bin/bash

# This is used to install JESftp to NIU's department server.
# It will probably work on other Unixes that have bash, wget, and python.

# Make the bin directory, ignore if it does not exist.
mkdir ~/bin &> /dev/null

# Grab the latest version from the repository and save it in ~/bin/JESftp.py
wget -q -O ~/bin/JESftp.py https://raw.github.com/scvnc/JESftp/master/JESftp.py

# Give user executable permissions.
chmod u+x ~/bin/JESftp.py

# Provide alias for invoking python.
# Alternatively, you can add the python shebang line and ensure ~/bin is in your PATH.
alias JESftp.py='python ~/bin/JESftp.py'

# Save alias updates.
alias > ~/.bash_aliases

echo "Install Complete"