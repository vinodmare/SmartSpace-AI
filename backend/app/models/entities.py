import enum
from datetime import date, datetime, time
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import INET, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UserRole(str, enum.Enum):
    customer = "customer"
    owner = "owner"
    admin = "admin"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    deleted = "deleted"


class VerificationStatus(str, enum.Enum):
    pending = "pending"
    in_review = "in_review"
    approved = "approved"
    rejected = "rejected"


class SpaceStatus(str, enum.Enum):
    draft = "draft"
    pending_approval = "pending_approval"
    approved = "approved"
    rejected = "rejected"
    suspended = "suspended"
    archived = "archived"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    rejected = "rejected"
    refunded = "refunded"


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    authorized = "authorized"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"
    partially_refunded = "partially_refunded"


class NotificationStatus(str, enum.Enum):
    unread = "unread"
    read = "read"
    archived = "archived"


class AiJobStatus(str, enum.Enum):
    queued = "queued"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class MediaType(str, enum.Enum):
    image = "image"
    video = "video"
    document = "document"


class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)


class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class User(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    full_name: Mapped[str | None] = mapped_column(String(160))
    phone: Mapped[str | None] = mapped_column(String(32))
    avatar_url: Mapped[str | None] = mapped_column(Text)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.active)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    phone_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    roles: Mapped[list["UserRoleLink"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    customer_profile: Mapped["CustomerProfile | None"] = relationship(back_populates="user")
    owner_profile: Mapped["OwnerProfile | None"] = relationship(back_populates="user")
    admin_profile: Mapped["AdminProfile | None"] = relationship(back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[UserRole] = mapped_column(Enum(UserRole), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    users: Mapped[list["UserRoleLink"]] = relationship(back_populates="role")


class UserRoleLink(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="roles")
    role: Mapped[Role] = relationship(back_populates="users")


class CustomerProfile(Base, AuditMixin):
    __tablename__ = "customer_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    preferred_city: Mapped[str | None] = mapped_column(String(120))
    preferred_space_type: Mapped[str | None] = mapped_column(String(80))
    accessibility_needs: Mapped[str | None] = mapped_column(Text)

    user: Mapped[User] = relationship(back_populates="customer_profile")


class OwnerProfile(Base, AuditMixin):
    __tablename__ = "owner_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    business_name: Mapped[str | None] = mapped_column(String(180))
    gst_number: Mapped[str | None] = mapped_column(String(32))
    pan_number: Mapped[str | None] = mapped_column(String(16))
    payout_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.pending
    )

    user: Mapped[User] = relationship(back_populates="owner_profile")
    spaces: Mapped[list["Space"]] = relationship(back_populates="owner")


class AdminProfile(Base, AuditMixin):
    __tablename__ = "admin_profiles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    department: Mapped[str | None] = mapped_column(String(120))
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship(back_populates="admin_profile")


class OwnerVerificationRequest(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "owner_verification_requests"

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("owner_profiles.user_id"), index=True)
    status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus), default=VerificationStatus.pending)
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    notes: Mapped[str | None] = mapped_column(Text)
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Address(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "addresses"

    line1: Mapped[str] = mapped_column(String(255))
    line2: Mapped[str | None] = mapped_column(String(255))
    locality: Mapped[str] = mapped_column(String(140), index=True)
    city: Mapped[str] = mapped_column(String(120), index=True)
    state: Mapped[str] = mapped_column(String(120))
    postal_code: Mapped[str | None] = mapped_column(String(16))
    country_code: Mapped[str] = mapped_column(String(2), default="IN")
    latitude: Mapped[float | None] = mapped_column(Numeric(10, 7))
    longitude: Mapped[float | None] = mapped_column(Numeric(10, 7))


class SpaceCategory(Base, AuditMixin):
    __tablename__ = "space_categories"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    spaces: Mapped[list["Space"]] = relationship(back_populates="category")


class Space(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "spaces"
    __table_args__ = (
        CheckConstraint("capacity > 0", name="spaces_capacity_check"),
        CheckConstraint("hourly_price_inr >= 0", name="spaces_hourly_price_check"),
        CheckConstraint("rating_average >= 0 AND rating_average <= 5", name="spaces_rating_average_check"),
        CheckConstraint("demand_score >= 0 AND demand_score <= 100", name="spaces_demand_score_check"),
        Index("idx_spaces_owner_status", "owner_id", "status"),
        Index("idx_spaces_category_status", "category_id", "status"),
    )

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("owner_profiles.user_id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("space_categories.id"))
    address_id: Mapped[UUID] = mapped_column(ForeignKey("addresses.id"))
    name: Mapped[str] = mapped_column(String(180))
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    capacity: Mapped[int] = mapped_column(Integer)
    size_sqft: Mapped[int | None] = mapped_column(Integer)
    hourly_price_inr: Mapped[int] = mapped_column(Integer)
    daily_price_inr: Mapped[int | None] = mapped_column(Integer)
    minimum_booking_hours: Mapped[float] = mapped_column(Numeric(4, 2), default=1)
    rating_average: Mapped[float] = mapped_column(Numeric(3, 2), default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    demand_score: Mapped[int] = mapped_column(SmallInteger, default=0)
    status: Mapped[SpaceStatus] = mapped_column(Enum(SpaceStatus), default=SpaceStatus.draft)
    approved_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(Text)

    owner: Mapped[OwnerProfile] = relationship(back_populates="spaces")
    category: Mapped[SpaceCategory] = relationship(back_populates="spaces")
    address: Mapped[Address] = relationship()
    media: Mapped[list["SpaceMedia"]] = relationship(back_populates="space", cascade="all, delete-orphan")
    amenities: Mapped[list["SpaceAmenity"]] = relationship(back_populates="space", cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="space")


class Amenity(Base, AuditMixin):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True)


class SpaceAmenity(Base):
    __tablename__ = "space_amenities"

    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), primary_key=True)
    amenity_id: Mapped[int] = mapped_column(ForeignKey("amenities.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    space: Mapped[Space] = relationship(back_populates="amenities")
    amenity: Mapped[Amenity] = relationship()


class SpaceMedia(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "space_media"

    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), index=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), default=MediaType.image)
    url: Mapped[str] = mapped_column(Text)
    alt_text: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    image_quality_score: Mapped[int | None] = mapped_column(SmallInteger)

    space: Mapped[Space] = relationship(back_populates="media")


class SpaceAvailabilityRule(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "space_availability_rules"
    __table_args__ = (
        CheckConstraint("day_of_week >= 0 AND day_of_week <= 6", name="day_of_week_check"),
        CheckConstraint("opens_at < closes_at", name="opens_before_closes_check"),
        UniqueConstraint("space_id", "day_of_week", "opens_at", "closes_at"),
    )

    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), index=True)
    day_of_week: Mapped[int] = mapped_column(SmallInteger)
    opens_at: Mapped[time] = mapped_column(Time)
    closes_at: Mapped[time] = mapped_column(Time)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)


