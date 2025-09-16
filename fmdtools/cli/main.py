#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fmdtools CLI - Interactive model builder wizard.
"""

import sys
from .nlp_wizard import main as nlp_wizard

def main():
    """Main CLI entry point - requires 'create' command."""
    args = sys.argv[1:]
    
    # Show help if requested or no command given
    if not args or args[0] in ["-h", "--help", "help"]:
        print("fmdtools - Interactive Model Builder")
        print("Creates fmdtools models through guided questions.")
        print("")
        print("Usage:")
        print("  fmdtools create    Start the interactive model builder")
        print("  fmdtools --help    Show this help message")
        return
    
    # Check for create command
    if args[0] == "create":
        nlp_wizard()
    else:
        print(f"Unknown command: {args[0]}")
        print("Use 'fmdtools create' to start the model builder")
        print("Use 'fmdtools --help' for more information")

if __name__ == "__main__":
    main()