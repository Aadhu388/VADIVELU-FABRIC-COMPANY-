# main.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
import base64
import os
import smtplib
import ssl
from email.message import EmailMessage

app = FastAPI()

# ---------------- EMAIL CONFIG ----------------
SMTP_USER = "amvadivelu@gmail.com" # default sender
SMTP_PASS = "kfww dumt zdsd mcxd" # must be set in environment
CEO_EMAIL = "amvadivelu@gmail.com"       # mail goes to this address


def send_order_mail(
    name: str,
    phone: str,
    customer_email: str,
    customer_address: str,
    cart_summary: str,
    cart_total: int
) -> bool:
    """
    Send order confirmation mail to CEO_EMAIL.
    Returns True if sent successfully, False otherwise.
    """
    if not SMTP_USER or not SMTP_PASS:
        print("SMTP credentials not set. Skipping email.")
        return False

    subject = f"New VFC Order - {name} - ₹{cart_total}"
    body = f"""
New order received from VFC Cart Page

Customer Details:
-----------------
Name    : {name}
Phone   : {phone}
Email   : {customer_email}
Address : {customer_address}

Cart Items:
-----------
{cart_summary}

Total Bill: ₹{cart_total}

Please verify UPI payment and contact the customer for delivery confirmation.
"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = CEO_EMAIL
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("Order email sent successfully.")
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False


# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WALL_PATH = os.path.join(BASE_DIR, "wall.jpg")
PREMIUM_LUNGI_IMG_PATH = os.path.join(BASE_DIR, "lungi1.jpg")

# ---------------- WALLPAPER LOAD ----------------
if os.path.exists(WALL_PATH):
    with open(WALL_PATH, "rb") as f:
        wall_b64 = base64.b64encode(f.read()).decode("utf-8")
    wallpaper_css = f"""
    background-image:url('data:image/jpeg;base64,{wall_b64}');
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
    """
else:
    wallpaper_css = """
    background:radial-gradient(circle at top, #1f2937 0, #020617 45%, #000 100%);
    """

# ---------------- PRODUCT IMAGE LOAD (PREMIUM LUNGI) ----------------
if os.path.exists(PREMIUM_LUNGI_IMG_PATH):
    with open(PREMIUM_LUNGI_IMG_PATH, "rb") as f:
        premium_img_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    premium_img_b64 = ""

# (no image peacock; using emoji instead)
peacock_img_fragment = ""  # kept for compatibility; not used in logo now

# ---------------- SVG LOGO (WITH PEACOCK EMOJI ABOVE VFC) ----------------
logo_svg = f"""
<svg width="85" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">

  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="35%" r="85%">
      <stop offset="0%" stop-color="#222"/>
      <stop offset="70%" stop-color="#050608"/>
      <stop offset="100%" stop-color="#000"/>
    </radialGradient>

    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff4c2"/>
      <stop offset="50%" stop-color="#d4af37"/>
      <stop offset="100%" stop-color="#9a7b2f"/>
    </linearGradient>

    <path id="topTextPath" d="M40,150 A110,110 0 0,1 260,150"/>
    <path id="bottomTextPath" d="M260,150 A110,110 0 0,1 40,150"/>

    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Outer ring -->
  <circle cx="150" cy="150" r="140" fill="url(#bgGrad)"
          stroke="url(#goldGrad)" stroke-width="6"/>

  <!-- Inner ring -->
  <circle cx="150" cy="150" r="125" fill="none"
          stroke="url(#goldGrad)" stroke-width="3"/>

  <!-- Dotted ring -->
  <circle cx="150" cy="150" r="100" fill="none"
          stroke="#666" stroke-width="1.6" stroke-dasharray="3 6"/>

  <!-- Peacock emoji above VFC, centred -->
  <text x="50%" y="110"
        text-anchor="middle"
        font-size="34"
        dominant-baseline="middle">
    🦚
  </text>

  <!-- Top arc text -->
  <text fill="#eedfa5"
        font-size="13"
        letter-spacing="3"
        font-family="Segoe UI">
    <textPath href="#topTextPath"
              startOffset="50%"
              text-anchor="middle"
              dominant-baseline="middle"
              dy="-2">
      VADIVELU FABRIC COMPANY
    </textPath>
  </text>

  <!-- Center text -->
  <text x="50%" y="150" text-anchor="middle"
        font-size="48" font-family="Segoe UI"
        font-weight="900"
        fill="url(#goldGrad)"
        filter="url(#softGlow)">
    VFC
  </text>

  <!-- Since line -->
  <text x="50%" y="190" text-anchor="middle"
        font-size="16" letter-spacing="3"
        font-family="Segoe UI" fill="#F5E6B2">
    SINCE 1988
  </text>

  <!-- Bottom arc text -->
  <text fill="#eedfa5"
        font-size="12"
        letter-spacing="3"
        font-family="Segoe UI">
    <textPath href="#bottomTextPath"
              startOffset="50%"
              text-anchor="middle"
              dominant-baseline="middle"
              dy="6">
      PREMIUM LUNGI MANUFACTURERS
    </textPath>
  </text>

</svg>
"""

# ---------------- BASE CSS (WITH DARK/LIGHT MODE) ----------------
base_style = """
<style>
* {
  box-sizing:border-box;
}

html, body {
  margin:0;
  padding:0;
  width:100%;
  max-width:100%;
  overflow-x:hidden;
  font-family:'Segoe UI',system-ui,sans-serif;
  color:#e5e7eb;
}

body {
""" + wallpaper_css + """
}

/* Light mode body override */
body.theme-light {
  background:#f3f4f6;
  color:#111827;
}

a {
  color:inherit;
}

.page-wrapper {
  min-height:100vh;
  display:flex;
  flex-direction:column;
}

/* HEADER */
.header {
  position:sticky;
  top:0;
  z-index:50;
  background:linear-gradient(90deg, #020617 0, #0b1120 50%, #020617 100%);
  border-bottom:1px solid rgba(148,163,184,0.3);
  box-shadow:0 8px 24px rgba(0,0,0,0.45);
  padding:8px 16px 6px;
}

.header-inner {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:14px;
  flex-wrap:wrap;
}

.brand {
  display:flex;
  align-items:center;
  gap:8px;
  color:#facc15;
  min-width:200px;
}

/* Logo size */
.brand svg {
  width:80px;
  height:auto;
}

.brand-text-main {
  font-weight:700;
  letter-spacing:0.08em;
  font-size:14px;
  text-transform:uppercase;
}

.brand-text-sub {
  font-size:11px;
  color:#e5e7eb;
}

.header-right {
  display:flex;
  align-items:center;
  gap:12px;
  margin-left:8px;
  flex-shrink:0;
}

.cart-pill {
  display:flex;
  align-items:center;
  gap:6px;
  background:#0f172a;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid rgba(250,204,21,0.8);
  font-size:12px;
  cursor:pointer;
}

.cart-pill span {
  font-weight:700;
  color:#facc15;
}

.cart-pill:hover {
  filter:brightness(1.08);
}

/* THEME TOGGLE BUTTON */
.theme-toggle-btn {
  display:flex;
  align-items:center;
  justify-content:center;
  width:34px;
  height:34px;
  border-radius:999px;
  border:1px solid rgba(250,204,21,0.8);
  background:#111827;
  color:#facc15;
  cursor:pointer;
  font-size:18px;
}

.theme-toggle-btn:hover {
  filter:brightness(1.1);
}

/* SUB NAV */
.subnav {
  display:flex;
  gap:12px;
  padding:6px 20px 8px;
  background:rgba(15,23,42,0.96);
  border-top:1px solid rgba(51,65,85,0.8);
  box-shadow:0 6px 18px rgba(0,0,0,0.4) inset;
  overflow-x:auto;
}

.subnav span {
  font-size:12px;
  padding:4px 10px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,0.7);
  color:#e5e7eb;
  cursor:pointer;
  white-space:nowrap;
}

.subnav span:hover {
  background:rgba(15,23,42,0.9);
  border-color:#facc15;
}

.section {
  width:94%;
  max-width:1150px;
  margin:22px auto;
  padding:22px 24px 26px;
  background:rgba(15,23,42,0.94);
  border-radius:18px;
  box-shadow:0 25px 50px rgba(0,0,0,0.5);
  border:1px solid rgba(148,163,184,0.35);
}

.hero-title {
  font-size:26px;
  color:#f9fafb;
  margin-top:0;
}

.hero-highlight {
  color:#facc15;
  font-weight:700;
}

.hero-meta {
  font-size:14px;
  color:#cbd5f5;
  margin-top:8px;
}

.chip-row {
  margin-top:14px;
}

.chip {
  display:inline-block;
  font-size:11px;
  padding:4px 10px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,0.7);
  color:#e5e7eb;
  margin-right:8px;
  margin-bottom:4px;
}

