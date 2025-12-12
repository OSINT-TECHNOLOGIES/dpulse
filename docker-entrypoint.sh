#!/bin/sh
set -e


if [ ! -d service ]; then
    mkdir -p service
fi

if [ ! -f service/config.ini ] && [ -f /app/service/config.ini ]; then
    cp /app/service/config.ini service/config.ini
fi

if [ ! -d dorking ]; then
    mkdir -p dorking
fi

if ls /app/dorking/*.db >/dev/null 2>&1; then
  for dbfile in /app/dorking/*.db; do
    dest="dorking/$(basename "$dbfile")"
    if [ ! -f "$dest" ]; then
        cp "$dbfile" "$dest"
    fi
  done
fi

if [ -d /app/service/pdf_report_templates ]; then
  if [ ! -d service/pdf_report_templates ]; then
      mkdir -p service/pdf_report_templates
  fi

  for tmpl in /app/service/pdf_report_templates/*; do
      dest="service/pdf_report_templates/$(basename "$tmpl")"
      if [ ! -f "$dest" ]; then
          cp "$tmpl" "$dest"
      fi
  done
fi

exec python /app/dpulse.py