class SpaceBlackoutDate(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "space_blackout_dates"
    __table_args__ = (CheckConstraint("starts_at < ends_at", name="blackout_period_check"),)

    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str | None] = mapped_column(Text)


class Favorite(Base):
    __tablename__ = "favorites"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Booking(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("starts_at < ends_at", name="booking_period_check"),
        CheckConstraint("guest_count > 0", name="booking_guest_count_check"),
        Index("idx_bookings_customer_starts", "customer_id", "starts_at"),
        Index("idx_bookings_owner_starts", "owner_id", "starts_at"),
        Index("idx_bookings_space_period", "space_id", "starts_at", "ends_at"),
    )

    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customer_profiles.user_id"))
    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("owner_profiles.user_id"))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    guest_count: Mapped[int] = mapped_column(Integer)
    hourly_price_inr: Mapped[int] = mapped_column(Integer)
    subtotal_inr: Mapped[int] = mapped_column(Integer)
    tax_inr: Mapped[int] = mapped_column(Integer, default=0)
    platform_fee_inr: Mapped[int] = mapped_column(Integer, default=0)
    total_inr: Mapped[int] = mapped_column(Integer)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.pending)
    cancellation_reason: Mapped[str | None] = mapped_column(Text)
    cancelled_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    space: Mapped[Space] = relationship(back_populates="bookings")


