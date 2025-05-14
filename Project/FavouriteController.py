from Favourite import Favourite

class FavouriteController:
    def fetch_favourites(homeowner_id):
       return Favourite.get_favourite_cleaners(homeowner_id)
    
    def validate_user_session(session):
      return session.get("user")