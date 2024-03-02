# Scripts

Most of these scripts are standalone and don't require kohya scripts to be installed.

## combine_captions.py

This script merges two folders with text files with comma-separated tags which have the same file name and outputs it somewhere. You can also specify a threshold, to only add from second directory if there's not enough tags. You can also provide a **LINE** separated meta tags, as in example `metatags.txt`.

```sh
python scripts/combine_captions.py -c 35 -m scripts/metatags.txt ./workdir/danbooru ./workdir/wd_tagger ./workdir/combined
```

## crawl.py

Crawl danbooru with it and resize pics if you want.

By default, it will download 400 images if there's enough. If you want less, you can use --limit. If you also want to resize all pics to have an area of 1024x1024, use --align-images.

```sh
python scripts/crawl.py -s "sparkle_(honkai:_star_rail)" "order:score" -o ./workdir/crawl
```

## remove_text_orphans.py

Remove text files which don't have a corresponding image file located in the same folder.

```sh
python scripts/remove_text_orphans.py ./workdir/crawl
```