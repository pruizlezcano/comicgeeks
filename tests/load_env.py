from pathlib import Path

from dotenv import dotenv_values

from comicgeeks import Comic_Geeks


def load_env():
    dotenv_path = Path(".devdata.env")
    env = dotenv_values(dotenv_path=dotenv_path)
    if "LCG_USERNAME" not in env:
        import os

        env = {
            "LCG_USERNAME": os.environ.get("LCG_USERNAME"),
            "LCG_PASSWORD": os.environ.get("LCG_PASSWORD"),
        }
    temp = Comic_Geeks()
    temp.login(env["LCG_USERNAME"], env["LCG_PASSWORD"])
    env["LCG_CI_SESSION"] = temp._session.cookies.get("ci_session")
    return env