class Payment(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "payments"

    booking_id: Mapped[UUID] = mapped_column(ForeignKey("bookings.id"), index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[str] = mapped_column(String(40))
    provider_payment_id: Mapped[str | None] = mapped_column(String(180))
    provider_order_id: Mapped[str | None] = mapped_column(String(180))
    amount_inr: Mapped[int] = mapped_column(Integer)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.pending)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    failed_reason: Mapped[str | None] = mapped_column(Text)


class Refund(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "refunds"

    payment_id: Mapped[UUID] = mapped_column(ForeignKey("payments.id"), index=True)
    amount_inr: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str | None] = mapped_column(Text)
    provider_refund_id: Mapped[str | None] = mapped_column(String(180))
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.pending)


class Review(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("rating >= 1 AND rating <= 5", name="reviews_rating_check"),)

    booking_id: Mapped[UUID] = mapped_column(ForeignKey("bookings.id"), unique=True)
    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), index=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customer_profiles.user_id"))
    rating: Mapped[int] = mapped_column(SmallInteger)
    review_text: Mapped[str | None] = mapped_column(Text)
    cleanliness_rating: Mapped[int | None] = mapped_column(SmallInteger)
    location_rating: Mapped[int | None] = mapped_column(SmallInteger)
    value_rating: Mapped[int | None] = mapped_column(SmallInteger)
    staff_rating: Mapped[int | None] = mapped_column(SmallInteger)
    sentiment_label: Mapped[str | None] = mapped_column(String(24))
    sentiment_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    owner_reply: Mapped[str | None] = mapped_column(Text)
    owner_replied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Notification(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "notifications"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    body: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(80))
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus), default=NotificationStatus.unread
    )
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class SearchEvent(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "search_events"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    query: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(120))
    capacity: Mapped[int | None] = mapped_column(Integer)
    budget_inr: Mapped[int | None] = mapped_column(Integer)
    ai_search: Mapped[bool] = mapped_column(Boolean, default=False)
    result_count: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UserSpaceEvent(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "user_space_events"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"))
    event_type: Mapped[str] = mapped_column(String(40))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ContactMessage(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "contact_messages"

    name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(180))
    message: Mapped[str] = mapped_column(Text)
    handled_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    handled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditLog(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    entity_type: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    action: Mapped[str] = mapped_column(String(80))
    before_data: Mapped[dict | None] = mapped_column(JSONB)
    after_data: Mapped[dict | None] = mapped_column(JSONB)
    ip_address: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FraudRiskAssessment(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "fraud_risk_assessments"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    booking_id: Mapped[UUID | None] = mapped_column(ForeignKey("bookings.id"))
    risk_score: Mapped[int] = mapped_column(SmallInteger)
    risk_level: Mapped[str] = mapped_column(String(16))
    signals: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(32), default="open")
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AiJob(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "ai_jobs"

    service_name: Mapped[str] = mapped_column(String(80), index=True)
    entity_type: Mapped[str | None] = mapped_column(String(80))
    entity_id: Mapped[UUID | None] = mapped_column(PG_UUID(as_uuid=True))
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_payload: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[AiJobStatus] = mapped_column(Enum(AiJobStatus), default=AiJobStatus.queued)
    error_message: Mapped[str | None] = mapped_column(Text)


class PriceSuggestion(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "price_suggestions"

    space_id: Mapped[UUID] = mapped_column(ForeignKey("spaces.id"), index=True)
    suggested_hourly_price_inr: Mapped[int] = mapped_column(Integer)
    lower_bound_inr: Mapped[int | None] = mapped_column(Integer)
    upper_bound_inr: Mapped[int | None] = mapped_column(Integer)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    explanation: Mapped[dict] = mapped_column(JSONB, default=dict)
    ai_job_id: Mapped[UUID | None] = mapped_column(ForeignKey("ai_jobs.id"))


class DemandForecast(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "demand_forecasts"

    space_id: Mapped[UUID | None] = mapped_column(ForeignKey("spaces.id"))
    city: Mapped[str | None] = mapped_column(String(120))
    forecast_date: Mapped[date] = mapped_column(Date)
    predicted_bookings: Mapped[float] = mapped_column(Numeric(10, 2))
    predicted_revenue_inr: Mapped[int | None] = mapped_column(Integer)
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 4))
    ai_job_id: Mapped[UUID | None] = mapped_column(ForeignKey("ai_jobs.id"))


class Report(Base, UUIDPrimaryKeyMixin, AuditMixin):
    __tablename__ = "reports"

    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    report_type: Mapped[str] = mapped_column(String(80))
    filters: Mapped[dict] = mapped_column(JSONB, default=dict)
    file_url: Mapped[str | None] = mapped_column(Text)
