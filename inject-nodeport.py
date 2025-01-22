#!/usr/bin/env python3
import sys, yaml

# Load the Helm-generated YAML
documents = yaml.safe_load_all(sys.stdin.read())

output = []
for doc in documents:
    if doc and doc.get("kind") == "Service" and doc["metadata"]["name"] == "passbolt":
        for port in doc["spec"]["ports"]:
            if port["name"] == "https":
                port["nodePort"] = 30443
            if port["name"] == "http":
                port["nodePort"] = 30080
    output.append(doc)

# Output the modified YAML
yaml.safe_dump_all(output, sys.stdout)

