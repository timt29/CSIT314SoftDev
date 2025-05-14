from Booking import Booking 

class SearchBookingController:

    def get_services_by_cleaner(cleaner_id):
        return Booking.get_services_by_cleaner(cleaner_id)