.section h2 {
  margin-top:0;
  color:#facc15;
  letter-spacing:0.08em;
  font-size:16px;
  text-transform:uppercase;
}

.section p {
  font-size:14px;
  color:#e5e7eb;
}

footer {
  text-align:center;
  padding:14px 10px 20px;
  font-size:11px;
  color:#9ca3af;
  margin-top:auto;
}

/* PRODUCTS LAYOUT */
.products-layout {
  display:grid;
  grid-template-columns:260px 1fr;
  gap:18px;
}

@media (max-width:900px) {
  .products-layout {
    grid-template-columns:1fr;
  }
}

/* SEARCH ON PRODUCTS PAGE ONLY */
.products-search-row {
  margin:10px 0 14px;
}

.products-search-input {
  width:100%;
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,0.7);
  background:#020617;
  color:#e5e7eb;
  font-size:13px;
  outline:none;
}

.products-search-input:focus {
  border-color:#facc15;
  box-shadow:0 0 0 1px rgba(250,204,21,0.6);
}

/* FILTERS */
.filters-card {
  background:radial-gradient(circle at top left, #020617, #020617 60%, #000 100%);
  border-radius:16px;
  border:1px solid rgba(148,163,184,0.5);
  padding:14px 14px 16px;
  box-shadow:0 18px 35px rgba(0,0,0,0.65);
  font-size:13px;
}

.filters-card h3 {
  margin:0 0 10px;
  font-size:14px;
  color:#facc15;
  text-transform:uppercase;
  letter-spacing:0.08em;
}

.filter-group {
  margin-bottom:10px;
}

.filter-group label {
  display:block;
  margin-bottom:6px;
  color:#cbd5f5;
  font-size:12px;
}

.filter-group select {
  width:100%;
  padding:6px 8px;
  border-radius:8px;
  border:1px solid rgba(148,163,184,0.7);
  background:#020617;
  color:#e5e7eb;
  font-size:12px;
}

/* PRODUCT GRID + CARDS */
.products-grid {
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:16px;
  margin-top:8px;
}

.product-card {
  background:radial-gradient(circle at top left, #1f2937, #020617);
  border-radius:16px;
  border:1px solid rgba(148,163,184,0.45);
  padding:20px 10px 14px;
  box-shadow:0 18px 35px rgba(0,0,0,0.55);
  position:relative;
  overflow:hidden;
}

.product-badge {
  position:absolute;
  top:6px;
  left:10px;
  padding:2px 8px;
  border-radius:999px;
  font-size:10px;
  text-transform:uppercase;
  letter-spacing:0.12em;
  background:rgba(250,204,21,0.1);
  border:1px solid rgba(250,204,21,0.8);
  color:#facc15;
  z-index:3;
}

.product-img {
  width:100%;
  border-radius:12px;
  margin:8px 0 6px;
  border:1px solid rgba(148,163,184,0.4);
  display:block;
}

.product-brand {
  font-size:11px;
  color:#9ca3af;
  text-transform:uppercase;
  letter-spacing:0.14em;
  margin-top:18px;
}

.product-title {
  margin:2px 0 4px;
  font-size:14px;
  color:#f9fafb;
  font-weight:600;
}

.product-price-row {
  display:flex;
  align-items:baseline;
  gap:6px;
  margin-bottom:6px;
}

.product-price {
  font-size:15px;
  font-weight:700;
  color:#facc15;
}

.product-mrp {
  font-size:12px;
  color:#9ca3af;
  text-decoration:line-through;
}

.product-discount {
  font-size:11px;
  color:#4ade80;
  font-weight:600;
}

.product-meta-small {
  font-size:11px;
  color:#9ca3af;
  margin-bottom:6px;
}

.cart-controls {
  display:flex;
  align-items:center;
  gap:6px;
  margin-top:4px;
}

.qty-btn {
  width:26px;
  height:26px;
  border-radius:50%;
  border:none;
  background:#111827;
  color:#facc15;
  font-weight:700;
  font-size:14px;
  cursor:pointer;
}

.qty-btn:hover {
  filter:brightness(1.15);
}

.qty-label {
  min-width:18px;
  text-align:center;
  font-size:13px;
  background:#020617;
  padding:3px 6px;
  border-radius:999px;
  border:1px solid rgba(148,163,184,0.5);
  color:#e5e7eb;
}

.add-to-cart-main {
  margin-left:auto;
  padding:5px 12px;
  border-radius:999px;
  border:none;
  background:linear-gradient(135deg,#facc15,#eab308);
  color:#111827;
  font-weight:700;
  font-size:11px;
  cursor:pointer;
}

.add-to-cart-main:hover {
  filter:brightness(1.08);
}

/* CART SUMMARY CARD */
.cart-bar {
  margin-top:20px;
  padding:12px 14px;
  border-radius:14px;
  background:rgba(15,23,42,0.98);
  border:1px solid rgba(250,204,21,0.7);
  font-size:13px;
}

.cart-bar-top {
  display:flex;
  flex-wrap:wrap;
  justify-content:space-between;
  gap:8px;
}

.cart-items-list {
  list-style:none;
  padding-left:0;
  margin-top:8px;
  max-height:220px;
  overflow-y:auto;
}

.cart-note {
  font-size:12px;
  color:#facc15;
  margin-top:4px;
}

.cart-summary-total {
  font-weight:700;
  margin-top:6px;
}

.small-cta {
  display:inline-block;
  padding:8px 12px;
  border-radius:10px;
  font-weight:700;
  text-decoration:none;
  border:none;
  cursor:pointer;
  font-size:12px;
}

.whatsapp-btn {
  background:#25D366;
  color:#042a18;
}

.upi-btn {
  background:linear-gradient(135deg,#facc15,#eab308);
  color:#111827;
}

.copy-btn {
  background:#3b82f6;
  color:white;
}

.form-field {
  margin-bottom:10px;
}

input, textarea {
  width:100%;
  padding:8px 10px;
  border-radius:8px;
  border:1px solid rgba(148,163,184,0.6);
  background:rgba(15,23,42,0.95);
  color:#e5e7eb;
  font-size:13px;
}

textarea {
  min-height:70px;
}

button {
  font-family:inherit;
}

ul {
  padding-left:18px;
  margin-top:6px;
  margin-bottom:10px;
}

ul li {
  font-size:13px;
  color:#e5e7eb;
  margin-bottom:4px;
}

/* PROFILE DROPDOWN */
.profile-menu-btn {
  display:flex;
  align-items:center;
  gap:6px;
  padding:6px 12px;
  border-radius:999px;
  background:#111827;
  border:1px solid rgba(250,204,21,0.8);
  color:#facc15;
  font-size:13px;
  cursor:pointer;
  font-weight:700;
}

.profile-menu-btn:hover {
  filter:brightness(1.1);
}

.profile-dropdown {
  position:absolute;
  top:50px;
  right:20px;
  background:#0b1120;
  border-radius:12px;
  padding:10px 0;
  border:1px solid rgba(250,204,21,0.4);
  box-shadow:0 8px 30px rgba(0,0,0,0.6);
  display:none;
  min-width:190px;
  z-index:200;
}

.profile-dropdown a {
  display:block;
  padding:8px 16px;
  font-size:13px;
  color:#e5e7eb;
  text-decoration:none;
}

.profile-dropdown a:hover {
  background:rgba(250,204,21,0.15);
}

/* ------- LIGHT THEME OVERRIDES ------- */
.theme-light .header {
  background:linear-gradient(90deg,#ffffff 0,#f3f4f6 50%,#ffffff 100%);
  border-bottom:1px solid #e5e7eb;
  box-shadow:0 4px 12px rgba(15,23,42,0.08);
}

.theme-light .brand-text-sub {
  color:#4b5563;
}

.theme-light .subnav {
  background:#e5e7eb;
  border-top:1px solid #d1d5db;
  box-shadow:none;
}

.theme-light .subnav span {
  border-color:#d1d5db;
  color:#111827;
}

.theme-light .subnav span:hover {
  background:#f9fafb;
  border-color:#f59e0b;
}

.theme-light .section {
  background:#ffffff;
  border:1px solid #e5e7eb;
  box-shadow:0 10px 30px rgba(15,23,42,0.08);
}

.theme-light .hero-title {
  color:#111827;
}

.theme-light .hero-meta,
.theme-light .section p {
  color:#374151;
}

.theme-light .chip {
  border-color:#d1d5db;
  color:#111827;
}

.theme-light footer {
  background:#f3f4f6;
  color:#4b5563;
}

.theme-light .products-search-input {
  background:#ffffff;
  color:#111827;
  border-color:#d1d5db;
}

.theme-light .filters-card {
  background:#f9fafb;
  border-color:#e5e7eb;
  box-shadow:0 8px 20px rgba(15,23,42,0.06);
}

.theme-light .product-card {
  background:#ffffff;
  border-color:#e5e7eb;
  box-shadow:0 8px 20px rgba(15,23,42,0.06);
}

.theme-light .product-title {
  color:#111827;
}

.theme-light .product-meta-small {
  color:#6b7280;
}

.theme-light .cart-bar {
  background:#ffffff;
  border-color:#f59e0b;
}

.theme-light .cart-note {
  color:#b45309;
}

.theme-light input,
.theme-light textarea {
  background:#ffffff;
  color:#111827;
  border-color:#d1d5db;
}

.theme-light .profile-menu-btn,
.theme-light .cart-pill,
.theme-light .theme-toggle-btn {
  background:#f9fafb;
  color:#92400e;
  border-color:#f59e0b;
}

.theme-light .profile-dropdown {
  background:#ffffff;
  border-color:#e5e7eb;
  box-shadow:0 10px 30px rgba(15,23,42,0.12);
}

/* ------------ MEDIA QUERIES ------------ */
@media (max-width: 768px) {
  body {
    font-size:13px;
  }
  .section {
    width:96%;
    margin:14px auto;
    padding:16px 14px 18px;
  }
  .hero-title {
    font-size:20px;
  }
  .hero-meta, .section p {
    font-size:13px;
  }
  .product-title {
    font-size:13px;
  }
  .product-price {
    font-size:14px;
  }
  .products-grid {
    grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  }
  .brand svg {
    width:72px;
  }
}

@media (max-width: 480px) {
  body {
    font-size:12px;
  }
  .header {
    padding:6px 10px;
  }
  .header-inner {
    gap:6px;
  }
  .brand {
    min-width:0;
    flex:1 1 60%;
  }
  .brand svg {
    width:64px;
  }
  .header-right {
    flex:1 1 40%;
    justify-content:flex-end;
    margin-left:0;
    gap:6px;
  }
  .profile-menu-btn {
    padding:4px 8px;
    font-size:11px;
  }
  .cart-pill {
    font-size:11px;
    padding:4px 8px;
  }
  .theme-toggle-btn {
    width:30px;
    height:30px;
    font-size:16px;
  }
  .hero-title {
    font-size:18px;
  }
  .chip {
    font-size:10px;
    padding:3px 8px;
  }
  .products-grid {
    grid-template-columns:1fr;
  }
}

@media (min-width: 1200px) {
  .section {
    max-width:1280px;
  }
  .hero-title {
    font-size:30px;
  }
  .products-grid {
    grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  }
  .brand svg {
    width:90px;
  }
}
</style>
"""

# ---------------- HEADER HTML ----------------
def header_html() -> str:
    return f"""
    <div class="header">
      <div class="header-inner">
        <div class="brand">
          <div>{logo_svg}</div>
          <div>
            <div class="brand-text-main">VADIVELU FABRIC COMPANY</div>
            <div class="brand-text-sub">Premium Lungi & Home Textile Manufacturers</div>
          </div>
        </div>
        <div class="header-right">
          <button type="button" class="theme-toggle-btn" onclick="toggleTheme()">
            <span id="theme-toggle-icon">🌙</span>
          </button>
          <button type="button" class="profile-menu-btn" onclick="toggleProfileMenu()">
            👤 Profile
          </button>
          <div id="profile-dropdown" class="profile-dropdown">
            <a href="/profile">My Profile</a>
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/cart">Cart / Payment</a>
            <a href="/about">About Company</a>
            <a href="/contact">Contact</a>
          </div>

          <div class="cart-pill" onclick="window.location='/cart';">
            🛒 Cart: <span id="header-cart-count">0</span>
          </div>
        </div>
      </div>
      <div class="subnav">
        <span data-category="All">All</span>
        <span data-category="Lungi">Lungis</span>
        <span data-category="Home Textile">Home Textiles</span>
        <span data-category="Premium">Premium</span>
        <span data-category="Budget">Budget</span>
      </div>
    </div>
    """


# ---------------- COMMON PROFILE SCRIPT ----------------
profile_script = """
<script>
function toggleProfileMenu() {
  const menu = document.getElementById('profile-dropdown');
  if (!menu) return;
  menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}

document.addEventListener('click', function(e) {
  const menu = document.getElementById('profile-dropdown');
  const btn = document.querySelector('.profile-menu-btn');
  if (!menu || !btn) return;
  if (!menu.contains(e.target) && !btn.contains(e.target)) {
    menu.style.display = 'none';
  }
});
</script>
"""

# ---------------- CART + FILTER LOGIC + THEME SCRIPT ----------------
# NOTE: this version includes cart page +/- buttons and event handlers,
# and enforces payment confirmation (client-side + sets a hidden field)
products_script = """
<script>
  /* THEME HANDLING */
  function applyTheme(theme) {
    const body = document.body;
    if (!body) return;

    body.classList.remove('theme-dark', 'theme-light');

    if (theme === 'light') {
      body.classList.add('theme-light');
    } else {
      body.classList.add('theme-dark');
      theme = 'dark';
    }

    try {
      localStorage.setItem('vfc_theme', theme);
    } catch (e) {}

    const icon = document.getElementById('theme-toggle-icon');
    if (icon) {
      icon.textContent = (theme === 'light') ? '☀️' : '🌙';
    }
  }

  function toggleTheme() {
    let current = 'dark';
    try {
      current = localStorage.getItem('vfc_theme') || 'dark';
    } catch (e) {}
    const next = (current === 'dark') ? 'light' : 'dark';
    applyTheme(next);
  }

  /* CART / FILTERS */
  let cart = {};

  function loadCartFromStorage() {
    try {
      const saved = localStorage.getItem('vfc_cart');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && typeof parsed === 'object') {
          cart = parsed;
          return;
        }
      }
    } catch (e) {
      // ignore parse errors
    }
    cart = {};
  }

  function saveCartToStorage() {
    try {
      localStorage.setItem('vfc_cart', JSON.stringify(cart));
    } catch (e) {
      // ignore
    }
  }

  // changeQty used on product cards: name (string), price (number), delta (+1 or -1)
  function changeQty(name, price, delta) {
    if (!name) return;
    if (!cart[name]) {
      cart[name] = { price: price, qty: 0 };
    }
    cart[name].qty += delta;
    if (cart[name].qty <= 0) {
      delete cart[name];
    }
    renderCart();
    updateQtyLabels();
    saveCartToStorage();
  }

  // Render the cart into multiple places (header count, small list, and the cart page list)
  function renderCart() {
    const countEl = document.getElementById('cart-count');
    const totalEl = document.getElementById('cart-total');
    const listEl = document.getElementById('cart-items');

    const countEl2 = document.getElementById('cart-count-page');
    const totalEl2 = document.getElementById('cart-total-page');
    const listEl2 = document.getElementById('cart-items-page');

    const headerCountEl = document.getElementById('header-cart-count');

    let totalItems = 0;
    let totalAmount = 0;
    const names = Object.keys(cart);
    let summaryText = "";

    names.forEach((name, idx) => {
      const item = cart[name];
      const lineTotal = item.qty * item.price;
      totalItems += item.qty;
      totalAmount += lineTotal;
      summaryText += (idx + 1) + ". " + name + " × " + item.qty + " = ₹" + lineTotal + "\\n";
    });

    if (countEl) countEl.textContent = totalItems;
    if (totalEl) totalEl.textContent = '₹' + totalAmount;
    if (listEl) {
      listEl.innerHTML = '';
      names.forEach((name, idx) => {
        const item = cart[name];
        const li = document.createElement('li');
        li.textContent = (idx + 1) + '. ' + name + ' × ' + item.qty + ' = ₹' + (item.qty * item.price);
        listEl.appendChild(li);
      });
    }

    if (countEl2) countEl2.textContent = totalItems;
    if (totalEl2) totalEl2.textContent = '₹' + totalAmount;
    if (listEl2) {
      listEl2.innerHTML = '';
      names.forEach((name, idx) => {
        const item = cart[name];
        // Build a cart line with - and + buttons on the cart page
        const li = document.createElement('li');
        li.style.display = 'flex';
        li.style.alignItems = 'center';
        li.style.justifyContent = 'space-between';
        li.style.gap = '12px';

        const left = document.createElement('div');
        left.style.flex = '1';
        left.textContent = (idx + 1) + '. ' + name;

        const center = document.createElement('div');
        center.style.display = 'flex';
        center.style.alignItems = 'center';
        center.style.gap = '8px';

        const minusBtn = document.createElement('button');
        minusBtn.type = 'button';
        minusBtn.className = 'small-cta';
        minusBtn.style.padding = '6px 8px';
        minusBtn.textContent = '−';
        minusBtn.setAttribute('data-name', name);
        minusBtn.setAttribute('data-action', 'decrease');

        const qtySpan = document.createElement('span');
        qtySpan.className = 'qty-label';
        qtySpan.style.minWidth = '26px';
        qtySpan.style.textAlign = 'center';
        qtySpan.textContent = item.qty;
        qtySpan.setAttribute('data-name', name);

        const plusBtn = document.createElement('button');
        plusBtn.type = 'button';
        plusBtn.className = 'small-cta';
        plusBtn.style.padding = '6px 8px';
        plusBtn.textContent = '+';
        plusBtn.setAttribute('data-name', name);
        plusBtn.setAttribute('data-action', 'increase');

        center.appendChild(minusBtn);
        center.appendChild(qtySpan);
        center.appendChild(plusBtn);

        const right = document.createElement('div');
        right.style.minWidth = '110px';
        right.style.textAlign = 'right';
        right.textContent = '₹' + (item.qty * item.price);

        li.appendChild(left);
        li.appendChild(center);
        li.appendChild(right);

        listEl2.appendChild(li);
      });
    }

    if (headerCountEl) headerCountEl.textContent = totalItems;

    // ----- UPI QR AUTO AMOUNT ----- 
    const baseUpi = "upi://pay?pa=9976791919@ybl&pn=Vadivelu%20Fabric%20Company&cu=INR";

    const qrImg = document.getElementById('upi-qr');
    if (qrImg) {
      let upiForQr = baseUpi;
      if (totalAmount > 0) {
        upiForQr += "&am=" + totalAmount;
      }
      const qrBase = "https://api.qrserver.com/v1/create-qr-code/?size=260x260&data=";
      qrImg.src = qrBase + encodeURIComponent(upiForQr);
    }

    // ----- SET HIDDEN FIELDS FOR EMAIL FORM ----- 
    const summaryInput = document.getElementById('cart_summary');
    const totalInput = document.getElementById('cart_total');
    if (summaryInput) summaryInput.value = summaryText;
    if (totalInput) totalInput.value = totalAmount;

    // Also update hidden payment_confirmed default when cart changes (no effect on checkbox)
    const paymentHidden = document.getElementById('payment_confirmed');
    if (paymentHidden && paymentHidden.value !== 'yes') {
      paymentHidden.value = 'no';
    }

    saveCartToStorage();
  }

  function updateQtyLabels() {
    document.querySelectorAll('.qty-label').forEach(span => {
      const name = span.getAttribute('data-name');
      span.textContent = cart[name] ? cart[name].qty : 0;
    });
    // header count
    const headerCountEl = document.getElementById('header-cart-count');
    let totalItems = 0;
    Object.values(cart).forEach(it => totalItems += it.qty || 0);
    if (headerCountEl) headerCountEl.textContent = totalItems;
  }

  function applyFilters() {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    const categorySelect = document.getElementById('filter-category');
    const priceSelect = document.getElementById('filter-price');
    const searchInput = document.getElementById('global-search-input');
    const sortSelect = document.getElementById('sort-by');
    const cards = Array.from(grid.querySelectorAll('.product-card'));

    const category = categorySelect ? categorySelect.value : 'All';
    const priceRange = priceSelect ? priceSelect.value : 'All';
    const search = searchInput ? searchInput.value.trim().toLowerCase() : '';
    const sortBy = sortSelect ? sortSelect.value : 'default';

    cards.forEach(card => {
      const name = (card.getAttribute('data-name') || '').toLowerCase();
      const categoryValue = card.getAttribute('data-category') || '';
      const tags = (card.getAttribute('data-tags') || '').toLowerCase();
      const price = parseInt(card.getAttribute('data-price') || '0');

      let visible = true;

      if (category !== 'All' && categoryValue != category) visible = false;

      if (priceRange !== 'All') {
        const parts = priceRange.split('-');
        const min = parseInt(parts[0]);
        const max = parseInt(parts[1]);
        if (!(price >= min && price <= max)) visible = false;
      }

      if (search && !(name.includes(search) || tags.includes(search))) visible = false;

      card.style.display = visible ? '' : 'none';
    });

    let sorted = cards.slice();
    if (sortBy === 'price-asc') {
      sorted.sort((a,b) => parseInt(a.getAttribute('data-price')) - parseInt(b.getAttribute('data-price')));
    } else if (sortBy === 'price-desc') {
      sorted.sort((a,b) => parseInt(b.getAttribute('data-price')) - parseInt(a.getAttribute('data-price')));
    }
    sorted.forEach(card => grid.appendChild(card));
  }

  document.addEventListener('DOMContentLoaded', () => {
    // THEME INITIALISATION
    let savedTheme = 'dark';
    try {
      savedTheme = localStorage.getItem('vfc_theme') || 'dark';
    } catch (e) {}
    applyTheme(savedTheme);

    // CART + FILTERS
    loadCartFromStorage();
    updateQtyLabels();
    renderCart();
    applyFilters();

    const shareBtn = document.getElementById('share-whatsapp');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        const names = Object.keys(cart);
        if (names.length === 0) {
          alert('Your cart is empty. Please add items before sharing the order.');
          return;
        }

        let message = "🧾 *New Order Request from VFC Website*%0A%0A";
        let total = 0;
        names.forEach((name, idx) => {
          const item = cart[name];
          const subtotal = item.qty * item.price;
          total += subtotal;
          message += (idx + 1) + ". *" + name + "* × " + item.qty + " = ₹" + subtotal + "%0A";
        });
        message += "%0A*Total: ₹" + total + "*%0A%0A";
        message += "Name: [Your Name]%0APhone/Email: [Your Contact]%0AAddress: [Delivery Address]%0A%0A";
        message += "After completing the UPI payment, I will send the payment screenshot here.%0A";
        message += "Please contact me to confirm delivery.%0A";

        const phone = "919976791919";
        const url = "https://wa.me/" + phone + "?text=" + message;
        window.open(url, "_blank");
      });
    }

    const copyUpiIdBtn = document.getElementById('copy-upi-id');
    if (copyUpiIdBtn) {
      copyUpiIdBtn.addEventListener('click', () => {
        const upiId = "9976791919@ybl";
        navigator.clipboard.writeText(upiId).then(() => {
          alert('UPI ID copied to clipboard.');
        }, () => {
          alert('Unable to copy. Please copy manually: 9976791919@ybl');
        });
      });
    }

    const categorySelect = document.getElementById('filter-category');
    const priceSelect = document.getElementById('filter-price');
    const sortSelect = document.getElementById('sort-by');
    const searchInput = document.getElementById('global-search-input');

    if (categorySelect) categorySelect.addEventListener('change', applyFilters);
    if (priceSelect)  priceSelect.addEventListener('change', applyFilters);
    if (sortSelect)   sortSelect.addEventListener('change', applyFilters);

    if (searchInput) {
      searchInput.addEventListener('input', applyFilters);
      searchInput.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          e.preventDefault();
          applyFilters();
        }
      });
    }

    document.querySelectorAll('.subnav span[data-category]').forEach(chip => {
      chip.addEventListener('click', () => {
        const cat = chip.getAttribute('data-category');
        const categorySelect = document.getElementById('filter-category');
        if (categorySelect) {
          categorySelect.value = cat;
          applyFilters();
        }
      });
    });

    // Show payment confirmation form only after payment checkbox ticked
    const payCheckbox = document.getElementById('payment-done-checkbox');
    const payFormWrapper = document.getElementById('payment-form-wrapper');
    const paymentHidden = document.getElementById('payment_confirmed');

    if (payCheckbox && payFormWrapper) {
      payCheckbox.addEventListener('change', () => {
        const checked = payCheckbox.checked;
        payFormWrapper.style.display = checked ? 'block' : 'none';
        if (paymentHidden) {
          paymentHidden.value = checked ? 'yes' : 'no';
        }
      });
    }

    // Event delegation for cart page +/- buttons (dynamically created)
    document.body.addEventListener('click', function (ev) {
      const btn = ev.target;
      if (!btn) return;
      const action = btn.getAttribute && btn.getAttribute('data-action');
      const name = btn.getAttribute && btn.getAttribute('data-name');
      if (!action || !name) return;

      if (action === 'increase') {
        // find price from stored cart or default 0
        const price = (cart[name] && cart[name].price) ? cart[name].price : 0;
        changeQty(name, price, +1);
      } else if (action === 'decrease') {
        const price = (cart[name] && cart[name].price) ? cart[name].price : 0;
        changeQty(name, price, -1);
      }
    });

    // Ensure checkout form has the latest cart data at submit time and enforce payment confirmation
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
      checkoutForm.addEventListener('submit', function (e) {
        // ensure hidden fields updated
        const summaryInput = document.getElementById('cart_summary');
        const totalInput = document.getElementById('cart_total');
        const paymentHiddenLocal = document.getElementById('payment_confirmed');
        let summaryText = "";
        let totalAmount = 0;
        const names = Object.keys(cart);
        names.forEach((name, idx) => {
          const item = cart[name];
          const lineTotal = (item.qty || 0) * (item.price || 0);
          summaryText += (idx + 1) + ". " + name + " × " + item.qty + " = ₹" + lineTotal + "\\n";
          totalAmount += lineTotal;
        });
        if (summaryInput) summaryInput.value = summaryText;
        if (totalInput) totalInput.value = totalAmount;

        // enforce: cart must not be empty and payment must be confirmed
        if (!paymentHiddenLocal || paymentHiddenLocal.value !== 'yes') {
          e.preventDefault();
          alert('Please confirm your UPI / Google Pay payment by ticking the checkbox before submitting the form.');
          return;
        }

        if (totalAmount <= 0) {
          e.preventDefault();
          alert('Your cart is empty. Add items before submitting payment confirmation.');
          return;
        }

        // allow submit to continue if checks pass
      });
    }
  });
