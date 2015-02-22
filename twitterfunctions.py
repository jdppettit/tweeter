import twython
import config

def make_api():
    api = twython.Twython(app_key=config.app_key,
                    app_secret=config.app_secret,
                    oauth_token=config.oauth_token,
                    oauth_token_secret=config.oauth_token_secret)
    return api

def make_tweet(message):
    api = make_api()
    api.update_status(status=message)
