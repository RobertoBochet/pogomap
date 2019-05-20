#!/usr/bin/env python3
import logging

from pogomap import PogoMap
from pogomap.PogoMap import GET_ENTITIES

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    pogomap = PogoMap(
        db_host="172.18.0.2:5432",
        db_user="postgres",
        db_pass="NjNXFh2XVJgsBY36",
        db_name="pogomap"
    )

    print(pogomap.is_editor_key_valid("0w15oLAp46PS2Gv69lHSWlkzbk1o83Tg"))
    print(pogomap.is_editor_key_valid("0w15oLAp46PS2Gv69lHSWlkzbk1o83Th"))

    for i in GET_ENTITIES:
        list(pogomap.get_entities(i))
