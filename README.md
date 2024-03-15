![Helios Logo](https://heliosmusic.io/application/files/thumbnails/large/4615/2807/9653/Helios-Logo.png "Helios Logo")

# Helios Client API (Pure Python 3 Module)

This is an easy to use pure Python 3 module that provides an API to communicate with a remote [Helios](https://www.heliosmusic.io) server. You can manage your music catalogue as well as perform similarity matches. You can review the raw REST API documentation [here](https://www.heliosmusic.io/api.html).

## What is Helios?

Helios is a powerful B2B technology to allow searching of large commercial music libraries by using music itself as the search key. There are many uses, but here are a few examples:

- You have a commercial music library of any size. Perhaps you are a major record label, perhaps independent, or maybe you've amalgamated music from multiple labels, independent artists, or publishers. You need to assist your clients with obtaining synchronization licenses quickly for appropriate pieces of music for their film, TV, documentary, commercial, video game, or some other context.

- Your business receives a new supply of music each month from artists. You need to be able to predict which new music is more likely to generate revenue based on how existing music in your catalogue already performed.

- You have a digital jukebox in bars, restaurants, and pubs. You want venue patrons to be able to play more music like the music they just paid to hear.

- You have a music catalogue management platform that publishers and labels use to track their digital assets. Your customers want to be able to search within their own catalogue using your slick platform.

- You have an online digital music store and you'd like to be able to make intelligent product recommendations to your customers based on what songs they already have in their shopping cart before they check out.

- You have a streaming music service for different venues or channels. You have in-house DJs that custom curate the playlists. You want to reduce their work as they create new ones.

- You have a streaming music service. The listener asked to skip the current track, but they also never want to hear anything similar again.

- You market software for DJs, such as plugins to manage their library. While they're performing live, a plugin in their favourite software suggests new tracks to mix or play next.

There are countless other examples, but let's talk about the first one. Nearly always, your client approaches you with samples already in hand. "Hey, do you have anything like this?" This could be an MP3 or a YouTube video URL. Because Helios allows you to search the catalogue using music itself as the search key, you could use the customer's samples directly to help them find what they're looking for.

Traditionally, in the absence of such technology, the way this has been done for decades may surprise many. It is both costly and involves many hours or even days of manual human labour which delays the business process. The business must manually search, usually using [textual tags](https://heliosmusic.io/index.php/faq#tagging), and listen to a great deal of irrelevant music in the hopes of finding the one the client is actually willing to spend money on.

## Quick installation

### Ubuntu
Packages already prepared for Ubuntu 23.10 (mantic) and later are available on our Personal Package Archive (PPA) [here](https://launchpad.net/%7Ekip/+archive/ubuntu/helios-public). To get the package installed and be up and running in seconds, just run the following two commands:

```console
$ sudo add-apt-repository ppa:kip/helios-public
$ sudo apt install python3-helios-client
```

### PyPi
If you are not using Ubuntu 23.10 or later and know what you are doing, you can use Python's ad hoc package management system. This is not recommended as a first choice because it is not as robust as a native package manager. But if you do choose to use `pip(1)` directly, you can always use it in a virtual environment.

```console
$ python -m venv Environment
$ source Environment/bin/activate
$ cd Environment
$ pip install helios-client
```

## Licensing

This Python module is released under the terms of the [LGPL 3.0](https://www.gnu.org/licenses/lgpl-3.0.html) or greater. Copyright (C) 2015-2024 Cartesian Theatre. See [Copying](./Copying) for more information.

