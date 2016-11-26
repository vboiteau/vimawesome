#!/bin/bash
current=${pwd}
cd $HOME/.vim/bundle;git clone $1
cd $current
