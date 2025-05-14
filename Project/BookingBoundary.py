from flask import request, render_template, redirect, url_for, session, jsonify
from ViewBookingController import ViewBookingController
from SearchBookingController import SearchBookingController

def register_routes6(app):

    @app.route("/booking")
    def confirmed_bookings_page():
        user = session.get("user")
        if not user:
            return redirect('/')

        cleaner_id = user.get("UserId")
        cleaner_name = user.get("Name")  # Adjust if stored differently

        filters = ViewBookingController.parse_filters(request)
        bookings = ViewBookingController.getBooking(cleaner_id, filters)
        services = SearchBookingController.get_services_by_cleaner(cleaner_id)

        return render_template(
            "confirmbooking.html",
            bookings=bookings,
            services=services,
            selected_service=filters.get("service_id"),
            date_used=filters.get("date_used"),
            cleaner_name=cleaner_name
        )
    
    @app.route("/api/book", methods=["POST"])
    def api_book_service():
        user = session.get("user")
        if not user:
            return jsonify({"error": "Not logged in"}), 401

        home_owner_id = user.get("UserId")
        cleaner_id = request.json.get("cleaner_id")
        service_id = request.json.get("service_id")


        is_successful = ViewBookingController.createBooking(home_owner_id, cleaner_id, service_id)
        # Handle the response
        if is_successful:
            return jsonify({"message": "Booking successful!"}), 200
        else:
            return jsonify({"error": "Failed to book service"}), 500