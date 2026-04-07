#!/usr/bin/env python3
"""
Graph Mirror: Export Obsidian vault link graph from a private vault
as a structured JSON artifact for the orchestrator agent.

The orchestrator agent reads this artifact to understand the full
topology of the private vault — which files exist, where they live,
and how they link together — WITHOUT any sensitive content.

Usage:
    python3 scripts/graph_mirror.py --source /path/to/private-vault --output /path/to/output.json
    (from skills/graph-mirror/)

Guardrails:
    - NEVER modifies source files in the private vault
    - Only writes a single JSON artifact to the output location
    - Strips ALL content, tags, metadata — keeps structure only
    - Respects --exclude patterns to skip sensitive files/folders
"""

import argparse
import json
import os
import re
from pathlib import Path


def extract_wikilinks(content: str) -> list[str]:
    """Extract all wiki-links [[link]] from markdown content."""
    # Match [[link]] and [[link|alias]]
    pattern = r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]'
    return list(set(re.findall(pattern, content)))


def build_graph(
    vault_path: Path,
    exclude_patterns: list[str] | None = None,
) -> dict:
    """
    Walk the vault and build a complete graph of all wiki-links.
    Returns a dict mapping each file's path to its outgoing link targets.
    """
    graph = {}
    
    import fnmatch
    
    def should_exclude(path: str) -> bool:
        if not exclude_patterns:
            return False
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False
    
    for md_file in sorted(vault_path.rglob("*.md")):
        rel_path = str(md_file.relative_to(vault_path))
        
        if should_exclude(rel_path) or str(md_file).startswith(".git"):
            continue
        
        try:
            content = md_file.read_text(encoding="utf-8")
            links = extract_wikilinks(content)
            # Normalize links: strip .md extension for consistency
            # The orchestrator agent will resolve these to actual files
            normalized_links = []
            for link in links:
                # Keep the link as-is (usually just the basename or path without .md)
                normalized_links.append(link)
            
            graph[rel_path] = {
                "links_to": sorted(normalized_links),
                "folder": str(Path(rel_path).parent),
            }
        except Exception as e:
            print(f"  Warning: Could not read {rel_path}: {e}")
            graph[rel_path] = {
                "links_to": [],
                "folder": str(Path(rel_path).parent),
            }
    
    return graph


def generate_artifact(
    graph: dict,
    vault_name: str = "private vault",
) -> dict:
    """Wrap the graph in the artifact format the orchestrator agent expects."""
    return {
        "_obsidian_graph_mirror": True,
        "source": vault_name,
        "description": (
            "This file mirrors the link topology of the private Obsidian vault. "
            "It contains file paths and their wiki-link connections ONLY. "
            "No file content, no tags, no metadata, no personal information. "
            "The orchestrator agent uses this to navigate the graph structure "
            "and suggest where to find information without accessing sensitive data."
        ),
        "graph": graph,
        "stats": {
            "total_files": len(graph),
            "total_links": sum(len(v["links_to"]) for v in graph.values()),
            "unique_targets": len(set(
                link
                for node in graph.values()
                for link in node["links_to"]
            )),
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Mirror Obsidian vault link graph as a structured JSON artifact"
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the source Obsidian vault (private)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the output JSON artifact (public vault destination)"
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Comma-separated glob patterns to exclude (e.g., '*.gitkeep,*secret*')"
    )
    parser.add_argument(
        "--vault-name",
        type=str,
        default="private vault",
        help="Human-readable name for the source vault"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing files"
    )
    
    args = parser.parse_args()
    
    exclude_patterns = [p.strip() for p in args.exclude.split(",") if p.strip()]
    
    if not args.source.exists():
        print(f"Error: Source vault not found: {args.source}")
        return
    
    print("=" * 60)
    print("Graph Mirror — Obsidian Vault Link Graph Export")
    print("=" * 60)
    print(f"Source: {args.source}")
    print(f"Output: {args.output}")
    
    graph = build_graph(args.source, exclude_patterns)
    artifact = generate_artifact(graph, args.vault_name)
    
    if args.dry_run:
        print(f"\n[DRY RUN] Would write {artifact['stats']['total_files']} file entries")
        print(f"  Total links: {artifact['stats']['total_links']}")
        print(f"  Unique link targets: {artifact['stats']['unique_targets']}")
        # Show first few entries as preview
        for i, (path, info) in enumerate(list(graph.items())[:5]):
            links = info['links_to']
            display = links[:3] + ['...'] if len(links) > 3 else links
            print(f"  {path} -> {display}")
        return
    
    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the artifact
    args.output.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    print(f"\nResults:")
    print(f"  Files indexed: {artifact['stats']['total_files']}")
    print(f"  Total links: {artifact['stats']['total_links']}")
    print(f"  Unique link targets: {artifact['stats']['unique_targets']}")
    print(f"\nArtifact written to: {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
