#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Insta Feed Downloader Script

This script will download photos or albums posted on the user's own Instagram feed. The script takes in the credentials
for an Instagram account. The username defaults to "goelrohan" if none is provided, and the password can be provided by
a command line arg or with an environment variable "INSTA_PASSWORD".

It prompts the username for a nickname for a post that is used in directory paths, URL slugs, and descriptions. It
downloads photos to a _drafts directory and pre-populates a markdown Jekyll blog post with some relevant details.
To publish the post, move it from the _drafts directory to the _travels directory.

If the script successfully processes a post, it adds the post ID to an exclusion list located at .insta_exclude_list. This
is to prevent the script from prompting the user about a successful post on future runs. If you desire to process the post
again, delete the relevant ID from the exclusion list.

This script is built using the instagrapi library. As it attempts to access the Instagram API, it may encounter errors and
tries fallback versions API.  This may result in nuisance errors that don't affect processing of the posts.

Helpful hints: If you receive an instagrapi.exceptions.ChallengeRequired error, log into Instagram from a browser or the app.

"""

from instagrapi import Client
from PIL import Image

import argparse
import os
import shutil

img_root_dir = "img" # expected path is /blog/img/yyyy/m-post-slug
blog_root_dir = "_drafts" # expected path is /_drafts/yyyy-mm-dd-slug
exclusion_file = ".insta_exclude_list"

front_matter_template = """---
layout: [slideshow, post]
title: {title}
type: photos
category: travel
location: {location_name}
country:
coordi: {coordinates}
image: {cover_image}
MarkerSize: small
ext: {ext}
publish: yes
redirect_from:  
  - /{slug}/       
description: {description}

