#!/bin/bash
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
#
# Build knowledge graph from wiki pages
# Usage: ./scripts/build-graph.sh
#
# Generates graph/data.json for use with graph/graph.html

WIKI_DIR="${WIKI_DIR:-wiki}"
OUTPUT_DIR="${OUTPUT_DIR:-graph}"

echo "📊 Building knowledge graph from $WIKI_DIR..."

# Check wiki exists
if [ ! -d "$WIKI_DIR" ]; then
    echo "❌ Wiki directory not found: $WIKI_DIR"
    exit 1
fi

# Initialize arrays
declare -a node_lines
declare -a edge_lines

# Process all markdown files
while IFS= read -r -d '' file; do
    # Skip hidden files
    [[ $(basename "$file") == .* ]] && continue
    
    # Get relative path and extract type
    rel_path="${file#$WIKI_DIR/}"
    dir_name=$(dirname "$rel_path")
    base_name=$(basename "$rel_path" .md)
    
    # Determine node type
    case "$dir_name" in
        sources) node_type="sources" ;;
        entities) node_type="entities" ;;
        concepts) node_type="concepts" ;;
        synthesis) node_type="synthesis" ;;
        *) node_type="other" ;;
    esac
    
    # Create label from filename
    label=$(echo "$base_name" | tr '-' ' ')
    
    # Add node
    node_lines+=("    { \"id\": \"$base_name\", \"label\": \"$label\", \"type\": \"$node_type\" }")
    
    # Extract wikilinks and create edges
    while IFS= read -r link; do
        [ -z "$link" ] && continue
        edge_lines+=("    { \"from\": \"$base_name\", \"to\": \"$link\" }")
    done < <(grep -oP '\[\[\K[^\]|]+' "$file" 2>/dev/null | sort -u)
    
done < <(find "$WIKI_DIR" -name "*.md" -type f -print0 2>/dev/null | sort -z)

# Write data.json
mkdir -p "$OUTPUT_DIR"

{
    echo "{"
    echo "  \"nodes\": ["
    
    # Join nodes with commas
    first=true
    for node in "${node_lines[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        echo -n "$node"
    done
    echo ""
    
    echo "  ],"
    echo "  \"edges\": ["
    
    # Join edges with commas
    first=true
    for edge in "${edge_lines[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            echo ","
        fi
        echo -n "$edge"
    done
    echo ""
    
    echo "  ]"
    echo "}"
} > "$OUTPUT_DIR/data.json"

echo "✅ Generated $OUTPUT_DIR/data.json"
echo "   ${#node_lines[@]} nodes, ${#edge_lines[@]} edges"
echo ""
echo "Open graph/graph.html in a browser to visualize."
