Playblast plus uses ffMpeg to transcode the preview image sequences into a H264 encoded MP4. It does this seamlessly after the preiew stage, but you need to have the executable located somewhere on your local system.

I don’t bundle the executable with the code base for a number of reasons, but the main one is so that the encoding step is offloaded to the local machine, while the main codebase can be run from a network. Whilst Playblast Plus will work fine when installed locally, run from a netwrok means the studio template default is applied across the board, and any changes to this will be adopted studio-wide automatically.

<img align="right" src="https://thelineanimation.github.io/playblast-plus/_images/downloader.gif"/>


Playblast Plus will search any locations that are present in the config.json and look for ffMpeg.exe. If it doesn’t find any, it will present you with a downloader to do this.

This will download the ffMpeg version specified in the config key ffmpeg:download_url to the current user directory. Simply unpack the zip and drop ffMpeg.exe into one of the locations shown, or install to a folder of your choice and update config.json to include this path.

If you don’t alter the first entry of the executable_paths entry, it will resolve a relative folder called /bin in the current script environment.

I don’t unpack and move this automatically, I decided it’s ok for someone to decide where they run this from.