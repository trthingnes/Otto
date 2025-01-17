import io

from slack_bolt import Args

from otto.app import app
from otto.features.coverimage.generator import CoverImageFormat, create_cover_image
from otto.image import retrieve_image
from otto.utils.actions import transform_action_state_values
from otto.utils.esn import EsnColor


@app.action("generate_coverimage")
def coverimage(args: Args):
    args.ack()

    channel_id = args.body["container"]["channel_id"]
    thread_ts = args.body["container"]["thread_ts"]
    image = retrieve_image(thread_ts)
    state = transform_action_state_values(args.body["state"]["values"])

    if image:
        coverimage = create_cover_image(
            title=state["title"],
            subtitle=state["subtitle"],
            subsubtitle=state["subsubtitle"],
            color=EsnColor.from_display_name(state["color"]),
            format=CoverImageFormat.from_value(state["format"]),
            background=image,
        )
    else:
        coverimage = create_cover_image(
            title=state["title"],
            subtitle=state["subtitle"],
            subsubtitle=state["subsubtitle"],
            color=EsnColor.from_display_name(state["color"]),
            format=CoverImageFormat.from_value(state["format"]),
        )

    image_content = io.BytesIO()
    coverimage.save(image_content, format="JPEG")

    args.client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        text="Your cover image is on its way over! Remember: You can change a couple of settings above and generate again if something is off.",
    )

    args.client.files_upload_v2(
        channel=channel_id,
        thread_ts=thread_ts,
        content=image_content.getvalue(),
        filename="coverimage.png"
    )
