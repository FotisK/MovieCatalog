MovieCatalog
========

## What is MovieCatalog?
It's a python script that fetches movie data from various sources (imdb,tmdb) and generates a user-friendly catalog for all the movies the user has inside a folder.

![image1](readme.resources/scroll09.gif) ![movie page](readme.resources/moviepage03.gif)

The resulting catalog can be found inside the `index.html` file. 

    (!) MovieCatalog does NOT download movies.

## How does MovieCatalog find which movies to download data for?
**MovieCatalog** is filesystem-based meaning that it scans a specific folder (*Source*) for files and folders (eg. .srt files, movie, .torrent files or .txt files) and fetches the information for the movies extracted from the filenames. The downloaded data are kept in a `cache` folder.

## Features
### runs on demand
**MovieCatalog** does not run in the background - The .py script updates the catalog by scanning changes in the *Source* folder, fetching the data and rebuilding the monolithic `index.html` file. 
### is filesystem-based
You need only manage your movie files (Source). The script makes sure that there is parity between the source movie files/folders and the cached data. If a movie exists and its cache doesn't, it fetches the data. If a movie does not exist, it deletes its cache.
### Contains various filters for data sorting/filtering
Allows various sorting options, as well as filtering by media type (movie,tv series) or combined genres (by pressing Cmd/Ctrl)

![filtering](readme.resources/filter04.gif)

**MovieCatalog** allows full-text searching inside keyword, synopsis, cast and crew data, alternative titles, ratings, release year etc.

![searching](readme.resources/search03.gif)

### Other features
The MovieCatalog `index.html` page is responsive, allows switching between light/dark mode easily and links to trailers for a one-stop experience!

![dark mode](readme.resources/trailer01.gif)

Ratings link to IMDB and themoviedb.org, whereas Cast and Crew link to their IMDB profile. It also displays the Director of Photography/Cinematographer along with the Directors.

## Using
This is the readme file!

## Limitations on ...
Tested with databased <700

## future work

## installation