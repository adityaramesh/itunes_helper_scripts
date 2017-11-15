# Overview

I often find myself needing to perform the same few tasks when organizing music in iTunes. Many of
these tasks are too cumbersome and time-consuming to do using iTunes' UI for more than a few files.
So, I wrote a few scripts to help me organize music more quickly. Here are the main features:

  - [**Edit song names with regex.**](scripts/atag_sub.py) Songs in an album often have long,
    redundant prefixes that make it difficult to read the name of the song currently being played,
    especially on mobile devices.
  - [**Reindex track numbers.**](scripts/atag_reindex.py) It's sometimes necessary to merge or split
    albums, but the iTunes interface makes it cumbersome to reindex the track numbers. This script
    renumbers the track numbers of all `n` files in a given directory. The file with the smallest
    track number is assigned the new track number `k`, and the file with the largest track number is
    assigned the new track number `k + n - 1`, where `k = 1` by default.

Note: after editing the metadata for a file, it must be reloaded by iTunes in order for the changes
to be reflected. This can be done either by playing the file, or by removing and readding the entire
album.

# Supported Formats

- MP3, MP4

# Requirements

- Python 3.6 and mutagen

# Example Usage

Note that in both of the examples below, the `-w` flag needs to be provided in order for the changes
to actually be committed. For safety reasons, the default behavior is to perform a dry run.

- View the names of all songs in `my_album`:


	python3.6 scripts/atag_sub.py my_album/*.mp4

- Strip the prefix "Prefix: " from the names of all songs in `my_album`:


	python3.6 scripts/atag_sub.py -p "Prefix: " -r "" my_album/*.mp4

- Reindex the track numbers of all songs in `my_album`:


	python3.6 scripts/atag_reindex.py my_album/*.mp4
