from comicgeeks import Comic_Geeks

# client = Comic_Geeks("8fa189492b034ff53653b8b7012acdf5f9c9516c")
client = Comic_Geeks()
data = client.issue_info(3616996)
# data = client.series_info(150065)

print(data.name)
