from flask import request, render_template, redirect, session, jsonify
from FavouriteController import FavouriteController
from ViewCleanerServicesController import ViewCleanerServicesController
from ViewShortlistController import ViewShortlistController

def register_routes4(app):

    @app.route('/fav')
    def favourites_page():
        user = FavouriteController.validate_user_session(session)
        if not user:
            return redirect('/')

        user_id = user.get("UserId")
        homeowner_name = ViewCleanerServicesController.get_homeowner_name(user_id)["name"]
        if not homeowner_name:
            return "homeowner not found", 404

        favourites = FavouriteController.fetch_favourites(user_id)

        return render_template(
            'HOfav.html',
            favourites=favourites,
            homeowner_name=homeowner_name
        )
    
    @app.route('/api/favourite', methods=['POST'])
    def favourite_service():
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        data = request.get_json()
        cleaner_id = data.get('cleaner_id')
        service_id = data.get('service_id')
        homeowner_id = user.get("UserId")

        # Basic check
        if not (homeowner_id and cleaner_id and service_id):
            return jsonify({'error': 'Missing required info'}), 400

        success, error = ViewShortlistController.add_to_favourites(homeowner_id, cleaner_id, service_id)

        if success:
            ViewShortlistController.increaseShortlistCount(cleaner_id, service_id)
            return jsonify({'message': 'Service added to shortlist!'}), 200
        else:
            return jsonify({'error': error or 'Something went wrong'}), 400
        
