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

from datetime import datetime
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from PIL import Image

import argparse
import logging
import os
import shutil
import sys

img_root_dir = "img" # expected path is /img/yyyy/m-post-slug
blog_root_dir = "_travels" # expected path is /_travels/yyyy-mm-dd-slug
exclusion_file = ".insta_exclude_list.txt"
insta_session_file = ".insta_session.json"

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
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

def login_user(username: str, password: str, verification_code: str):
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password. Verification code is optional.
    """

    cl = Client()
    if os.path.exists(insta_session_file):
        session = cl.load_settings(insta_session_file)
    else:
        session = cl

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login (username, password) # this doesn't actually login using username/password but uses the session

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(username=username, password=password, verification_code=verification_code)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % username)
            if cl.login(username, password, verification_code=verification_code):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    return cl

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
    (orig_h, orig_w) = pil_image.size   # current size (height,width)

    aspect = orig_w / float(orig_h)

    ideal_width = 400
    ideal_height = 300

    ideal_aspect = ideal_width / float(ideal_height)

    if aspect > ideal_aspect:
        # Then crop the left and right edges:
        new_width = int(ideal_aspect * orig_h)
        offset = (orig_w - new_width) / 2
        resize = (offset, 0, orig_w - offset, orig_h)
    else:
        # ... crop the top and bottom:
        new_height = int(orig_w / ideal_aspect)
        offset = (orig_h - new_height) / 2
        resize = (0, offset, orig_w, orig_h - offset)

    pil_image = pil_image.crop(resize).resize((ideal_width, ideal_height), Image.Resampling.LANCZOS)
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

    try:
        cl = login_user(insta_username, args.password, str(args.verification_code))
    except Exception as e:
        logger.error("Couldn't login using either username/password or saved session. Please try again by providing credentials on the command line. error: %s" % e)
        quit()

    # Save login info settings for next time
    cl.dump_settings(insta_session_file)
    cl.request_timeout = args.timeout
    total_media_count = cl.user_info_by_username(insta_username).media_count

    logger.info("Checking media for user {}, starting with most recent post...".format(insta_username))
    if args.date:
        date_to_search_for = args.date.date()
        logger.info("Looking chronologically backwards for posts with date {}, overriding exclude list".format(date_to_search_for))
    else:
        date_to_search_for = None

    should_get_next_page = True
    end_cursor = None
    media_found_count = 0
    while should_get_next_page:
        media_list, end_cursor = cl.user_medias_paginated(cl.user_id, 10, end_cursor=end_cursor)
        if len(media_list) < 1:
            logger.error("Returned media object, but no media found.")
            break
        for current_post in media_list:
            downloaded_file_list = []
            media_found_count += 1

            if media_found_count >= total_media_count:
                # We've come to the last post in the feed
                should_get_next_page = False

            current_post_date = current_post.taken_at.date()

            if date_to_search_for:
                if date_to_search_for != current_post_date:
                    logger.info("Found post with date {}, continuing on until we find {}".format(current_post_date, date_to_search_for))
                    continue
                # comment since post in timeline are not strictly decreasing - when there are pinned posts
                # if date_to_search_for > current_post_date:
                #     logger.info("Found post with date {}, which is after {}, the date we were searching for. Exiting..".format(current_post_date,
                #                                                                            date_to_search_for))
                #     should_get_next_page = False
                #     break

            logger.info("\nProcessing post {} from {} with description: {}".format(current_post.pk, current_post_date.isoformat(), current_post.caption_text))

            if str(current_post.pk) in exclusion_list and not date_to_search_for:
                logger.info("Found post {} in exclusion list, moving on to next post.".format(current_post.pk))
                continue

            user_in = input("Enter a nickname for this post and an optional new date, separated by a comma [ex: lisbon,2025-01-01], or type s(kip) or e(xit)\n")
            if user_in.lower() in ("e", "exit"):
                logger.info("Exiting...")
                should_get_next_page = False
                break
            if user_in.lower() in ("s", "skip"):
                logger.info("Moving on to next post, excluding this one...")
                # If we made it this far successfully, let's prevent ourselves from processing this post again
                add_to_exclusion_file(current_post.pk)
                continue

            split_user_in = user_in.split(",")
            post_slug = split_user_in[0]
            if len(split_user_in) > 1:
                date_for_blog = datetime.strptime(split_user_in[1], '%Y-%m-%d')
            else:
                date_for_blog = current_post_date

            img_directory_path = os.path.join(img_root_dir, str(date_for_blog.year), "{}-{}".format(date_for_blog.month, post_slug))
            logger.info("Putting photos in directory {}".format(img_directory_path))

            if os.path.exists(img_directory_path):
                if len(os.listdir(img_directory_path)) > 0:
                    logger.warning("Path {} already exists and has files, you must delete the files if you want to redownload them...".format(img_directory_path))
                    file_exists_input = input("Type s(kip) to skip downloading, or type anything to continue...\n")
                    if file_exists_input.lower() in ("s", "skip"):
                        logger.info("Moving on to next post...")
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
                logger.warning("Unexpected media type found while processing post, not a photo or album: {}".format(current_post.id))
                continue
            if hasattr(downloaded_path, "__len__") and len(downloaded_path) > 1:
                downloaded_file_list = downloaded_path
            else:
                downloaded_file_list.append(downloaded_path)

            enumerated_file_names = rename_photos_in_dir(img_directory_path, downloaded_file_list)
            if current_post.media_type != 2:
                cover_photo_name = make_cover_photo(img_directory_path)
            else:
                logger.warning("Not making a cover photo, unsupported media {}".format(downloaded_path))
                cover_photo_name = None

            blog_post_name = "{}-{}.md".format(date_for_blog.strftime("%Y-%m-%d"), post_slug)
            blog_post_path = os.path.join(blog_root_dir, blog_post_name)
            if os.path.isfile(blog_post_path):
                logger.warning("Path {} already exists, you must delete it or move it to recreate it...".format(blog_post_path))
                file_exists_input = input("Type s(kip) to skip creating it, or type anything to continue...\n")
                if file_exists_input.lower() in ("s", "skip"):
                    logger.info("Moving on to next post...")
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
            logger.info("Created blog post draft at {}".format(blog_post_path))

            # If we made it this far successfully, let's prevent ourselves from processing this post again
            add_to_exclusion_file(current_post.pk)

            if date_to_search_for:
                # processed date to search for, break
                logger.info("Finished requested date")
                break

        if media_found_count >= total_media_count:
            logger.info("Reached last post in the feed.")


def environ_or_required(key):
    return (
        {'default': os.environ.get(key)} if os.environ.get(key)
        else {'required': True} if not os.path.exists(insta_session_file) else {}
    )

def valid_date(s: str) -> datetime:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a valid date: {s!r}")

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument("-u", "--username", default="goelrohan", help="Instagram Username")
    PARSER.add_argument("-p", "--password", **environ_or_required("INSTA_PASSWORD"), help="Instagram Password")
    PARSER.add_argument("-c", "--verification_code", help="Instagram verification code")
    PARSER.add_argument("-d", "--date", type=valid_date, help="Download the post or posts from a single day, based on the date posted to Instagram. Overrides exclude list. format: YYYY-MM-DD")
    PARSER.add_argument("-t", "--timeout", type=int, default=1, help="Sets the default request timeout for interacting with the Instagram API")

    MYARGS = PARSER.parse_args()
    main(MYARGS)