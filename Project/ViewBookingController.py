from Booking import Booking 

class ViewBookingController:

    def getBooking(cleaner_id, filters):
        return Booking.get_confirmed_bookings_for_cleaner(
            cleaner_id,
            filters.get("service_id"),
            filters.get("date_used")
        )
    
    def parse_filters(request):
        return {
            "service_id": request.args.get("service_filter"),
            "date_used": request.args.get("date_used")
        }
    
    def createBooking(home_owner_id, cleaner_id, service_id):
        return Booking.create_booking(home_owner_id, cleaner_id, service_id)
