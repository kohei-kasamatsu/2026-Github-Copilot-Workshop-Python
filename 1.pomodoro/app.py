from flask import Flask, render_template

from config import AppConfig
from services.pomodoro_service import get_initial_settings


def create_app() -> Flask:
	app = Flask(__name__)
	app.config.from_object(AppConfig)

	@app.route("/")
	def index() -> str:
		return render_template(
			"index.html",
			page_title=app.config["APP_TITLE"],
			initial_settings=get_initial_settings(app.config),
		)

	return app


app = create_app()


if __name__ == "__main__":
	app.run(debug=True)
