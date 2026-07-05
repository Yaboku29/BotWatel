from deep_translator import GoogleTranslator


async def process_TL(message):

    original = message.message.text

    if not original:
        return

    # print("=== Translator ===")
    # print(original)

    translated = GoogleTranslator(
        source="auto",
        target="en"
    ).translate(original)

    # print(translated)

    message.message.text = (
        f"Original\n\n"
        f"{original}\n\n"
        f"--------------------\n\n"
        f"English\n\n"
        f"{translated}"
    )