#!/usr/bin/env bash

sudo mkdir /usr/share/fonts
sudo chmod 777 /usr/share/fonts
sudo cp tce_cron_fonts/SimHei.ttf /usr/share/fonts/SimHei.ttf
sudo rm -rf ~/.cache/matplotlib/
