from classes.Database import get_session
from classes.models import User

def get_user_by_username(username: str) -> User | None:
    """
    Retrieves a user from the database by their username.

    Args:
        username: The username of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        return user
    except Exception as e:
        print(f"Error querying user by username: {e}")
        return None
    finally:
        session.close()
