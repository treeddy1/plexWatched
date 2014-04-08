#plexWatched

simple python script for listing watched TV episodes and movies.  I wrote it on ubuntu so I could generate "rm" command lines to delete the files.  

## How it got started

I have been a longtime [SickBeard](http://http://sickbeard.com/) and [XBMC](http://xbmc.org/) user.  Then one day XBMC started to suck on my ATV2, and I wanted a multi-user implementation (you know to keep my kids from watching my shows). So I switched to Plex, and I love it. But I realized there wasn't a built in way to output that information and then delete files.  I was looking for a project to get started wtih Python and plexWatched was born.  After I started to investigate how to implement multi-user, I found [plexWatch](https://github.com/ljunkie/plexWatch) and [plexWatchWeb](https://github.com/ecleese/plexWatchWeb).  So the name plexWatched is a tip of the hat to those guys.  I find that [plexWatch](https://github.com/ljunkie/plexWatch) just did way more than I wanted, so I kept the script (relatively) simple.  

## Credits

As you browse through my code, you will notice some similarities to the Plex notifier from SickBeard. To give myself a headstart I copied midgetspy's connection function.


##What it does

+ Identifies TV Show, and Movie libraries (currently only one each)
+ Lists all the episodes and movies, then outputs the ones that have been marked watched.
+ plexWatched supports local authentication


##What it doesn't do

+ It does not support Multi-User conifgurations. It will work just fine for the account you specify, but has no idea what the other accounts you have shared your library with have watched.


###Future features:

+ Delete instead of outputing command lines
+ Write command lines to file, instead of outputing them to the console
+ Potentially support multi-user (would like to see plex implement that in the API)
+ Build a web interface for it
+ Add config file support, so you don't have to specify the options evertime you run

