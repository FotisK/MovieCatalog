MovieCatalog
========

## What is MovieCatalog?
Movie Catalog is a python script that fetches movie data from various sources (imdb,tmdb) and generates a user-friendly catalog for all the movies the user has inside a folder. 

![image1](readme.resources/scroll09.gif)

I created it to best manage my watchlist and quickly scan for movie information without jumping from site to site.

![movie page](readme.resources/moviepage03.gif)

The resulting catalog can be found inside the `index.html` file. 

    (!) MovieCatalog is NOT a movie downloader.

## How does MovieCatalog find which movies to download data for?
**MovieCatalog** is filesystem-based meaning that it scans a specific folder (*Source*) for files and folders (eg. .srt files, video files, .torrent files or .txt files) and fetches the information for the movies extracted from the filenames. In other words, it treats the folder contents, as a list of movie names! The downloaded data are kept in a `cache` folder.

## Features
### runs on demand
**MovieCatalog** does not run in the background but can be automated to run when a file is added or removed from a folder (eg via smart folders/Automator) - The .py script updates the catalog by scanning changes in the *Source* folder, fetching the data and rebuilding the monolithic `index.html` file and then quits. 
### Is filesystem-based
You need only manage your movie files (Source). The script makes sure that there is parity between the source movie files/folders and the cached data. If a movie exists and its cache doesn't, it fetches the data. If a movie no longer exists, it simply deletes its cache.
### Contains various filters for data sorting/filtering
Allows various sorting options, as well as filtering by media type (movie,tv series) or combined genres (by pressing Cmd/Ctrl)

![filtering](readme.resources/filter04.gif)

**MovieCatalog** allows full-text searching inside keywords, synopsis, cast and crew data, alternative titles, ratings and things such as the release year etc.

![searching](readme.resources/search03.gif)

### Other features
The MovieCatalog `index.html` page is responsive, allows switching between light/dark mode easily and links to trailers in order to provide a one-stop experience to the user.
Ratings link to IMDB and themoviedb.org, whereas Cast and Crew link to their IMDB profile. It also displays the Director of Photography/Cinematographer along with the Directors.

## Using
This is the readme file!

## Limitations on ...
Tested with databased <700

## future work

## installation