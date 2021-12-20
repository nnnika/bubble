from flask import Flask

app=Flask(
			__name__,
			template_folder='api_server',
			static_folder='xxx',
			static_url_path='/xxx'
		)