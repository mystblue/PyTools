from pixivpy3 import AppPixivAPI

def login():
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)
    return api

def main():
    apilogin  = login()

if __name__ == '__main__':
	main()