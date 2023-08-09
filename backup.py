import json

import jsonpickle
import streamlit as st

from common import Conversation
from encryption import decrypt_prop, encrypt_prop, generate_key, DEFAULT_KEY

BACKUP_PROPS = ["vector_stores", "databases", "current_conversation"]


def backup_settings(password: str) -> dict:
    backup = dict()

    backup['use_default_key'] = not password
    enc_key = generate_key(password) if password else DEFAULT_KEY

    for prop in BACKUP_PROPS:
        value = st.session_state[prop]

        if isinstance(value, dict):
            value = {k: json.loads(jsonpickle.encode(encrypt_prop(v, enc_key))) for k, v in value.items()}

        backup[prop] = value

    return backup


def load_settings(backup: dict, password: str):
    enc_key = generate_key(password) if password else DEFAULT_KEY

    for prop in BACKUP_PROPS:
        if prop in backup:
            value = backup[prop]

            if isinstance(value, dict):
                value = {k: decrypt_prop(jsonpickle.decode(json.dumps(v)), enc_key) for k, v in value.items()}

            st.session_state[prop] = value


def backup_conversation(id: str) -> dict:
    if id not in st.session_state.conversations:
        return None

    return json.loads(jsonpickle.encode(st.session_state.conversations[id]))


def load_conversation(backup: dict) -> Conversation:
    # As this will create a new object, the timestamp will be updated
    return jsonpickle.decode(json.dumps(backup))
