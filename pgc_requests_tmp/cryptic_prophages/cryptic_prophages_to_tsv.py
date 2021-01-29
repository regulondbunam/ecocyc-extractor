import pythoncyc


def get_transcription_direction(transcription_direction):
    if transcription_direction is None:
        return "undetermined"
    else:
        if transcription_direction == "+":
            return "forward"
        elif transcription_direction == "-":
            return "reverse"

pt_conn = pythoncyc.select_organism("ecoli")

cryptic_prophages_ids = pt_conn.get_class_all_instances("|Cryptic-Prophages|")

cryptic_prophages_objects = pt_conn.get_frame_objects(cryptic_prophages_ids)

with open("cryptic_prophages.tsv", 'w') as cp_fp:
    cp_fp.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
        "ECOCYC_ID",
        "COMMON_NAME",
        "LEFT_END_POS",
        "RIGHT_END_POS",
        "TRANSCRIPTION_DIRECTION",
        "CITATIONS"
    ))
    for cryptic_prophage in cryptic_prophages_objects:
        cp_fp.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
            cryptic_prophage["frameid"],
            cryptic_prophage["common_name"],
            cryptic_prophage["left_end_position"],
            cryptic_prophage["right_end_position"],
            get_transcription_direction(cryptic_prophage["transcription_direction"]),
            ", ".join(cryptic_prophage["citations"])
        ))

