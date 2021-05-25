from psycopg2 import connect
import yaml


class Connection():
    with open("settings.yml", "r") as f:
        settings = yaml.safe_load(f)
    conn = connect(**settings["postgres"])
