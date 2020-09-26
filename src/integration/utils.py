import pytest, threading, logging, json

from telegram import Update

from modules.pytg.load import manager, get_module_content_folder
from modules.pytg.init import boot, initialize, launch
from modules.pytg.development import add_reroute_rule, register_mock_manager

def setup_environment():
    boot(dev_mode = True)

    add_reroute_rule("bot", "mockbot")
    add_reroute_rule("config", "mock_config")

    # add_reroute_rule("data", "mock_data")
    # add_reroute_rule("sqlite3", "mock_sqlite3")

    initialize()

    manager("mock_config").add_mock_settings({
        "loaders": ["yaml", "json"],
        "default_loader": "yaml"
    }, "resources")

    manager("mock_config").add_mock_settings({
        "default": "en"
    }, "text", "lang")

    manager("mock_config").add_mock_settings({
        "pragma": {}
    }, "sqlite3")

    manager("mock_config").add_mock_settings({
        "reaction_extra_points": {
            'UP': 4,
            'DOWN': 1,
        }
    }, "dummy", "reactions")

    launch(main_module="mockbot")

    # Uncomment if 'data' module has to be used for tests
    # manager("data").save_data("dummy", "user_reactions", "__default", {"reacted_messages": {}})

    # Uncomment if 'sqlite3' module has to be used for tests
    # session = manager("sqlite3").create_session("dummy", "reactions", "test")

    # session.lock()
    # session.execute_script(open("{}/sqlite3/init_db.sql".format(get_module_content_folder("dummy")), "r").read())
    # session.unlock()
    
def teardown_environment():
    manager("mockbot").join()
    manager("mockbot").stop()

    # manager("sqlite3").clear_session("dummy", "reactions", "test")

def load_test_json(path, name):
    return manager("resources").load_resource("dummy_tests", name, path=path, loader="json")

def load_test_yaml(path, name):
    return manager("resources").load_resource("dummy_tests", name, path=path, loader="yaml")

def load_test_update(path, name):
    return Update.de_json(load_test_json(path, name), manager("mockbot").bot)