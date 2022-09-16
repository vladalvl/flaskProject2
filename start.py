from settings import app


if __name__ == '__main__':

    from views.post_with_orm import post
    app.register_blueprint(post)

    app.run()