photos:
{photos}
---
"""

def rename_photos_in_dir(directory_path: str, file_list: list):
    new_file_list = []
    for i, file_name in enumerate(file_list):
        extension = str(file_name).split(".")[-1]
        new_file_name = os.path.join(directory_path, "{}.{}".format(i+1, extension))
        os.rename(os.path.join(directory_path, str(file_name)), new_file_name)
        new_file_list.append(os.path.join("/", new_file_name))

    return new_file_list

def make_cover_photo(directory_path: str):
    cover_photo_name = sorted(os.listdir(directory_path))[0]
    extension = cover_photo_name.split(".")[-1]
    new_file_name = os.path.join(directory_path, "{}.{}".format("cover-min", extension))
    shutil.copyfile(os.path.join(directory_path, cover_photo_name), new_file_name)
    pil_image = Image.open(new_file_name)
    i = pil_image.size   # current size (height,width)
    pil_image = pil_image.resize(i, Image.Resampling.LANCZOS)
    pil_image.save(new_file_name, optimize=True, quality=95)
    return os.path.join("/", new_file_name)

def add_to_exclusion_file(pk: int):
    with open(exclusion_file, 'a+') as f:
        f.write("{}\n".format(str(pk)))

def main(args: argparse.Namespace):
    """ Main entry point of the app """

    # Read in the list of posts to exclude
    exclusion_list = []
    if os.path.exists(exclusion_file):
        with open(exclusion_file, "r") as f:
            for line in f:
                exclusion_list.append(line.strip())

    insta_username = args.username

    cl = Client()
    cl.login(username=insta_username, password=args.password, verification_code=str(args.verification_code))
    total_media_count = cl.user_info_by_username(insta_username).media_count

    print("Checking media for user {}, starting with most recent post...".format(insta_username))

    should_find_next_post = True
    end_cursor = None
    media_found_count = 0
    while should_find_next_post:
        downloaded_file_list = []
        media, end_cursor = cl.user_medias_paginated(cl.user_id, 1, end_cursor=end_cursor)
        if len(media) < 1:
            print("Returned media object, but no media found.")
            break
        current_post = media[0]
        media_found_count += 1

        if media_found_count >= total_media_count:
            # We've come to the last post in the feed
            should_find_next_post = False

        current_post_date = current_post.taken_at.date()
        print("\nProcessing post {} from {} with description: {}".format(current_post.pk, current_post_date.isoformat(), media[0].caption_text))

        if str(current_post.pk) in exclusion_list:
            print("Found post {} in exclusion list, moving on to next post.".format(current_post.pk))
            continue

        user_in = input("Enter a nickname for this post, or type s(kip) or e(xit)\n")
        if user_in.lower() in ("e", "exit"):
            print("Exiting...")
            break
        if user_in.lower() in ("s", "skip"):
            print("Moving on to next post, excluding this one...")
            # If we made it this far successfully, let's prevent ourselves from processing this post again
            add_to_exclusion_file(current_post.pk)
            continue

        post_slug = user_in
        img_directory_path = os.path.join(img_root_dir, str(current_post_date.year), "{}-{}".format(current_post_date.month, post_slug))
        print("Putting photos in directory {}".format(img_directory_path))

        if os.path.exists(img_directory_path):
            if len(os.listdir(img_directory_path)) > 0:
                print("Warning: path {} already exists and has files, you must delete the files if you want to redownload them...".format(img_directory_path))
                file_exists_input = input("Type s(kip) to skip downloading, or type anything to continue...\n")
                if file_exists_input.lower() in ("s", "skip"):
                    print("Moving on to next post...")
                    add_to_exclusion_file(current_post.pk)
                    continue
        else:
            os.makedirs(img_directory_path)

        if current_post.media_type == 1:
            downloaded_path = cl.photo_download(current_post.pk, img_directory_path)
        elif current_post.media_type == 8:
            downloaded_path = cl.album_download(current_post.pk, img_directory_path)
        elif current_post.media_type == 2:
            if current_post.product_type == 'feed':
                downloaded_path = cl.video_download(current_post.pk, img_directory_path)
            if current_post.product_type == 'igtv':
                downloaded_path = cl.igtv_download(current_post.pk, img_directory_path)
            if current_post.product_type == 'clips':
                downloaded_path = cl.clip_download(current_post.pk, img_directory_path)
        else:
            print("Unexpected media type found while processing post, not a photo or album: {}".format(current_post.id))
            continue
        if hasattr(downloaded_path, "__len__") and len(downloaded_path) > 1:
            downloaded_file_list = downloaded_path
        else:
            downloaded_file_list.append(downloaded_path)

        enumerated_file_names = rename_photos_in_dir(img_directory_path, downloaded_file_list)
        if current_post.media_type != 2:
            cover_photo_name = make_cover_photo(img_directory_path)
        else:
            print("Not making a cover photo, unsupported media {}".format(downloaded_path))
            cover_photo_name = None

        blog_post_name = "{}-{}.md".format(current_post_date.isoformat(), post_slug)
        blog_post_path = os.path.join(blog_root_dir, blog_post_name)
        if os.path.isfile(blog_post_path):
            print("Warning: path {} already exists, you must delete it or move it to recreate it...".format(blog_post_path))
            file_exists_input = input("Type s(kip) to skip creating it, or type anything to continue...\n")
            if file_exists_input.lower() in ("s", "skip"):
                print("Moving on to next post...")
                continue

        front_matter_dict = {}
        front_matter_dict["title"] = post_slug
        front_matter_dict["location_name"] = "" if current_post.location is None else current_post.location.name
        front_matter_dict["coordinates"] = "" if current_post.location is None else "({},{})".format(current_post.location.lat, current_post.location.lng)
        front_matter_dict["ext"] = extension = enumerated_file_names[0].split(".")[-1]
        front_matter_dict["cover_image"] = cover_photo_name
        front_matter_dict["slug"] = post_slug
        front_matter_dict["description"] = "\"{}\"".format(current_post.caption_text.replace('"','\\"'))
        photos = ""
        for photo_name in enumerated_file_names:
            photos += "  - image: {}\n    caption:\n".format(photo_name)
        front_matter_dict["photos"] = photos

        if not os.path.exists(blog_root_dir):
            os.makedirs(blog_root_dir)
        blog_file = open(blog_post_path, "w")
        blog_file.write(front_matter_template.format(**front_matter_dict))
        blog_file.close()
        print("Created blog post draft at {}".format(blog_post_path))

        # If we made it this far successfully, let's prevent ourselves from processing this post again
        add_to_exclusion_file(current_post.pk)

    if media_found_count >= total_media_count:
        print("Reached last post in the feed.")


def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True}
    )

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("-u", "--username", default="goelrohan", help="Instagram Username")
    PARSER.add_argument("-p", "--password", **environ_or_required("INSTA_PASSWORD"), help="Instagram Password")
    PARSER.add_argument("-c", "--verification_code", help="Instagram verification code")

    # Optional argument flag which defaults to False
    PARSER.add_argument("-f", "--flag", action="store_true", default=False)

    MYARGS = PARSER.parse_args()
    main(MYARGS)