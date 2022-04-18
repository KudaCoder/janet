from flask_assets import Environment, Bundle

assets = Environment()


def init_app(app):
    assets.init_app(app)


janet_js = Bundle(
    "js/styles.js",
    "js/pages/config.js",
)
js = Bundle(janet_js, output="main.min.js")

janet_css = Bundle(
    "css/styles.css",
    "css/pages/config.css",
    "css/pages/readings.css",
    "css/modules/login-register.css",
    "css/modules/habi-nav.css",
    "css/modules/nav-bar.css",
)
css = Bundle(janet_css, output="main.min.css")


assets.register("js", js)
assets.register("css", css)
