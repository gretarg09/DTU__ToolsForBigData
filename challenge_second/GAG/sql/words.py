symbols =

s = """**Most Popular Comments**   \n\n---\n|Score|Author|Post Title|Link to comment|\n|:-|-|-|-|\n|4186|/u/DrowningDream|[WP] A Man gets to paradise. Unfortunately, Lucifer won the War"""

s = s.lower()
for sym in symbols:
	s = s.replace(sym, " ")

words = set()
for w in s.split(" "):
	if len(w.replace(" ","")) > 0:
		words.add(w)

print words
