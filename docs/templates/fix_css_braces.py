p = "build_page_hub.py"
s = open(p, encoding="utf-8").read()
start = s.index(".bar{display:flex")
end = s.index("</style>", start)
block = s[start:end]
fixed = block.replace("{", "{{").replace("}", "}}")
s = s[:start] + fixed + s[end:]
open(p, "w", encoding="utf-8").write(s)
print("css braces escaped")
