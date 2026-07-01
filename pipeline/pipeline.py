class MessagePipeline:

    def __init__(self):

        self.handlers = []

    def register(self, handler):

        self.handlers.append(handler)

    async def process(self, message):

        for handler in self.handlers:

            await handler(message)