from src.web import create_app
from pathlib import Path
import os

static_folder = os.path.join(Path(__file__).parent.resolve(), "public")
app = create_app(env="development", static_folder=static_folder)


def main():
    app.run()


if __name__ == "__main__":
    main()
