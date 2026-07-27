#!/usr/bin/env bash
set -u
mkdir -p fetch/out
while IFS=$'\t' read -r name url; do
  [ -z "$name" ] && continue
  for i in 1 2 3; do
    curl -sf -m 40 "$url" -o "fetch/out/$name.json" && break
    sleep 2
  done
  [ -f "fetch/out/$name.json" ] || echo "{\"__fetch_error\":true}" > "fetch/out/$name.json"
done < fetch/list.tsv
date -u +%FT%TZ > fetch/out/_fetched_at.txt
