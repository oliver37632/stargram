from src.__init__ import create_app
from src.config import authjwt_secret_key, ALGORITHM

if __name__ == "__main__":
    app = create_app()
    app.config['SECRET_KEY'] = authjwt_secret_key
    app.config["JWT_DECODE_ALGORITHMS"] = ALGORITHM


    app.run(host="0.0.0.0", debug=True, port=8000)