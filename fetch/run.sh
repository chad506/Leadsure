#!/usr/bin/env bash
set -u
mkdir -p fetch/out
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
while IFS=$'\t' read -r name url; do
  [ -z "${name:-}" ] && continue
  case "$name" in \#*) continue ;; esac
  ok=0
  for i in 1 2 3; do
    if curl -sS -m 60 -A "$UA" -H 'Accept-Language: en-US,en;q=0.9' \
         --compressed "$url" -o "fetch/out/$name.html"; then ok=1; break; fi
    sleep 3
  done
  [ "$ok" = 1 ] || echo "FETCH_ERROR $url" > "fetch/out/$name.html"
  sleep 2   # robots.txt crawl-delay
done < fetch/list.tsv
date -u +%FT%TZ > fetch/out/_fetched_at.txt
