# list of valid filetypes to treat as movie names in order to fetch their data
ValidFileTypes = [
    ".mkv",
    ".avi",
    ".mp4",
    ".mov",
    ".mpeg",
    ".txt",
    ".torrent",
    ".jpg",
    ".png",
]

# allow folders to be treated as movie names and fetch their data? True/False
includeFoldersInValidFileTypes = True

# personal themoviedb.org API key request one at:
# https://developers.themoviedb.org/3/getting-started/introduction
# after creating a free account
myTMDB_APIkey = ""  # <------ type keyinside quotes

# absolute path with the Source (movie) files:
SourcePath = ""  # eg. SourcePath='/Users/user1/Video/MyMovies'
# alternatively use relative path to the script by uncommenting the following line
# SourceRelativePath='' # <------- type relative path
