# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Construction of the master pipeline.
"""

from typing import Dict
from kedro.pipeline import Pipeline, node

from .nodes import generate_comic_urls, download_url_html, extract_image_metadata, download_image, save_images_by_title


def create_pipelines(**kwargs) -> Dict[str, Pipeline]:
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """

    download_html = Pipeline([
        node(generate_comic_urls, inputs=["params:start_id", "params:end_id"], outputs="comic_urls"),
        node(download_url_html, inputs="comic_urls", outputs="comic_html", confirms="comic_urls"),
    ])

    process_data = Pipeline([
        node(extract_image_metadata, inputs="comic_html", outputs="image_metadata"),
    ])

    download_images = Pipeline([
        node(download_image, inputs="image_metadata", outputs="images"),
    ])

    group_images = Pipeline([
        node(save_images_by_title, inputs=["image_metadata", "images"], outputs="images_by_title", confirms="image_metadata")
    ])

    return {
        "download_html": download_html,
        "process_data": process_data,
        "download_images": download_images,
        "group_images": group_images,
        "__default__": download_html + process_data + download_images + group_images
    }
