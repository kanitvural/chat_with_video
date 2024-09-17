import os

import scrapetube
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser

from models.youtube_video import YoutubeVideo

load_dotenv()


# Transcryption


def get_video_transcrypt(url):

    target_dir = "./audios/"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir), OpenAIWhisperParser()
    )

    video_transcrypt_docs = loader.load()

    return video_transcrypt_docs


# Youtube search


def get_videos_for_search_term(
    search_term, video_count=1, sorting_criteria="relevance"
):

    convert_sorting_option = {
       "Relevance":"relevance",
       "Date":"upload_date",
        "Views":"view_count",
        "Likes":"rating",
    }

    videos = scrapetube.get_search(
        query=search_term,
        limit=video_count,
        sort_by=convert_sorting_option[sorting_criteria],
    )
    videolist = list(videos)

    youtube_videos = []

    for video in videolist:
        youtube_video = YoutubeVideo(
            video_id=video["videoId"],
            video_title=video["title"]["runs"][0]["text"],
            video_url="https://www.youtube.com/watch?v=" + video["videoId"],
            channel_name=video["longBylineText"]["runs"][0]["text"],
            duration=video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date=video["publishedTimeText"]["simpleText"],
        )

        youtube_videos.append(youtube_video)

    return youtube_videos