</script>
"""

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home():
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h1 class="hero-title">
              Fashion-Style <span class="hero-highlight">Lungi & Textile Store</span> from Erode
            </h1>
            <p class="hero-meta">
              Experience an online-store layout like Amazon / Meesho / Myntra / Ajio,
              with simple cart and WhatsApp ordering – directly from the manufacturer.
            </p>
            <div class="chip-row">
              <span class="chip">Premium Lungis</span>
              <span class="chip">Budget Lungis</span>
              <span class="chip">Dobby & Designer</span>
              <span class="chip">Super Quality</span>
              <span class="chip">Towels</span>
              <span class="chip">Bedspreads</span>
              <span class="chip">Kerchiefs</span>
            </div>
          </div>

          <footer>
            © Vadivelu Fabric Company • Erode District, Tamil Nadu • Phone / WhatsApp: +91 99767 91919
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- PRODUCTS PAGE ----------------
@app.get("/products", response_class=HTMLResponse)
def products_page():
    premium_img_html = ""
    if premium_img_b64:
        premium_img_html = f"""
        <img class="product-img"
             src="data:image/jpeg;base64,{premium_img_b64}"
             alt="Premium Lungi" />
        """

    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Products - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}

          <div class="section">
            <h2>All Products</h2>
            <p>Browse products in an e-commerce layout similar to Amazon, Meesho, Myntra, Ajio – with filters, search and cart.</p>

            <div class="products-search-row">
              <input id="global-search-input"
                     class="products-search-input"
                     placeholder="Search premium lungi, towels, bedspreads, kerchiefs..." />
            </div>

            <div class="products-layout">
              <div class="filters-card">
                <h3>Filters</h3>

                <div class="filter-group">
                  <label>Category</label>
                  <select id="filter-category">
                    <option value="All">All</option>
                    <option value="Lungi">Lungis</option>
                    <option value="Home Textile">Home Textile</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label>Price Range</label>
                  <select id="filter-price">
                    <option value="All">All</option>
                    <option value="0-120">Up to ₹120</option>
                    <option value="121-170">₹121 – ₹170</option>
                  </select>
                </div>

                <div class="filter-group">
                  <label>Sort By</label>
                  <select id="sort-by">
                    <option value="default">Recommended</option>
                    <option value="price-asc">Price: Low to High</option>
                    <option value="price-desc">Price: High to Low</option>
                  </select>
                </div>

                <p style="font-size:12px;color:#9ca3af;margin-top:10px;">
                  Use the search box and filters to quickly find premium / budget / home textile products.
                </p>
              </div>

              <div>
                <div class="products-grid" id="product-grid">

                  <div class="product-card"
                       data-name="Premium Cotton Lungi"
                       data-category="Lungi"
                       data-tags="premium gifting soft"
                       data-price="170">
                    <span class="product-badge">Premium</span>
                    {premium_img_html}
                    <div class="product-brand">VFC ORIGINALS</div>
                    <div class="product-title">Premium Cotton Lungi</div>
                    <div class="product-price-row">
                      <span class="product-price">₹170</span>
                      <span class="product-mrp">₹220</span>
                      <span class="product-discount">23% OFF</span>
                    </div>
                    <p class="product-meta-small">Soft, rich colours · Ideal for premium customers and gifting.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Premium Cotton Lungi',170,-1)">-</button>
                      <span class="qty-label" data-name="Premium Cotton Lungi">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Premium Cotton Lungi',170,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Premium Cotton Lungi',170,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Budget Friendly Lungi"
                       data-category="Lungi"
                       data-tags="budget regular"
                       data-price="110">
                    <span class="product-badge">Budget</span>
                    <div class="product-brand">VFC BASIC</div>
                    <div class="product-title">Budget Friendly Lungi</div>
                    <div class="product-price-row">
                      <span class="product-price">₹110</span>
                      <span class="product-mrp">₹150</span>
                      <span class="product-discount">27% OFF</span>
                    </div>
                    <p class="product-meta-small">Comfortable, budget-friendly lungi for regular everyday use.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Budget Friendly Lungi',110,-1)">-</button>
                      <span class="qty-label" data-name="Budget Friendly Lungi">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Budget Friendly Lungi',110,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Budget Friendly Lungi',110,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Dobby Quality Lungi"
                       data-category="Lungi"
                       data-tags="dobby designer pattern"
                       data-price="170">
                    <span class="product-badge">Designer</span>
                    <div class="product-brand">VFC DESIGNER</div>
                    <div class="product-title">Dobby Quality Lungi</div>
                    <div class="product-price-row">
                      <span class="product-price">₹170</span>
                      <span class="product-mrp">₹230</span>
                      <span class="product-discount">26% OFF</span>
                    </div>
                    <p class="product-meta-small">Attractive dobby weave designs ideal for showrooms.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Dobby Quality Lungi',170,-1)">-</button>
                      <span class="qty-label" data-name="Dobby Quality Lungi">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Dobby Quality Lungi',170,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Dobby Quality Lungi',170,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Super Quality Lungi"
                       data-category="Lungi"
                       data-tags="super wholesale"
                       data-price="130">
                    <span class="product-badge">Popular</span>
                    <div class="product-brand">VFC CLASSIC</div>
                    <div class="product-title">Super Quality Lungi</div>
                    <div class="product-price-row">
                      <span class="product-price">₹130</span>
                      <span class="product-mrp">₹185</span>
                      <span class="product-discount">30% OFF</span>
                    </div>
                    <p class="product-meta-small">Comfort, colour fastness, affordability – perfect for bulk orders.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Super Quality Lungi',130,-1)">-</button>
                      <span class="qty-label" data-name="Super Quality Lungi">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Super Quality Lungi',130,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Super Quality Lungi',130,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Cotton Towels"
                       data-category="Home Textile"
                       data-tags="towel bath face lodge hotel"
                       data-price="120">
                    <span class="product-badge">Home Textile</span>
                    <div class="product-brand">VFC HOME</div>
                    <div class="product-title">Cotton Towels</div>
                    <div class="product-price-row">
                      <span class="product-price">₹120</span>
                      <span class="product-mrp">₹160</span>
                      <span class="product-discount">25% OFF</span>
                    </div>
                    <p class="product-meta-small">Absorbent cotton towels for home, lodge and hotel use.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Cotton Towels',120,-1)">-</button>
                      <span class="qty-label" data-name="Cotton Towels">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Cotton Towels',120,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Cotton Towels',120,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Bedspreads"
                       data-category="Home Textile"
                       data-tags="bedspread bed sheet"
                       data-price="100">
                    <span class="product-badge">Home Textile</span>
                    <div class="product-brand">VFC HOME</div>
                    <div class="product-title">Bedspreads</div>
                    <div class="product-price-row">
                      <span class="product-price">₹100</span>
                      <span class="product-mrp">₹140</span>
                      <span class="product-discount">29% OFF</span>
                    </div>
                    <p class="product-meta-small">Soft, durable, neatly stitched for long-term use.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Bedspreads',100,-1)">-</button>
                      <span class="qty-label" data-name="Bedspreads">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Bedspreads',100,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Bedspreads',100,1)">Add to Cart</button>
                    </div>
                  </div>

                  <div class="product-card"
                       data-name="Kerchiefs (1 dozen)"
                       data-category="Home Textile"
                       data-tags="kerchief hanky handkerchief"
                       data-price="130">
                    <span class="product-badge">Essentials</span>
                    <div class="product-brand">VFC ESSENTIALS</div>
                    <div class="product-title">Kerchiefs (1 dozen)</div>
                    <div class="product-price-row">
                      <span class="product-price">₹130</span>
                      <span class="product-mrp">₹170</span>
                      <span class="product-discount">24% OFF</span>
                    </div>
                    <p class="product-meta-small">Plain & printed, custom packing and bulk orders accepted.</p>
                    <div class="cart-controls">
                      <button class="qty-btn"
                              onclick="changeQty('Kerchiefs (1 dozen)',130,-1)">-</button>
                      <span class="qty-label" data-name="Kerchiefs (1 dozen)">0</span>
                      <button class="qty-btn"
                              onclick="changeQty('Kerchiefs (1 dozen)',130,1)">+</button>
                      <button class="add-to-cart-main"
                              onclick="changeQty('Kerchiefs (1 dozen)',130,1)">Add to Cart</button>
                    </div>
                  </div>

                </div>

                <div style="margin-top:16px;">
                  <a href="/cart" class="small-cta upi-btn">Open Cart / Payment Page</a>
                </div>

              </div>
            </div>
          </div>

          <footer>
            © Vadivelu Fabric Company • Premium Lungi & Textile Manufacturers
          </footer>

          {profile_script}
          {products_script}
        </div>
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- CART PAGE (PAYMENT DETAILS + EMAIL FORM) ----------------
@app.get("/cart", response_class=HTMLResponse)
def cart_page():
    upi_uri = "upi://pay?pa=9976791919@ybl&pn=Vadivelu%20Fabric%20Company&cu=INR"
    qr_data = upi_uri
    qr_src = f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&data={qr_data}"

    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Cart & Payment - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}

          <div class="section">
            <h2>Cart & Payment</h2>
            <p>Review your cart items and complete payment using UPI / Google Pay. Then send your order details on WhatsApp and finally submit the payment confirmation form.</p>

            <div class="cart-bar">
              <div class="cart-bar-top">
                <div><b>Cart Items:</b> <span id="cart-count-page">0</span></div>
                <div class="cart-summary-total"><b>Total Amount:</b> <span id="cart-total-page">₹0</span></div>
              </div>
              <div class="cart-note">
                These items are taken from your cart on the products page. If you want to change quantity,
                go back to <a href="/products" style="color:#facc15;text-decoration:underline;">All Products</a>.
              </div>
              <ul id="cart-items-page" class="cart-items-list"></ul>

              <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
                <button id="share-whatsapp" class="small-cta whatsapp-btn">Share Order on WhatsApp</button>
              </div>
            </div>

            <div class="section" style="margin-top:18px; padding:18px;">
              <h3 style="margin-top:0;">UPI / Google Pay (Scan or Tap)</h3>
              <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;">
                <img id="upi-qr" src="{qr_src}" alt="UPI QR"
                     style="width:160px;border-radius:12px;border:1px solid rgba(148,163,184,0.35);" />
                <div>
                  <p style="margin:0 0 8px;">UPI ID: <b>9976791919@ybl</b></p>
                  <p style="margin:0 0 8px;">Payee Name: <b>Vadivelu Fabric Company</b></p>
                  <a href="{upi_uri}" class="small-cta upi-btn" style="margin-right:8px;">Open UPI App</a>
                  <button id="copy-upi-id" class="small-cta copy-btn">Copy UPI ID</button>
                </div>
              </div>
              <p style="margin-top:12px;font-size:13px;color:#facc15;">
                After payment, please share payment screenshot + order message with us on WhatsApp at <b>+91 99767 91919</b>.
              </p>
            </div>

            <div class="section" style="margin-top:18px; padding:18px;">
              <h3 style="margin-top:0;">Payment Confirmation Form (Send Email to Company)</h3>
              <p style="font-size:13px;">
                After completing UPI payment, tick the checkbox below. Then the form will appear.
                Fill the details and submit to send a confirmation mail with your cart details and total bill.
              </p>

              <label style="font-size:13px;display:flex;align-items:center;gap:8px;margin-top:10px;">
                <input type="checkbox" id="payment-done-checkbox" />
                <span>I have completed the UPI / Google Pay payment.</span>
              </label>

              <div id="payment-form-wrapper" style="display:none;margin-top:14px;">
                <form method="post" action="/cart/checkout" id="checkout-form">
                  <div class="form-field">
                    <input name="customer_name" placeholder="Your Name" required />
                  </div>
                  <div class="form-field">
                    <input name="customer_phone" placeholder="Your Phone / WhatsApp Number" required />
                  </div>
                  <div class="form-field">
                    <textarea name="customer_address" placeholder="Full Address (Door No, Street, Area, City, District, Pincode)" required></textarea>
                  </div>
                  <div class="form-field">
                    <input type="email" name="customer_email" placeholder="Your Email (mandatory)" required />
                  </div>

                  <!-- Hidden fields auto-filled by JS renderCart() -->
                  <input type="hidden" id="cart_summary" name="cart_summary" />
                  <input type="hidden" id="cart_total" name="cart_total" />
                  <!-- hidden flag that indicates payment checkbox was ticked; client sets this when checkbox is checked -->
                  <input type="hidden" id="payment_confirmed" name="payment_confirmed" value="no" />

                  <button type="submit" class="small-cta upi-btn">Submit Payment Confirmation</button>
                </form>
              </div>
            </div>

          </div>

          <footer>
            © Vadivelu Fabric Company • Cart & Payment
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- CART CHECKOUT (SEND EMAIL) ----------------
@app.post("/cart/checkout", response_class=HTMLResponse)
def cart_checkout(
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    customer_email: str = Form(...),
    cart_summary: str = Form(""),
    cart_total: int = Form(0),
    payment_confirmed: str = Form("no")
):
    # Server-side enforcement: payment must be confirmed and cart_total must be positive
    if (not payment_confirmed) or payment_confirmed.lower() != "yes" or cart_total <= 0:
        status_text = "Payment NOT confirmed or cart is empty. Please complete the UPI payment, tick the checkbox, and try again."
        html = f"""
        <html>
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Payment Confirmation - Vadivelu Fabric Company</title>
            {base_style}
          </head>
          <body class="theme-dark">
            <div class="page-wrapper">
              {header_html()}
              <div class="section">
                <h2>Payment Not Confirmed</h2>
                <p style="color:#f87171;">{status_text}</p>

                <p style="margin-top:12px;font-size:13px;">
                  Make sure you have completed the UPI / Google Pay payment, then tick the checkbox on the cart page
                  and submit the confirmation form. If you already paid, please re-open the cart page and ensure the
                  checkbox is selected before submitting.
                </p>

                <p style="margin-top:12px;">
                  <a href="/cart" class="small-cta upi-btn">Back to Cart</a>
                </p>
              </div>
              <footer>
                © Vadivelu Fabric Company • Payment Confirmation
              </footer>
            </div>
            {profile_script}
            {products_script}
          </body>
        </html>
        """
        return HTMLResponse(html)

    # If payment confirmed, attempt to send email
    mail_ok = send_order_mail(
        name=customer_name,
        phone=customer_phone,
        customer_email=customer_email,
        customer_address=customer_address,
        cart_summary=cart_summary,
        cart_total=cart_total,
    )

    status_text = "Email sent successfully to the company." if mail_ok else (
        "Order saved, but email could not be sent (check SMTP settings on the server)."
    )

    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Payment Confirmation - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h2>Thank You, {customer_name}!</h2>
            <p>Your payment confirmation has been submitted.</p>
            <p><b>Phone / WhatsApp:</b> {customer_phone}</p>
            <p><b>Email:</b> {customer_email}</p>
            <p><b>Address:</b> {customer_address}</p>
            <p><b>Total Bill:</b> ₹{cart_total}</p>

            <h3 style="margin-top:16px;">Cart Summary</h3>
            <pre style="background:#020617;padding:10px;border-radius:8px;border:1px solid rgba(148,163,184,0.4);font-size:13px;white-space:pre-wrap;">{cart_summary}</pre>

            <p style="margin-top:12px;font-size:13px;color:#facc15;">
              {status_text}
            </p>

            <p style="margin-top:12px;font-size:13px;">
              You can also directly message us on WhatsApp at <b>+91 99767 91919</b> with your payment screenshot.
            </p>

            <p style="margin-top:12px;">
              <a href="/products" class="small-cta upi-btn">Back to Products</a>
            </p>
          </div>
          <footer>
            © Vadivelu Fabric Company • Payment Confirmation
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- CONTACT ----------------
@app.get("/contact", response_class=HTMLResponse)
def contact_page():
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Contact - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h2>Contact Us</h2>
            <p>If you are a dealer, wholesaler or retailer, contact us for bulk order details and latest designs.</p>
            <p><b>Phone:</b> +91 99767 91919</p>
            <p><b>Email:</b> amvadivelu@gmail.com</p>
            <p><b>WhatsApp / Google Pay Number:</b> +91 99767 91919</p>

            <form method="post" action="/contact">
              <div class="form-field">
                <input name="name" placeholder="Your Name" required />
              </div>
              <div class="form-field">
                <input name="email" placeholder="Email / WhatsApp Number" required />
              </div>
              <div class="form-field">
                <textarea name="message" placeholder="Your enquiry (product, quantity, location)" required></textarea>
              </div>
              <button type="submit" class="small-cta upi-btn">Send Enquiry</button>
            </form>
          </div>
          <footer>
            Vadivelu Fabric Company • Ayakkatur Alampalayam, Erode District, Tamil Nadu • Phone: +91 99767 91919
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


@app.post("/contact", response_class=HTMLResponse)
def contact_submit(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Thank You - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h2>Thank You, {name}!</h2>
            <p>We have received your enquiry:</p>
            <p style="font-size:13px;border-left:3px solid #facc15;padding-left:10px;">{message}</p>
            <p>Our team will contact you on <b>{email}</b> with product and price details.</p>
            <p>You can also message us directly on WhatsApp at <b>+91 99767 91919</b>.</p>
          </div>
          <footer>
            © Vadivelu Fabric Company • All rights reserved.
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- ABOUT ----------------
@app.get("/about", response_class=HTMLResponse)
def about_page():
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>About - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h2>About Our Company</h2>

            <p><b>Company Name:</b> Vadivelu Fabric Company</p>
            <p><b>Owner / Proprietor:</b> AM. VADIVELU</p>
            <p><b>Established:</b> Since 1988</p>
            <p><b>Industry:</b> Wholesale & Retail Lungis, Home Textiles</p>
            <p><b>Employees:</b> 101 – 500</p>
            <p><b>Annual Turnover:</b> 5 – 25 Crores</p>
            <p><b>GST Number:</b> 33AFWPV3836J1ZO</p>

            <h3 class="hero-highlight">Product Range</h3>
            <ul>
              <li>Lungi – Premium Quality (₹170)</li>
              <li>Lungi – Super Quality (₹130)</li>
              <li>Lungi – Budget Friendly Quality (₹110)</li>
              <li>Lungi – Dobby Quality (₹170)</li>
              <li>Towels (₹120)</li>
              <li>Bedspreads (₹100)</li>
              <li>Kerchiefs – 1 dozen (₹130)</li>
            </ul>

            <h3 class="hero-highlight">Location</h3>
            <p><b>Address:</b> 6-2-8-D1-1A Ayakkatur Alampalayam, Tamil Nadu, 638007</p>
            <p><b>District:</b> Erode District</p>

            <h3 class="hero-highlight">Contact Details</h3>
            <p><b>Phone:</b> +91 99767 91919</p>
            <p><b>Email:</b> amvadivelu@gmail.com</p>
            <p><b>Google Pay / UPI & WhatsApp:</b> +91 99767 91919</p>

            <p style="margin-top:15px;font-size:13px;">
              Vadivelu Fabric Company is a family-owned textile unit with more than three decades of
              experience in South Indian lungi manufacturing. We focus on consistent fabric quality,
              colour fastness and timely delivery, building long-term relationships with dealers
              and retailers across India.
            </p>
            <p style="margin-top:8px;font-size:13px;">
              Payment for orders can be made directly through the app using all bank cards and UPI transactions.
              Google Pay / UPI and WhatsApp payment options are available on <b>+91 99767 91919</b>.
            </p>
          </div>
          <footer>
            © Vadivelu Fabric Company • Since 1988 • GST: 33AFWPV3836J1ZO • Phone: +91 99767 91919
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- PROFILE ----------------
@app.get("/profile", response_class=HTMLResponse)
def profile_page():
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>My Profile - Vadivelu Fabric Company</title>
        {base_style}
      </head>
      <body class="theme-dark">
        <div class="page-wrapper">
          {header_html()}
          <div class="section">
            <h2>My Profile</h2>
            <p>This section can be extended later with login / registration and saved addresses.</p>

            <p style="font-size:13px;margin-top:10px;">
              Use the <b>Profile</b> button on the top-right to open:
            </p>
            <ul>
              <li>Home (main store front)</li>
              <li>Products (full catalogue with cart)</li>
              <li>Cart & Payment</li>
              <li>About Company</li>
              <li>Contact</li>
            </ul>

            <p style="margin-top:12px;font-size:13px;">
              For bulk orders or dealership enquiries, visit the
              <a href="/contact" style="color:#facc15;text-decoration:underline;">Contact</a> page
              or WhatsApp directly to <b>+91 99767 91919</b>.
            </p>
          </div>
          <footer>
            © Vadivelu Fabric Company • My Profile • Phone: +91 99767 91919
          </footer>
        </div>
        {profile_script}
        {products_script}
      </body>
    </html>
    """
    return HTMLResponse(html)


# ---------------- RUN DIRECTLY ----------------
if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
