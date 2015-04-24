#!/bin/bash
git archive master | bzip2 >/tmp/xxx.tar.bz2
scp /tmp/xxx.tar.bz2 rune@bigdog:/tmp
ssh rune@bigdog 'mkdir /tmp/ttt;cd /tmp/ttt;tar xvjmf ../xxx.tar.bz2'
ssh rune@bigdog 'cp -rf /tmp/ttt/* /var/www/ghiro.beatmatic.it/'
ssh rune@bigdog 'rm -rf /tmp/ttt;rm /tmp/xxx.tar.bz2'