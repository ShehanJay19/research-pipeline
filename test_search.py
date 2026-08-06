from core.tools import web_search

results = web_search("solid-state battery commercialization 2026")

for r in results:
     print(r["title"], "-", r["url"])