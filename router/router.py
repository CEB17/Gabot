# Import controller file
from controllers import controllers
# Router endpoint
def router(app, parser, line_bot_api):
    @app.route("/", methods=['GET'])
    def index():
        return controllers.index()

    @app.route("/", methods=['POST'])
    def callback():
        return controllers.handler(app,parser,line_bot_api)


