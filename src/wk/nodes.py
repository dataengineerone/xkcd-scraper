from typing import Dict, Any


def generate_comic_urls(from_comics, to_comics):
    comic_ids = range(from_comics, to_comics + 1)

    comic_urls = {}

    for comic_id in comic_ids:
        comic_urls[f"{comic_id:04}"] = f"https://xkcd.com/{comic_id}/"

    return comic_urls


def _get_url(url):
    import requests
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to download url {url}.")
    return resp


def download_url_html(comic_urls: Dict[str, str]) -> Dict[str, str]:
    html_data = {}

    for comic_id, comic_url in comic_urls.items():
        html_data[comic_id] = _get_url(comic_url).text
    return html_data


def extract_image_metadata(comic_html: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    import re

    image_metadata = {}

    for comic_id, html in comic_html.items():
        matches = re.findall('<img src="(.*?)" title="(.*?)"', html)
        if len(matches) <= 0:
            raise Exception(f"No image match found for {comic_id}")
        image_url, image_title = matches[0]
        image_metadata[comic_id] = {'url': f"http:{image_url}", 'title': image_title}

    return image_metadata


def download_image(image_metadata: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
    image_data = {}
    for comic_id, image_meta in image_metadata.items():
        image_data[comic_id] = _get_url(image_meta['url']).content
    return image_data


def save_images_by_title(image_metadata: Dict[str, Dict[str, str]],
                         image_data: Dict[str, Any]):
    images_by_title = {}
    for comic_id, image_meta in image_metadata.items():
        images_by_title[image_meta['title'].replace("/", "_")] = image_data[comic_id]
    return images_by_title
