from controllers import controllers

def router(app, parser, line_bot_api):
    @app.route("/", methods=['GET'])
    def index():
        return controllers.index()

    @app.route("/callback", methods=['POST'])
    def callback():
        return controllers.handler(app,parser,line_bot_api)


