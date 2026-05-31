---
author: Orchestrator
status: active
timestamp: 2026-05-27
tags: [memory-scope, protocol, v4.5, orchestrator]
---

# Memory Scope Protocol (v4.5 Hyper-Native)

## 1. SCOUT Memory Scope
- **Store**: Trusted primary URLs, recurring blind spots, query strategies.
- **Skip**: Raw scraped web text (temporary execution buffers only).

## 2. SCRIBE Memory Scope
- **Store**: Output style preferences, Markdown/Obsidian graph taxonomies (tags), formatting rules.
- **Skip**: Draft versions of documents.

## 3. REACH Memory Scope
- **Store**: Target audience personas, historical campaign metrics, validated growth channels.
- **Skip**: Hallucinated projections or raw analytics dumps.

## 4. DEV Memory Scope
- **Store**: Environment facts (paths for uv, rg, obsidian), working architecture decisions, rollback patterns.
- **Skip**: Gigantic raw error logs (extract root cause instead).

## Trigger Rules & Autonomous Curation
- **Session Recall Trigger**: If an entity asks about past conversational details, use the native Honcho FTS5 session search; do not bloat workspace with chat transcripts.
- **Skill Creation Trigger**: If a complex multi-step procedure is repeated 3 times successfully, package it into a procedural prompt and hand it over to the native hermes curator subsystem for synchronization.
- **Vault Storage Trigger**: Any output longer than 400 words meant for preservation MUST go to /home/hiryu/.hermes/vault/<agent>/ as a .md file.