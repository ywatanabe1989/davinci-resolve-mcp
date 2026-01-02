<!-- ---
!-- Timestamp: 2025-12-29 09:50:15
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/davinci-resolve-mcp/docs/API_DOCS/GEMINI_SUGGESIONS.md
!-- --- -->

DaVinci Resolve does not have a public web-based API portal like many modern SaaS tools. Instead, its scripting documentation is bundled directly with the software installation or maintained through community-driven repositories. 
Official API Reference (Local Files)
The most authoritative and up-to-date documentation is located within your DaVinci Resolve installation directory. 
Access via UI: Open DaVinci Resolve and go to Help > Documentation > Developer.
Direct File Paths:
Windows: %PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt
macOS: /Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/README.txt
Linux: /opt/resolve/Developer/Scripting/README.txt 
Third-Party & Community References
Since official documentation is primarily a text file, several developers have created formatted web versions:
ExtremRaym's Formatted API Doc: A frequently updated, searchable web version of the official README.txt for DaVinci Resolve 20.
Unofficial GitHub Pages (Deric): A well-organized Markdown-to-HTML conversion of the scripting API.
DaVinci Resolve Wiki: A community-maintained wiki that includes basic function lists and examples. 
Fusion Scripting Reference
For advanced visual effects (Fusion) scripting, refer to the Fusion Scripting Guide (PDF). Although dated, many of the core objects and methods (such as those for Fusion nodes) remain valid. 
Key API Objects
The API is hierarchical, typically starting with the Resolve object: 
ProjectManager: Handles project creation, loading, and folder management.
Project: Manages the current project settings, timelines, and render jobs.
MediaPool: Used to import media, create bins, and manage assets.
Timeline: Provides access to track data and clip manipulation. 
Development Tools
VSCode Toolkit for Resolve: A VSCode extension providing autocompletion for Resolve API functions.
Interactive Console: Inside Resolve, you can use the Workspace > Console (Lua or Python) to test commands live. 

<!-- EOF -->