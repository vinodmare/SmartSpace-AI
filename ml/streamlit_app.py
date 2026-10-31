from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

import joblib
import pandas as pd
import streamlit as st

from model_loader import price_input_to_frame
from streamlit_train import MODEL_DIR, REPORT_DIR

st.set_page_config(page_title="SmartSpace AI ML Studio", page_icon="SS", layout="wide")

model_path = MODEL_DIR / "model.pkl"
metadata_path = MODEL_DIR / "training_metadata.pkl"
owner_listing_path = REPORT_DIR / "owner_space_listings.csv"
owner_image_dir = REPORT_DIR / "owner_images"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
owner_image_dir.mkdir(parents=True, exist_ok=True)

st.markdown(
    """
    <style>
    :root {
      --ink: #0b1220;
      --soft-ink: #334155;
      --muted: #64748b;
      --line: rgba(15, 23, 42, .10);
      --panel: rgba(255, 255, 255, .86);
      --brand: #0369a1;
      --brand-2: #0f766e;
      --accent: #f59e0b;
    }
    .stApp {
      background:
        linear-gradient(180deg, #f8fbff 0%, #f8fafc 45%, #eef7f6 100%);
      color: var(--ink);
    }
    .block-container {
      max-width: 1160px;
      padding: 1.45rem 2rem 3rem;
    }
    [data-testid="stHeader"] {
      background: rgba(248, 250, 252, .78);
      backdrop-filter: blur(14px);
    }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
      border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] * {
      color: var(--ink) !important;
    }
    [data-testid="stSidebar"] .stCaptionContainer p {
      color: var(--muted) !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
      min-height: 2.75rem;
      border: 1px solid transparent;
      border-radius: 12px;
      padding: .65rem .75rem;
      margin-bottom: .35rem;
      transition: all .18s ease;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
      background: #eef8fb;
      border-color: rgba(3, 105, 161, .16);
    }
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
      background: linear-gradient(135deg, rgba(3, 105, 161, .10), rgba(15, 118, 110, .10));
      border-color: rgba(15, 118, 110, .28);
    }
    h1, h2, h3, h4, h5, h6, p, label, span {
      letter-spacing: 0 !important;
    }
    .ss-shell {
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      gap: 1.15rem;
    }
    .ss-hero {
      position: relative;
      overflow: hidden;
      padding: 1.55rem 1.7rem;
      border-radius: 18px;
      border: 1px solid rgba(255, 255, 255, .55);
      background:
        linear-gradient(135deg, rgba(3, 105, 161, .97), rgba(15, 118, 110, .95)),
        linear-gradient(90deg, rgba(255, 255, 255, .18), transparent);
      color: white;
      box-shadow: 0 24px 70px rgba(15, 23, 42, .16);
      margin-bottom: 1.2rem;
    }
    .ss-hero:after {
      content: "";
      position: absolute;
      right: -5rem;
      top: -7rem;
      width: 18rem;
      height: 18rem;
      border-radius: 999px;
      background: rgba(255, 255, 255, .16);
    }
    .ss-kicker {
      display: inline-flex;
      align-items: center;
      gap: .45rem;
      padding: .38rem .62rem;
      border-radius: 999px;
      background: rgba(255,255,255,.14);
      color: rgba(255,255,255,.9);
      font-size: .78rem;
      font-weight: 750;
      text-transform: uppercase;
      margin-bottom: .8rem;
    }
    .ss-hero h1 {
      position: relative;
      z-index: 1;
      font-size: clamp(2rem, 3vw, 3.05rem);
      line-height: 1.05;
      margin: 0 0 .65rem;
    }
    .ss-hero p {
      position: relative;
      z-index: 1;
      max-width: 780px;
      margin: 0;
      color: rgba(255,255,255,.86);
      font-size: 1.02rem;
    }
    .ss-strip {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: .85rem;
      margin-bottom: 1.25rem;
    }
    .ss-card {
      padding: 1rem;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--panel);
      box-shadow: 0 16px 44px rgba(15, 23, 42, .07);
    }
    .ss-card strong {
      color: var(--ink);
    }
    .ss-label {
      color: var(--muted);
      font-size: .73rem;
      font-weight: 800;
      letter-spacing: .07em !important;
      text-transform: uppercase;
      margin-bottom: .32rem;
    }
    .ss-value {
      color: var(--ink);
      font-size: 1.35rem;
      font-weight: 800;
      margin: 0;
    }
    .ss-subtle {
      color: var(--muted);
      font-size: .9rem;
      margin: .22rem 0 0;
    }
    .ss-section-title {
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 1rem;
      margin: .3rem 0 .85rem;
    }
    .ss-section-title h2 {
      margin: 0;
      font-size: 1.65rem;
      line-height: 1.15;
    }
    .ss-section-title p {
      margin: .28rem 0 0;
      color: var(--muted);
    }
    div[data-testid="stForm"] {
      padding: 1.1rem 1.1rem 1.2rem;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: rgba(255, 255, 255, .82);
      box-shadow: 0 18px 48px rgba(15, 23, 42, .08);
    }
    label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label, .stFileUploader label {
      color: var(--ink) !important;
      font-weight: 720 !important;
      font-size: .9rem !important;
    }
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"],
    input,
    textarea {
      min-height: 2.8rem;
      background: #ffffff !important;
      color: var(--ink) !important;
      border-color: rgba(15, 23, 42, .14) !important;
      border-radius: 12px !important;
      box-shadow: none !important;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="textarea"]:focus-within {
      border-color: rgba(3, 105, 161, .55) !important;
      box-shadow: 0 0 0 3px rgba(14, 165, 233, .12) !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] svg,
    input::placeholder,
    textarea::placeholder {
      color: #475569 !important;
      fill: #475569 !important;
    }
    [data-testid="stFileUploader"] section {
      border: 1px dashed rgba(3, 105, 161, .36);
      border-radius: 14px;
      background: linear-gradient(180deg, #ffffff, #f8fafc);
      padding: 1rem;
    }
    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
      min-height: 2.95rem;
      border: 0;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--brand), var(--brand-2));
      color: white;
      font-weight: 800;
      box-shadow: 0 12px 28px rgba(3, 105, 161, .18);
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
      color: white;
      filter: brightness(1.04);
      border: 0;
    }
    div[data-testid="stMetric"] {
      padding: 1.1rem;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: rgba(255,255,255,.9);
      box-shadow: 0 16px 44px rgba(15, 23, 42, .08);
    }
    [data-testid="stMetricValue"] {
      color: var(--brand-2);
      font-weight: 850;
    }
    [data-testid="stDataFrame"] {
      border: 1px solid var(--line);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 16px 44px rgba(15, 23, 42, .06);
    }
    .ss-listing-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: .9rem;
      margin: .75rem 0 1rem;
    }
    .ss-listing {
      border: 1px solid var(--line);
      border-radius: 14px;
      background: white;
      padding: .9rem;
      box-shadow: 0 12px 34px rgba(15, 23, 42, .06);
    }
    .ss-listing-title {
      font-weight: 820;
      color: var(--ink);
      margin: 0 0 .25rem;
    }
    .ss-pill {
      display: inline-flex;
      padding: .22rem .5rem;
      border-radius: 999px;
      background: #ecfeff;
      color: #0f766e;
      font-size: .76rem;
      font-weight: 800;
      margin-top: .45rem;
    }
    @media (max-width: 860px) {
      .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
      }
      .ss-strip,
      .ss-listing-grid {
        grid-template-columns: 1fr;
      }
      .ss-hero {
        padding: 1.25rem;
      }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_artifacts():
    model = joblib.load(model_path)
    metadata = joblib.load(metadata_path)
    return model, metadata


def format_inr(value: float) -> str:
    return f"Rs. {value:,.0f}"


def listing_count() -> int:
    if not owner_listing_path.exists():
        return 0
    return len(pd.read_csv(owner_listing_path))


def save_owner_listing(row: dict[str, object]) -> None:
    new_row = pd.DataFrame([row])
    if owner_listing_path.exists():
        existing = pd.read_csv(owner_listing_path)
        new_row = pd.concat([existing, new_row], ignore_index=True)
    new_row.to_csv(owner_listing_path, index=False)


def save_uploaded_image(uploaded_file) -> str:
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        extension = ".jpg"

    image_path = owner_image_dir / f"{datetime.now():%Y%m%d_%H%M%S}_{uuid4().hex[:8]}{extension}"
    image_path.write_bytes(uploaded_file.getbuffer())
    return str(image_path)


def render_page_intro(title: str, description: str, tag: str) -> None:
    st.markdown(
        f"""
        <div class="ss-section-title">
          <div>
            <div class="ss-label">{tag}</div>
            <h2>{title}</h2>
            <p>{description}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_cards() -> None:
    model_state = "Ready" if model_path.exists() else "Train first"
    listings = listing_count()
    st.markdown(
        f"""
        <div class="ss-strip">
          <div class="ss-card">
            <div class="ss-label">Model Status</div>
            <p class="ss-value">{model_state}</p>
            <p class="ss-subtle">Uses your trained Indian rental model</p>
          </div>
          <div class="ss-card">
            <div class="ss-label">Owner Listings</div>
            <p class="ss-value">{listings}</p>
            <p class="ss-subtle">Saved locally for marketplace testing</p>
          </div>
          <div class="ss-card">
            <div class="ss-label">Currency</div>
            <p class="ss-value">INR</p>
            <p class="ss-subtle">Prices display as Indian rupees</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_recent_owner_listings() -> None:
    if not owner_listing_path.exists():
        return

    listings = pd.read_csv(owner_listing_path)
    if listings.empty:
        return

    latest = listings.tail(3).iloc[::-1]
    cards = ['<div class="ss-listing-grid">']
    for _, listing in latest.iterrows():
        title = str(listing.get("space_name", "Untitled space"))
        locality = str(listing.get("locality", ""))
        city = str(listing.get("city", ""))
        space_type = str(listing.get("space_type", "Space"))
        price = float(listing.get("expected_monthly_price_rs", 0) or 0)
        cards.append(
            f"""
            <div class="ss-listing">
              <p class="ss-listing-title">{title}</p>
              <p class="ss-subtle">{locality}, {city}</p>
              <p class="ss-value">{format_inr(price)}</p>
              <span class="ss-pill">{space_type}</span>
            </div>
            """
        )
    cards.append("</div>")

    st.markdown("### Recent Owner Listings")
    st.markdown("".join(cards), unsafe_allow_html=True)
    with st.expander("View listing table"):
        st.dataframe(listings.tail(8), use_container_width=True, hide_index=True)


def render_prediction() -> None:
    render_page_intro(
        "Predict Rental Price",
        "Enter the location and property details to estimate the monthly rental price.",
        "Customer tool",
    )

    if not model_path.exists():
        st.warning("Model is not trained yet. Run the training notebook first, then return here.")
        return

    model, metadata = load_artifacts()

    with st.form("prediction_form"):
        left, right = st.columns([1, 1])

        with left:
            st.markdown("#### Location")
            city = st.text_input("City", "Bangalore")
            locality = st.text_input("Locality", "Whitefield")
            amenities = st.text_input("Amenities", "wifi, parking, ac")

        with right:
            st.markdown("#### Space Details")
            property_type = st.selectbox(
                "Space Type",
                ["Flat", "House", "Villa", "Office", "Studio", "Coworking", "Event Hall", "Warehouse"],
            )
            furnishing = st.selectbox("Furnishing", ["Semi-Furnished", "Furnished", "Unfurnished"])
            area = st.number_input("Area / Size sqft", min_value=100.0, value=1200.0, step=50.0)

        room_col, bath_col = st.columns(2)
        with room_col:
            rooms = st.number_input("Rooms", min_value=0.0, value=2.0, step=1.0)
        with bath_col:
            bathrooms = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=1.0)

        submitted = st.form_submit_button("Predict Price", use_container_width=True)

    if not submitted:
        return

    payload = {
        "city": city.lower().strip(),
        "locality": locality.lower().strip(),
        "property_type": property_type.lower(),
        "area": area,
        "beds": rooms,
        "bathrooms": bathrooms,
        "balconies": 1,
        "furnishing": furnishing.lower(),
        "amenities": amenities,
        "description": amenities,
        "target_type": "monthly_rent",
    }

    predicted_price = float(model.predict(price_input_to_frame(payload))[0])
    metric_col, model_col = st.columns([0.38, 0.62])

    with metric_col:
        st.metric("Predicted Monthly Price", format_inr(predicted_price))

    with model_col:
        st.markdown(
            f"""
            <div class="ss-card">
              <div class="ss-label">Prediction Confidence</div>
              <p class="ss-value">{metadata.get("best_model_name", "Trained model")}</p>
              <p class="ss-subtle">Best model selected by cross-validation and validation RMSE.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_owner_listing() -> None:
    render_page_intro(
        "List Property or Space",
        "Capture owner details, pricing, amenities, and one clear image for marketplace onboarding.",
        "Owner workflow",
    )

    with st.form("owner_listing_form"):
        identity, property_details = st.columns([.95, 1.05])

        with identity:
            st.markdown("#### Owner & Location")
            owner_name = st.text_input("Owner Name")
            contact = st.text_input("Phone or Email")
            space_name = st.text_input("Property / Space Name")
            city = st.text_input("City", "Bangalore")
            locality = st.text_input("Locality")

        with property_details:
            st.markdown("#### Space & Pricing")
            space_type = st.selectbox(
                "Space Type",
                [
                    "Event Hall",
                    "Meeting Room",
                    "Coworking Space",
                    "Parking",
                    "Studio",
                    "Warehouse",
                    "Classroom",
                    "Sports Venue",
                    "Office",
                    "Flat",
                    "Villa",
                ],
            )
            area = st.number_input("Area / Size sqft", min_value=50.0, value=1000.0, step=50.0)
            capacity = st.number_input("Capacity", min_value=1, value=10, step=1)
            expected_price = st.number_input("Expected Monthly Price in Rs.", min_value=0.0, value=50000.0, step=1000.0)
            furnishing = st.selectbox("Furnishing", ["Not Applicable", "Furnished", "Semi-Furnished", "Unfurnished"])

        media_col, notes_col = st.columns([.95, 1.05])
        with media_col:
            property_image = st.file_uploader(
                "Property Image",
                type=["jpg", "jpeg", "png", "webp"],
                help="Upload one clear image of the property or space.",
            )
            if property_image is not None:
                st.image(property_image, caption="Image preview", use_container_width=True)
        with notes_col:
            amenities = st.text_input("Amenities", "wifi, parking, ac")
            description = st.text_area("Description", height=155)

        submitted = st.form_submit_button("Save Owner Listing", use_container_width=True)

    if submitted:
        required_values = [owner_name, contact, space_name, city, locality]
        if any(not str(value).strip() for value in required_values):
            st.error("Please fill owner name, contact, space name, city, and locality.")
            return

        image_path = save_uploaded_image(property_image) if property_image is not None else ""

        save_owner_listing(
            {
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "owner_name": owner_name.strip(),
                "contact": contact.strip(),
                "space_name": space_name.strip(),
                "city": city.strip(),
                "locality": locality.strip(),
                "space_type": space_type,
                "area_sqft": area,
                "capacity": capacity,
                "expected_monthly_price_rs": expected_price,
                "furnishing": furnishing,
                "amenities": amenities.strip(),
                "description": description.strip(),
                "image_path": image_path,
                "status": "draft",
            }
        )
        st.success("Owner listing saved successfully.")

    show_recent_owner_listings()


with st.sidebar:
    st.markdown("## SmartSpace AI")
    st.caption("Rental intelligence workspace")
    section = st.radio(
        "Navigation",
        ["Predict Price", "List Property"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        f"""
        <div class="ss-card">
          <div class="ss-label">Workspace</div>
          <p class="ss-subtle"><strong>Model:</strong> {"Available" if model_path.exists() else "Missing"}</p>
          <p class="ss-subtle"><strong>Listings:</strong> {listing_count()}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="ss-hero">
      <div class="ss-kicker">SmartSpace AI Studio</div>
      <h1>Rental pricing and owner onboarding in one workspace.</h1>
      <p>Estimate Indian rental prices, capture owner spaces, and prepare clean marketplace data for the full SmartSpace AI platform.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_status_cards()

if section == "Predict Price":
    render_prediction()
else:
    render_owner_listing()
