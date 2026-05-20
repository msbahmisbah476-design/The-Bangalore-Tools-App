import streamlit as st
from supabase import create_client
import datetime

# --- 1. CONFIGURATION & DATABASE ---
# Using the credentials from your previous setup
URL = "https://zuujdlxfqvlutlrndxol.supabase.co"
# Ensure there are no spaces inside these quotes
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp1dWpkbHhmcXZsdXRscm5keG9sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyNTEwNzgsImV4cCI6MjA5MzgyNzA3OH0.oiIfem__VrbwVQCEAfEEAGPLpVOisPs7qxnLSnQGO7Y"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="The Bangalore Tools", page_icon="🛠️", layout="wide")

# --- 2. SESSION STATE ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'user' not in st.session_state:
    st.session_state.user = ""

# --- 3. HELPER FUNCTIONS ---
def send_whatsapp_msg(target_num, message):
    """Formats a WhatsApp URL for easy clicking."""
    encoded_msg = message.replace(' ', '%20').replace('\n', '%0A')
    return f"https://wa.me/{target_num}?text={encoded_msg}"

# --- 4. LOGIN PAGE ---
if not st.session_state.auth:
    st.title("🛠️ The Bangalore Tools")
    with st.container(border=True):
        st.subheader("Customer & Staff Sign-in")
        name = st.text_input("Full Name")
        password = st.text_input("Access Password", type="password") # You can set a fixed password for customers
        
        if st.button("Enter App", use_container_width=True):
            if name:
                st.session_state.auth = True
                st.session_state.user = name
                st.rerun()
            else:
                st.error("Please enter your name to continue.")

# --- 5. MAIN APP INTERFACE ---
else:
    # --- SIDEBAR ICONS & NAVIGATION ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3062/3062413.png", width=100)
    st.sidebar.title(f"Hello, {st.session_state.user}")
    
    # Navigation logic
    menu_options = ["🏠 Home & About", "📦 Check Availability", "📝 Place Order", "🚚 Book Delivery"]
    
    # Manager Access (Dad's Dashboard)
    # If the login name matches your Dad's name from the shop board
    if st.session_state.user.lower() == "arif":
        menu_options.insert(0, "📊 MANAGER DASHBOARD")
    
    choice = st.sidebar.radio("Go to:", menu_options)
    
    st.sidebar.divider()
    st.sidebar.subheader("Quick Contact")
    # WhatsApp Query Icon/Link
    wa_query = send_whatsapp_msg("919845724046", "Hi Arif, I have a query about a tool.")
    st.sidebar.link_button("💬 Chat with Me (WhatsApp)", wa_query)
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    # --- FEATURE 1: MANAGER DASHBOARD (Private to Dad) ---
    if choice == "📊 MANAGER DASHBOARD":
        st.title("👨‍💼 Manager Control Panel")
        st.info("View current customer requirements from the database.")
        
        try:
            # Fetching from the 'Orders' table you created
            res = supabase.table("Orders").select("*").order("created_at", desc=True).execute()
            all_orders = res.data
            
            if all_orders:
                for o in all_orders:
                    with st.expander(f"Order from {o['customer_name']}"):
                        st.write(f"**Requirement:** {o['requirements']}")
                        st.caption(f"Received at: {o['created_at']}")
            else:
                st.write("No pending orders found.")
        except Exception as e:
            st.error(f"Error fetching orders: {e}")

    # --- FEATURE 2: HOME & ABOUT ---
    elif choice == "🏠 Home & About":
        st.title("THE BANGALORE TOOLS")
        st.markdown(f"""
        ### 🏭 Shop Profile
        **Suppliers of All Types Of:** 
        CNC Cutting Tools & Inserts, HSS Tools, Endmills, Instruments & Boring Tools.
        
        **📍 Shop Location:**
        #67/2 6th Main, Muthkurappa Layout, Opp. Metro Pillar #162, Garudacharpalya, Mahadevapura Post, Bengaluru-560048
        
        **📧 Business Email:** arifulla31@gmail.com
        **📞 Direct Mobile:** +91 98457 24046
        """)
        st.divider()
        st.info("💡 Note: We provide high-quality industrial tools for CNC and VMC machining.")

    # --- FEATURE 3: LIVE AVAILABILITY ---
    elif choice == "📦 Check Availability":
        st.title("📦 Tool Availability")
        st.write("Check if the materials you need are currently in stock.")
        
        # Grid view for tools
        col1, col2 = st.columns(2)
        with col1:
            st.success("✅ **CNC Inserts (CCMT/WNMG)** - In Stock")
            st.success("✅ **HSS Drills** - In Stock")
        with col2:
            st.success("✅ **Carbide Endmills (4-12mm)** - In Stock")
            st.warning("⏳ **Boring Bars** - Low Stock (Restocking)")

    # --- FEATURE 4: PLACE ORDER ---
    elif choice == "📝 Place Order":
        st.title("📝 Submit Requirement")
        order_text = st.text_area("List the tools and sizes you need:", placeholder="e.g. 10pcs CNMG Insert, 2pcs 8mm Endmill")
        
        if st.button("Submit to Shop", use_container_width=True):
            if order_text:
                try:
                    # Save to Supabase 'Orders' Table
                    payload = {"customer_name": st.session_state.user, "requirements": order_text}
                    supabase.table("Orders").insert(payload).execute()
                    st.success("✅ Order saved in shop records!")
                    
                    # Notify via WhatsApp
                    notification = f"*New Order from {st.session_state.user}:*\n{order_text}"
                    wa_url = send_whatsapp_msg("919845724046", notification)
                    st.markdown(f"**[🚀 Click to Notify me on WhatsApp]({wa_url})**")
                except Exception as e:
                    st.error(f"Database Error: {e}")
            else:
                st.error("Please enter a requirement first.")

    # --- FEATURE 5: BOOK DELIVERY ---
    elif choice == "🚚 Book Delivery":
        st.title("🚚 Delivery & Logistics")
        st.write("Once your order is ready, you can book a Porter pickup from our shop location.")
        st.link_button("🚀 Open Porter App / Website", "https://www.porter.in/")