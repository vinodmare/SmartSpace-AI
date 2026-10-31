from fastapi import APIRouter

from app.api.v1.endpoints import (
    admin,
    ai,
    analytics,
    amenities,
    auth,
    availability,
    bookings,
    favorites,
    notifications,
    owners,
    payments,
    reviews,
    search,
    spaces,
    uploads,
    users,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(owners.router, prefix="/owners", tags=["Owners"])
api_router.include_router(spaces.router, prefix="/spaces", tags=["Spaces"])
api_router.include_router(amenities.router, prefix="/amenities", tags=["Amenities"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(availability.router, prefix="/availability", tags=["Calendar Availability"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Placeholders"])

