async def logger_service(message):

    print("=" * 60)

    # print(message.chat.name)

    # print(message.sender.name)

    print(message.message.text)

    print("=" * 60)