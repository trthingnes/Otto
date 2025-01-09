def section(text: str):
    return {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": text,
            "emoji": True,
        },
    }


def text_input(text: str, value: str):
    return {
        "type": "input",
        "dispatch_action": False,
        "element": {
            "type": "plain_text_input",
            "action_id": value,
        },
        "label": {"type": "plain_text", "text": text, "emoji": True},
    }


def select_input(text: str, value: str, options: list[str], initial_option: str = None):
    dict = {
        "type": "input",
        "dispatch_action": False,
        "element": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select an option",
                "emoji": True,
            },
            "options": [
                {
                    "text": {"type": "plain_text", "text": option, "emoji": True},
                    "value": option,
                }
                for option in options
            ],
            "action_id": value,
        },
        "label": {"type": "plain_text", "text": text, "emoji": True},
    }

    if initial_option is not None:
        dict["element"]["initial_option"] = {
            "text": {
                "type": "plain_text",
                "text": initial_option if initial_option else options[0],
                "emoji": True,
            },
            "value": initial_option if initial_option else options[0],
        }

    return dict


def actions(elements: list[dict[str, any]]):
    return {"type": "actions", "elements": elements}


def button(text: str, value: str) -> dict:
    return {
        "type": "button",
        "text": {"type": "plain_text", "text": text, "emoji": True},
        "value": value,
        "action_id": value,
    }
