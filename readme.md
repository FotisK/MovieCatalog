MovieCatalog
========

## What is MovieCatalog?
It's a python script that fetches movie data from various sources (imdb,tmdb) and generates a user-friendly local media catalog.

![image1](readme.resources/scroll09.gif)

The resulting catalog is inside an `index.html` file. 

    (!) **MovieCatalog** does _NOT_ download movies.

## How does MovieCatalog find which movies to download data for?
**MovieCatalog** is filesystem-based meaning that it scans a specific folder (*Source*) for files and folders (eg. .srt files, movie, .torrent files or .txt files) and fetches the information for the movies extracted from filenames. The downloaded data are kept in a `cache` folder.

## Features
### runs on demand
**MovieCatalog** does not run in the background - The .py script updates the catalog by scanning changes in the *Source* folder, fetching the data and rebuilding the monolithic `index.html` file. 
### is filesystem-based
You need only manage your movie files (Source). The script makes sure that there is parity between the source movie files/folders and the cached data. If a movie exists and its cache doesn't, it fetches the data. If a movie does not exist, it deletes its cache.
### Contains various filter for data sorting/filtering
**MovieCatalog** allows full-text searching inside keyword, synopsis, cast and crew data, alternative titles, ratings, release year etc.

![searching](readme.resources/search03.gif)

Allows various sorting options, as well as filtering by media type (movie,tv series) or combined genres (by pressing Cmd/Ctrl)

![filtering](readme.resources/filter04.gif)

### Has dark mode
Switch between light and dark mode easily

![dark mode](readme.resources/darkmode03.gif)

### Quick view vs detailed view
Displays the movie's quick info inside the movie thumbnail and

![quickinfo](readme.resources/thumbnail04.gif)

and detailed info (eg. cinematographer, movie media, languages) when clicked on.

![dark mode](readme.resources/moviepage03.gif)

### Displays Trailer
Displays the movie trailer both on the thumbnail and the dedicated movie page.

![dark mode](readme.resources/trailer01.gif)

### Links to external sources
Ratings link to IMDB and themoviedb.org, whereas Cast and Crew link to their IMDB profile.


## Using
This is the readme file!



## Limitations on ...
Tested with databased <700