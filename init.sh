#!/bin/bash
echo ""
echo "`date '+%Y-%m-%d %H:%M:%S'` START"
python cloudflare-update.py
echo "`date '+%Y-%m-%d %H:%M:%S'` FINISH"
