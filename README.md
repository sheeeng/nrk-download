# nrkdownload

This is yet another commandline tool to download programs and series from NRK (Norwegian public broadcaster). It is inspired by the already existing tools that you can find on GitHub. The reason I decided to make yet another tool, was that I found the source code of some of the other tools to be difficult to read and understand, and thus difficult to contribute to.

The tool is written in Python, and is compatible with Python 2.7 and 3.x. It has been tested under both Linux, MacOS and Windows.

## What does this tool add?
When you download a program with this tool, it doesn't just download that file. If the program is part of a series, directories for that series and season is created. And the file is automatically named according to its episode and season number. Subtitles and additional images are also automatically downloaded. The subtitles are automatically embedded in the .m4v-file, so you could decide to delete the .srt-file. (I have found that in some tools (like VLC), the support for included subtitles is not perfect. That's why the separate .srt-file is also there.)

The idea behind this is that the downloaded programs should integrate seamlessly into you favorite media server, e.g. [Plex](http://www.plex.tv). If you for example download all the episodes of the very popular series SKAM, you would get a directory-structure like this: 

```
SKAM
├── poster.jpg
├── Season 01
│   ├── SKAM - S01E01 - 1of11.jpg
│   ├── SKAM - S01E01 - 1of11.m4v
│   ├── SKAM - S01E01 - 1of11.no.srt
⋮
├── Season 02
│   ├── SKAM - S02E01 - 1of12.jpg
│   ├── SKAM - S02E01 - 1of12.m4v
│   ├── SKAM - S02E01 - 1of12.no.srt
⋮
└── Season 03
    ├── SKAM - S03E01 - 1of10.jpg
    ├── SKAM - S03E01 - 1of10.m4v
    ├── SKAM - S03E01 - 1of10.no.srt
    ⋮
    ├── SKAM - S03E10 - 10of10.jpg
    ├── SKAM - S03E10 - 10of10.m4v
    └── SKAM - S03E10 - 10of10.no.srt
```

## Usage
In order to download something, you first have to search for it. And you have to specify whether you are searching for a particular program, or if you are searching for a series.
```
$ nrkdownload -h
usage: nrkdownload [-h] [-s] [-p] [-d DIRECTORY] [--version] search_string

Download series or programs from NRK, complete with images and subtitles.

positional arguments:
  search_string

optional arguments:
  -h, --help            show this help message and exit
  -s, --series          Search for series
  -p, --program         Search for programs
  -d DIRECTORY, --dir DIRECTORY
                        The directory where the downloaded files will be
                        placed
  --version             show program's version number and exit
```

### Searching for a series
Let's say you are interested in downloading all the available episodes about the rescue boat "Elias". You would then use the flag `-s` to specify that you are searching for a series with the name Elias. If there is more than one matching series, you will be asked to specify which one of them you want. You respond to this by typing an integer and pressing Enter. If there is only one matching series, it skips directly to the next step:

Then, all of the registered episodes will be listed (due to copyright-issues, some of them might not be available for download). You then will be asked to specify what episodes you want to download. You respond to this by typing an integer or a range. The range can be specified in different ways:
- `5-10` or `5:10`, means all episodes from 5 to 10, including both 5 and 10.
- `-10` or `:10`, means all episodes from the start (0) to 10, including both 0 and 10.
- `10-` or `10:`, means all episodes from 10 to the last, including both 10 and the last.
- `-` or `:`, means all available episodes.

So the above would typically look like this in your terminal:
```
$ nrkdownload.py -s elias

Matching series:
 0: Elias på eventyr : 1 Sesong(er)
 1: Elias : 2 Sesong(er)

Enter a number in the range 0-1. (q to quit): 1

Matching programs
 0: Elias (Sesong 1): Elias - 1:26 - S01E01
 1: Elias (Sesong 1): Elias - 2:26 - S01E02
⋮
50: Elias (Sesong 2): Elias - 25:26 - S02E25
51: Elias (Sesong 2): Elias - 26:26 - S02E26

Enter a number or interval (e.g. 8 or 5-10). (q to quit): -10
Getting program details for your selection of 11 programs...
Ready to download 11 programs, with total duration 2:01:02
Downloading:  35%|█████████                 | 2.52K/7.26K [01:25<02:22, 33.1s/s]
```
The progress bar shows the number of seconds of video to be downloaded, in this case 2:01:02 = 2*3600 + 62 = 7262 seconds. The next two times are the estimated remaining and total download time. The last number shows how many seconds of video are downloaded per second. So in this snapshot, the video was downloaded at 33x the playback speed. 

If you have already downloaded some of the episodes, those will be automatically skipped (not overwritten).

### Searching for a program
If you were interested in programs where the name "Elias" was mentioned (as opposed to the series "Elias", as described above), you would specify that by using the flag `-p`. The results from the search will be programs, so all you have to do is to specify the program(s) you want by using the range syntax described above.

Note that if your search string consists of more than one word, you must surround it with single or double quotes.

In your terminal, that would look like this:
```
$ nrkdownload.py -p "redningsskøyta elias"

Matching programs
 0: Gratulerer med dagen! (2011): Gratulerer med dagen! 17.05.2011 - 17.05.2011 - S34E01
 1: Dagsrevyen (Januar 2013): Dagsrevyen 10.01.2013 - 10.01.2013 - S36E10
⋮
 6: Supernytt (2015): Supernytt 06.05.2015 - 06.05.2015 - S06E80
 7: Barne-tv - hele sendinger (2017): Barne-tv - 12.01.2017 - S02E12

Enter a number or interval (e.g. 8 or 5-10). (q to quit): 
```

### Configurable download directory
If you don't specify anything, the directories will be created inside `~/Downloads/nrkdownload`, where `~` means your home directory. If you want the downloads somewhere else (e.g. directly to your NAS), there are two ways to specify a different download directory:
- Define an environment variable named `NRKDOWNLOAD_DIR`
- Specify the download directory on the command line with the option `-d download_dir`

If you do both at the same time, the option from the command line will take precedence.

If you don't know how to define an environment variable under your operating system, try to Google `create environment variable` and the name of you operating system. (Under Linux and MacOS, you would want to edit your `~/.bash_profile`)

## Installing
The package and its requirements can be installed in several ways, depending on whether you want to just use it or whether you want to change the code. And since it is compatible with both Python 2 and 3, you can decide under what version of Python you want to run it.

Anyway, you should avoid installing it as root (Administrator), and keep your global Python-installation clean. This can be achieved in several ways:
1. Install it under you own home-directory by passing the `--user` option to the `pip` installer.
2. Install your own user-specific Python distribution, [Anaconda](https://www.continuum.io/downloads) is a good choice.
3. Create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and install in there.

In the following examples, it is assumed that your system has support for [user install directory](https://www.python.org/dev/peps/pep-0370/) (thus, example 1 above). This is true for standard Linux-distribution, Windows and MacOS.

If your system has both Python 2 and 3 installed, `pip` could be pointing to the Python-2 installation, whereas `pip3` points to the Python-3 installation. If that is the case for you, and you explicitly want to run this under Python-3, you can replace `pip` with `pip3` in these examples.

### Installing the latest official release
```
$ pip install --user nrkdownload
```
If you at some point want to upgrade to a newer version, add a `-U` (for Upgrade) just after install:
```
$ pip install -U --user nrkdownload
```

### Installing the latest revision directly from GitHub:
```
$ pip install --user git+https://github.com/marhoy/nrk-download.git#egg=nrkdownload
```
If you at some point want to upgrade to a newer version, use `-U` as described above.

### Installing in development mode:
If you want to change (and possibly contribute to) the code, first clone the repository. This will create a directory containing a local copy of the GitHub-repository. Then install in develop mode from this directory:
```
$ git clone https://github.com/marhoy/nrk-download.git
$ pip install --user -e nrk-download
```
You will then be able to use the tool as usual, but the installation will be a pointer to your local repository. Whatever changes you do in your local repository will have immediate effect on the "installation".

## Uninstalling
```
$ pip uninstall nrkdownload
```


### FFmpeg
The videos and subtitles are downloaded using [FFmpeg](https://ffmpeg.org/). It is available for all major operating systems.


# TODO
## URLs as input
It could be useful to specify an URL instead of a search string. The URLs could be like:
- `https://tv.nrk.no/program/KOID26004816/president-trump` for a specific program 
- `https://tv.nrk.no/serie/unge-lovende/KMTE20006115/sesong-2/episode-1` for a specific episode of a series
- `https://tv.nrk.no/serie/unge-lovende` for a whole series

For a program or a specific episode, the download could then start without requiring any other input. For a series, one could have a commandline-switch to specify the interval of episodes that you want to download. (The URLs could perhaps also be read from an input-file.) This would enable the download tool to run without requiring input from the user. It could therefore be run as a scheduled job via e.g. cron.

## More metadata?
Both series and programs/episodes have a description at tv.nrk.no. It could possibly be interesting to save these descriptions to a text file.
