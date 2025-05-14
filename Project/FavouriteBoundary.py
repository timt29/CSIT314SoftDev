from flask import request, render_template, redirect, session
from FavouriteController import FavouriteController
from ViewServicesController import ViewServicesController


def register_routes4(app):

    @app.route('/fav')
    def favourites_page():
        user = FavouriteController.validate_user_session(session)
        if not user:
            return redirect('/')

        user_id = user.get("UserId")
        homeowner_name = ViewServicesController.get_homeowner_name(user_id)["name"]
        if not homeowner_name:
            return "homeowner not found", 404

        favourites = FavouriteController.fetch_favourites(user_id)

        return render_template(
            'HOfav.html',
            favourites=favourites,
            homeowner_name=homeowner_name
        )
    
