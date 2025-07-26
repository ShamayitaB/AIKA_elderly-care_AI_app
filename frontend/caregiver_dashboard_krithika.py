import streamlit as st
from PIL import Image
import base64
import pandas as pd
import geopy.distance
import datetime
import random

# --- User Database ---
USERS = {
    "elderly": {"password": "123", "role": "elderly"},
    "volunteer": {"password": "123", "role": "volunteer"},
    "caregiver": {"password": "123", "role": "caregiver"},
    "lovedone": {"password": "123", "role": "lovedone"},
}

# --- Load Background Image as Base64 ---
def set_login_background(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        .login-box {{
            background-color: rgba(255, 255, 255, 0.00);
            padding: 30px;
            border-radius: 15px;
            max-width: 400px;
            margin: 100px auto;
            text-align: center;
        }}
        input {{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#Personal Information
def personal_information():
    st.subheader("👤 Personal Information")
    
    # Basic info in a styled container
    st.markdown("""
        <style>
        .info-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #4CAF50;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Personal details
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Details")
        st.markdown("**Name:** Ramesh Krishnan")
        st.markdown("**Age:** 72 years")
        st.markdown("**Gender:** Male")
        st.markdown("**Blood Group:** O+")
        st.markdown("**Date of Birth:** 15-03-1953")
        
    with col2:
        st.markdown("#### Contact Information")
        st.markdown("**Mobile:** +91 98765 43210")
        st.markdown("**Email:** ramesh.k@gmail.com")
        st.markdown("**Emergency Contact:** +91 87654 32109")
        st.markdown("**Aadhaar No:** XXXX-XXXX-7890")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Address information
    st.markdown("#### 🏠 Residential Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Address:** 45, Gandhi Street, Adyar")
        st.markdown("**City:** Chennai")
        st.markdown("**State:** Tamil Nadu")
        st.markdown("**PIN Code:** 600020")
        
    with col2:
        st.markdown("**Region:** South Chennai")
        st.markdown("**Landmark:** Near Apollo Hospital")
        st.markdown("**Residence Type:** Own")
        st.markdown("**Years at Address:** 23")
    
    # Family information
    st.markdown("#### 👪 Family Information")
    
    family_data = [
        {
            "name": "Lakshmi Krishnan", 
            "relation": "Wife", 
            "age": 68, 
            "contact": "+91 98765 43211",
            "location": "Chennai (Same Address)"
        },
        {
            "name": "Priya Suresh", 
            "relation": "Daughter", 
            "age": 45, 
            "contact": "+91 87654 32109",
            "location": "Bengaluru"
        },
        {
            "name": "Karthik Krishnan", 
            "relation": "Son", 
            "age": 42, 
            "contact": "+91 76543 21098",
            "location": "USA"
        }
    ]
    
    for member in family_data:
        with st.expander(f"{member['name']} ({member['relation']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Age:** {member['age']} years")
                st.write(f"**Contact:** {member['contact']}")
            with col2:
                st.write(f"**Location:** {member['location']}")
                if member['relation'] == "Daughter":
                    st.write("**Role:** Local Guardian")
    
    # Local Guardian
    st.markdown("#### 🛡️ Local Guardian")
    st.info("**Priya Suresh (Daughter)** is designated as local guardian and will be notified of all emergencies.")
    
    # Area supervisor
    st.markdown("#### 👥 Area Support Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Area Supervisor:** Lakshmi Narayan")
        st.markdown("**Contact:** +91 9876543211")
        st.markdown("**Response Time:** ~15 minutes")
    
    with col2:
        st.markdown("**Nearby Facility:** Apollo Hospitals")
        st.markdown("**Emergency Services:** 108")
        st.markdown("**Police Station:** Adyar (044-24547878)")
    
    # Medical information
    st.markdown("#### 🏥 Medical Information")
    
    medical_conditions = {
        "Diabetes Type 2": "Since 2010",
        "Hypertension": "Since 2008",
        "Arthritis": "Since 2015"
    }
    
    if medical_conditions:
        st.write("**Existing Medical Conditions:**")
        for condition, duration in medical_conditions.items():
            st.write(f"- {condition} ({duration})")
    else:
        st.write("**Existing Medical Conditions:** None")
    
    # Doctor information
    st.markdown("#### 👨‍⚕️ Primary Doctor Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Doctor:** Dr. Anita Sharma")
        st.markdown("**Specialization:** General Medicine")
        st.markdown("**Hospital:** Apollo Hospitals, Chennai")
    
    with col2:
        st.markdown("**Contact:** +91 44 28293333")
        st.markdown("**Last Visit:** March 15, 2025")
        st.markdown("**Next Appointment:** May 12, 2025")
    
    # Allergies and preferences
    st.markdown("#### ⚠️ Allergies & Special Considerations")
    
    allergies = ["Penicillin", "Peanuts"]
    if allergies:
        st.write("**Allergies:**")
        for allergy in allergies:
            st.write(f"- {allergy}")
    else:
        st.write("**Allergies:** None")
    
    st.write("**Dietary Restrictions:** Vegetarian, Low Sugar")
    st.write("**Special Needs:** Reading glasses, Walking stick")

# --- Volunteer Connect Feature ---
import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import random

def volunteer_connect():
    st.subheader("🤝 Connect with Nearby Volunteers")

    # --------------------------
    # Step 1: Chennai Regions & Coordinates
    # --------------------------
    CHENNAI_REGIONS = {
        "North Chennai": (13.1477, 80.2859),
        "South Chennai": (12.9507, 80.2047),
        "East Chennai": (13.0827, 80.2707),
        "West Chennai": (13.0477, 80.1831),
        "Central Chennai": (13.0802, 80.2838)
    }

    # --------------------------
    # Step 2: User Region Selection
    # --------------------------
    selected_region = st.selectbox("📍 Select your area in Chennai", list(CHENNAI_REGIONS.keys()))
    current_coords = CHENNAI_REGIONS[selected_region]

    # --------------------------
    # Step 3: Region Supervisors
    # --------------------------
    SUPERVISORS = {
        "North Chennai": {"name": "Rajesh Kumar", "phone": "+91 9876543210"},
        "South Chennai": {"name": "Lakshmi Narayan", "phone": "+91 9876543211"},
        "East Chennai": {"name": "Priya Venkatesh", "phone": "+91 9876543212"},
        "West Chennai": {"name": "Karthik Raman", "phone": "+91 9876543213"},
        "Central Chennai": {"name": "Meena Sundaram", "phone": "+91 9876543214"}
    }
    
    current_supervisor = SUPERVISORS[selected_region]
    
    # Display supervisor info
    st.info(f"📢 **Area Supervisor:** {current_supervisor['name']} ({current_supervisor['phone']})")
    st.caption("The supervisor will be notified of all emergency requests in this area")

    # --------------------------
    # Step 4: Volunteers Data (5 per region)
    # --------------------------
    REGION_VOLUNTEERS = {
        "North Chennai": [
            {"name": "Aditya Sharma", "distance": 1.2, "status": "Available"},
            {"name": "Divya Krishnan", "distance": 1.8, "status": "Available"},
            {"name": "Mohammed Imran", "distance": 2.5, "status": "Busy"},
            {"name": "Kavitha Suresh", "distance": 3.1, "status": "Available"},
            {"name": "Ravi Shankar", "distance": 3.7, "status": "Offline"}
        ],
        "South Chennai": [
            {"name": "Sridevi Nair", "distance": 0.8, "status": "Available"},
            {"name": "Arjun Menon", "distance": 1.5, "status": "Busy"},
            {"name": "Lakshmi Prasad", "distance": 2.0, "status": "Available"},
            {"name": "Venkat Raman", "distance": 2.8, "status": "Available"},
            {"name": "Amrita Pillai", "distance": 3.2, "status": "Offline"}
        ],
        "East Chennai": [
            {"name": "Gayathri Venkatesan", "distance": 1.0, "status": "Available"},
            {"name": "Abdul Raheem", "distance": 1.7, "status": "Available"},
            {"name": "Saranya Kumar", "distance": 2.3, "status": "Available"},
            {"name": "Vishnu Prasad", "distance": 2.9, "status": "Busy"},
            {"name": "Fathima Begum", "distance": 3.5, "status": "Offline"}
        ],
        "West Chennai": [
            {"name": "Suresh Narayanan", "distance": 0.5, "status": "Available"},
            {"name": "Anitha Devan", "distance": 1.2, "status": "Available"},
            {"name": "Joseph Mathew", "distance": 1.9, "status": "Busy"},
            {"name": "Geetha Krishnan", "distance": 2.6, "status": "Available"},
            {"name": "Prakash Raj", "distance": 3.0, "status": "Offline"}
        ],
        "Central Chennai": [
            {"name": "Ramya Subramanian", "distance": 0.7, "status": "Available"},
            {"name": "Vijay Kumar", "distance": 1.4, "status": "Available"},
            {"name": "Shobana Ravi", "distance": 2.1, "status": "Available"},
            {"name": "Dinesh Babu", "distance": 2.7, "status": "Busy"},
            {"name": "Latha Menon", "distance": 3.3, "status": "Offline"}
        ]
    }
    
    volunteers = REGION_VOLUNTEERS[selected_region]
    
    # Sort volunteers by distance
    sorted_volunteers = sorted(volunteers, key=lambda x: x["distance"])

    # --------------------------
    # Step 5: Emergency Button
    # --------------------------
    st.warning("🚨 In case of emergency, click below to notify all nearby volunteers.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Emergency Broadcast"):
            st.success(f"📢 Emergency alert sent to all volunteers and supervisor {current_supervisor['name']} in {selected_region}!")
    
    with col2:
        help_type = st.selectbox("Select type of help needed:", [
            "Medical Emergency", 
            "Fall Assistance", 
            "Medication Help", 
            "Transportation", 
            "Grocery/Food", 
            "Other"
        ])

    # --------------------------
    # Step 6: Show Matched Volunteers
    # --------------------------
    st.markdown("### 👥 Available Volunteers Near You")
    
    # Generate some random coordinates around the region center
    import random
    
    # Create map data with volunteer positions
    map_data = []
    
    for vol in sorted_volunteers:
        color_icon = {"Available": "🟢", "Busy": "🟡", "Offline": "🔴"}
        eta = round((vol["distance"] / 5) * 60)  # assuming 5 km/hr walking speed
        
        # Random slight variation for map display
        lat_offset = random.uniform(-0.01, 0.01)
        lon_offset = random.uniform(-0.01, 0.01)
        vol_lat = current_coords[0] + lat_offset
        vol_lon = current_coords[1] + lon_offset
        
        map_data.append({"lat": vol_lat, "lon": vol_lon})
        
        if vol["status"] != "Offline":
            with st.expander(f"👤 {vol['name']} ({vol['status']}) - {vol['distance']} km away"):
                st.write(f"{color_icon[vol['status']]} Status: **{vol['status']}**")
                st.write(f"📍 Distance: **{vol['distance']} km**")
                st.write(f"🕒 Estimated arrival time: **{eta} minutes**")
                
                # Add phone with randomly generated number
                phone = f"+91 9{random.randint(100000000, 999999999)}"
                st.write(f"📞 Contact: {phone}")
                
                # Skills/Services
                skills = random.sample([
                    "First Aid Certified", "Medical Background", "Driver", 
                    "Cooking", "Heavy Lifting", "Medication Management"
                ], k=random.randint(1, 3))
                
                st.write("🛠️ **Skills:** " + ", ".join(skills))
                
                # Help request button
                if st.button(f"📢 Request Help – {vol['name']}", key=vol['name']):
                    arrival_time = f"{eta} minutes"
                    st.success(f"✅ Help request sent to {vol['name']}!")
                    st.info(f"💬 Message from {vol['name']}: I will be arriving in approximately {arrival_time}")
                    
                    # Rating system appears after help request
                    st.markdown("📝 *After assistance is complete, please rate:*")
                    st.slider(f"Rate {vol['name']}'s assistance (1-5)", 1, 5, key=f"rating_{vol['name']}")

    # --------------------------
    # Step 7: Show Volunteers on Map
    # --------------------------
    st.markdown("### 🗺️ Volunteers in Your Area")
    
    # Add user position (slightly randomized around region center)
    user_lat = current_coords[0] + random.uniform(-0.003, 0.003)
    user_lon = current_coords[1] + random.uniform(-0.003, 0.003)
    
    # Add supervisor position
    sup_lat = current_coords[0] + random.uniform(-0.02, 0.02)
    sup_lon = current_coords[1] + random.uniform(-0.02, 0.02)
    
    # Create final map dataframe
    map_df = pd.DataFrame(map_data + [{"lat": user_lat, "lon": user_lon}, {"lat": sup_lat, "lon": sup_lon}])
    
    st.map(map_df)
    st.caption("📍 Blue markers show volunteer locations. Your location is also shown on the map.")
    
    # Additional region information
    st.markdown("### 📊 Region Information")
    st.write(f"**{selected_region}** has **{sum(1 for v in volunteers if v['status'] == 'Available')}** available volunteers right now")
    st.write(f"Average response time in this area: **{random.randint(8, 15)} minutes**")
    st.write(f"Most common service requests in {selected_region}: Medical Assistance, Transportation")

# --- Login Page ---
def login():
    set_login_background(r"C:\Users\Shamayita Biswas\OneDrive\Desktop\Projects\3rd yr project\aika_trial\frontend\background_new_img.jpg")

    st.markdown("""
        <style>
        .login-header {
            color: black;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 40px;
            text-align: center;
            font-weight: bold;
            font-size: 28px;
        }
        
        /* Style for input field labels */
        .stTextInput label {
            color: black !important;
            background-color: rgba(255, 255, 255, 0.7) !important;
            padding: 5px 10px !important;
            border-radius: 5px !important;
            font-weight: bold !important;
        }
        
        /* Style for input fields */
        .stTextInput input {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid #4B4B4B !important;
            color: black !important;
            font-weight: 500 !important;
        }
        
        /* Style for login button */
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    # Centered header with background padding for visibility
    st.markdown('<div class="login-header">🧓 AIKA – An Elderly Care App</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = user["role"]
        else:
            st.error("❌ Invalid username or password")

    st.markdown('</div>', unsafe_allow_html=True)

def medicine_reminders():
    st.subheader("📋 Medicine & Medical Records")
    
    # Patient info in a card-like container
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Instead of using a placeholder URL, use a colored box with text
            st.markdown("""
                <div style="background-color:#f0f0f0; width:120px; height:120px; 
                border-radius:10px; display:flex; align-items:center; justify-content:center; 
                text-align:center; color:#555; font-size:14px;">
                    Patient Photo<br>(Not Available)
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Patient: Ramesh Krishnan")
            st.markdown("**Age:** 72 years")
            st.markdown("**Blood Group:** O+")
            st.markdown("**Primary Doctor:** Dr. Anita Sharma")
            st.markdown("**Hospital:** Apollo Hospitals, Chennai")
    
    
    # Checkup dates
    st.markdown("### 🏥 Medical Appointments")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Last Checkup:** March 15, 2025")
    with col2:
        st.warning("**Next Appointment:** May 12, 2025 (in 31 days)")
    
    # Prescription view option
    st.markdown("### 📝 Prescriptions")
    tabs = st.tabs(["Current Prescription", "Previous Prescriptions"])
    
    with tabs[0]:
        st.markdown("**Prescribed on:** March 15, 2025")
        if st.button("View Prescription Document"):
            st.markdown("![Prescription](https://via.placeholder.com/600x400?text=Prescription+Document)")
            st.download_button("Download Prescription", "prescription_data", "prescription_march_2025.pdf")
    
    with tabs[1]:
        previous_prescriptions = {
            "February 10, 2025": "Dr. Anita Sharma - Apollo Hospitals",
            "December 22, 2024": "Dr. Vikram Mehta - Apollo Hospitals",
            "October 5, 2024": "Dr. Anita Sharma - Apollo Hospitals"
        }
        
        for date, doctor in previous_prescriptions.items():
            with st.expander(f"Prescription - {date}"):
                st.write(f"**Doctor:** {doctor}")
                st.button("View Document", key=f"view_{date}")
    
    # Medicine schedule
    st.markdown("### 💊 Medicine Schedule")
    
    medicine_data = [
        {"name": "Telma 40", "morning": True, "afternoon": False, "evening": True, "quantity": "1 tablet", "purpose": "Blood Pressure"},
        {"name": "Ecosprin 75", "morning": True, "afternoon": False, "evening": False, "quantity": "1 tablet", "purpose": "Blood Thinner"},
        {"name": "Glycomet 500", "morning": True, "afternoon": True, "evening": True, "quantity": "1 tablet", "purpose": "Diabetes"},
        {"name": "Calcitrol D3", "morning": False, "afternoon": False, "evening": True, "quantity": "1 capsule", "purpose": "Vitamin D Supplement"},
        {"name": "B-Complex Forte", "morning": True, "afternoon": False, "evening": False, "quantity": "1 tablet", "purpose": "Vitamin Supplement"}
    ]
    
    # Color-coded medicine table
    for med in medicine_data:
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        
        col1.write(f"**{med['name']}**")
        
        morning_status = "✅" if med["morning"] else "❌"
        afternoon_status = "✅" if med["afternoon"] else "❌"
        evening_status = "✅" if med["evening"] else "❌"
        
        col2.write(f"Morning: {morning_status}")
        col3.write(f"Afternoon: {afternoon_status}")
        col4.write(f"Evening: {evening_status}")
        col5.write(f"{med['quantity']} - {med['purpose']}")
        
        # Show adherence monitoring
        adherence = random.choice(["High", "Medium", "Low"])
        adherence_color = {"High": "green", "Medium": "orange", "Low": "red"}
        st.markdown(f"<div style='height:8px; background-color:{adherence_color[adherence]}; margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    # Upcoming reminders
    st.markdown("### ⏰ Today's Reminders")
    current_hour = datetime.datetime.now().hour
    
    if current_hour < 12:
        st.success("🔔 **9:00 AM** - Take morning medications (Telma 40, Ecosprin 75, Glycomet 500, B-Complex)")
    elif current_hour < 16:
        st.success("🔔 **2:00 PM** - Take afternoon medication (Glycomet 500)")
    else:
        st.success("🔔 **8:00 PM** - Take evening medications (Telma 40, Glycomet 500, Calcitrol D3)")# --- Elderly Dashboard ---
def elderly_dashboard():
    st.markdown(
        """
        <style>
        .stApp {
            background: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("👵 Elderly Dashboard")

    option = st.sidebar.selectbox("Choose an option", [
        "Personal Information",  # New option
        "Connect with Volunteers",
        "Medicine Reminders",
        "Contact Loved Ones",
        "Health Alerts",
        "Health Record History"
    ])

    if option == "Personal Information":
        personal_information()
    
    elif option == "Connect with Volunteers":
        volunteer_connect()

    elif option == "Medicine Reminders":
        medicine_reminders()

    elif option == "Contact Loved Ones":
        contact_loved_ones()

    elif option == "Health Alerts":
        st.subheader("Recent Alerts")
        st.write("✅ No recent falls detected.")
        st.write("✅ Heart rate stable.")

    elif option == "Health Record History":
        st.subheader("📊 Health Data (Last 30 Days)")
        df = pd.DataFrame({
            'Date': pd.date_range(start='2025-04-01', periods=30),
            'BP': [120 + (i % 5) for i in range(30)],
            'Heart Rate': [72 + (i % 3) for i in range(30)],
            'Steps': [1500 + (i * 20) for i in range(30)],
        })
        st.dataframe(df)

def contact_loved_ones():
    st.subheader("👪 Connect with Family & Loved Ones")
    
    # Contact list with family members
    family_contacts = [
        {
            "name": "Priya Suresh",
            "relation": "Daughter", 
            "photo": "daughter_photo.jpg",
            "phone": "+91 87654 32109",
            "last_contact": "Yesterday at 7:30 PM",
            "reminder": "Visiting on Sunday at 11 AM"
        },
        {
            "name": "Karthik Krishnan",
            "relation": "Son", 
            "photo": "son_photo.jpg",
            "phone": "+91 76543 21098",
            "last_contact": "April 8, 2025",
            "reminder": "Video call scheduled for tomorrow at 9 PM"
        },
        {
            "name": "Lakshmi Krishnan",
            "relation": "Wife", 
            "photo": "wife_photo.jpg",
            "phone": "+91 98765 43211",
            "last_contact": "Today at 10:00 AM",
            "reminder": None
        },
        {
            "name": "Deepa Sundaram",
            "relation": "Sister", 
            "photo": "sister_photo.jpg",
            "phone": "+91 65432 10987",
            "last_contact": "March 30, 2025",
            "reminder": "Birthday on April 22"
        },
        {
            "name": "Dr. Anita Sharma",
            "relation": "Doctor", 
            "photo": "doctor_photo.jpg",
            "phone": "+91 44 28293333",
            "last_contact": "March 15, 2025",
            "reminder": "Next appointment: May 12, 2025"
        }
    ]
    
    # Display upcoming reminders at the top
    st.markdown("### 📅 Upcoming Family Reminders")
    upcoming_reminders = [contact for contact in family_contacts if contact["reminder"]]
    
    if upcoming_reminders:
        for contact in upcoming_reminders:
            st.info(f"🔔 **{contact['name']}** ({contact['relation']}): {contact['reminder']}")
    else:
        st.write("No upcoming reminders")
    
    # Quick action buttons for most frequent contacts
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Call Daughter"):
            st.success("📱 Calling Priya (Daughter)...")
            st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/telephone_ring.wav", format="audio/wav")
    
    with col2:
        if st.button("📹 Video Call Son"):
            st.success("🎥 Starting video call with Karthik (Son)...")
    
    with col3:
        if st.button("🆘 Emergency Alert"):
            st.error("🚨 Emergency alert sent to all family members!")
    
    # Contact list with actions
    st.markdown("### 📒 Contact List")
    
    for contact in family_contacts:
        with st.expander(f"👤 {contact['name']} • {contact['relation']}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Display a placeholder if photo not available
                st.markdown("""
                    <div style="background-color:#f0f0f0; width:80px; height:80px; 
                    border-radius:50%; display:flex; align-items:center; justify-content:center; 
                    text-align:center; color:#555; font-size:10px;">
                        Photo
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write(f"**Phone:** {contact['phone']}")
                st.write(f"**Last Contact:** {contact['last_contact']}")
                if contact["reminder"]:
                    st.write(f"**Reminder:** {contact['reminder']}")
            
            # Action buttons
            action_col1, action_col2, action_col3 = st.columns(3)
            
            with action_col1:
                if st.button(f"📞 Call", key=f"call_{contact['name']}"):
                    st.success(f"📱 Calling {contact['name']}...")
            
            with action_col2:
                if st.button(f"💬 Message", key=f"msg_{contact['name']}"):
                    st.text_area(f"Message to {contact['name']}", key=f"text_{contact['name']}")
                    if st.button(f"Send", key=f"send_{contact['name']}"):
                        st.success(f"✅ Message sent to {contact['name']}!")
            
            with action_col3:
                if st.button(f"📹 Video", key=f"video_{contact['name']}"):
                    st.success(f"🎥 Starting video call with {contact['name']}...")
    
    # Send new message section
    st.markdown("### 💬 Send New Message")
    
    recipient = st.selectbox("Select recipient", [f"{c['name']} ({c['relation']})" for c in family_contacts])
    message_type = st.radio("Message type", ["Text", "Voice", "Photo"])
    
    if message_type == "Text":
        message = st.text_area("Type your message")
        if st.button("Send Message"):
            if message:
                st.success(f"✅ Message sent to {recipient}!")
            else:
                st.warning("Please type a message before sending")
    
    elif message_type == "Voice":
        st.write("🎙️ Click and hold to record voice message")
        if st.button("Start Recording"):
            st.info("🎙️ Recording... (Simulated)")
            if st.button("Stop and Send"):
                st.success(f"✅ Voice message sent to {recipient}!")
    
    elif message_type == "Photo":
        st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"])
        if st.button("Send Photo"):
            st.success(f"✅ Photo sent to {recipient}!")
    
    # View messages section
    st.markdown("### 📨 Recent Messages")
    
    recent_messages = [
        {"from": "Priya Suresh (Daughter)", "time": "Yesterday, 7:30 PM", "content": "Hi Dad, just checking in. How are you feeling today?"},
        {"from": "You", "time": "Yesterday, 7:45 PM", "content": "I'm doing well, thank you. The new medicine is working well."},
        {"from": "Karthik Krishnan (Son)", "time": "April 8, 2:15 PM", "content": "Dad, remember we have a video call tomorrow evening. I want to show you your grandkids' new school project!"},
        {"from": "Dr. Anita Sharma (Doctor)", "time": "April 5, 10:20 AM", "content": "Mr. Krishnan, please remember to take your blood pressure readings daily and note them down for our next appointment."}
    ]
    
    for msg in recent_messages:
        if msg["from"] == "You":
            st.markdown(f"""
                <div style="background-color:#dcf8c6; padding:10px; border-radius:10px; 
                margin:5px 0 5px 50px; text-align:right;">
                    <span style="font-size:12px; color:#666;">{msg["time"]}</span><br>
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background-color:#f0f0f0; padding:10px; border-radius:10px; margin:5px 50px 5px 0;">
                    <strong>{msg["from"]}</strong><br>
                    <span style="font-size:12px; color:#666;">{msg["time"]}</span><br>
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)

# Update the elderly_dashboard function to use this new contact_loved_ones function

# --- Role-based Dashboard ---
def show_dashboard(role):
    st.markdown(
        """
        <style>
        .stApp {
            background: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if role == "elderly":
        elderly_dashboard()

    elif role == "volunteer":
        st.title("Volunteer Dashboard")
        st.write("- 📍 Locate Nearby Elderly")
        st.write("- 🤝 Assist with Tasks")
        st.write("- 📅 View Activities")

    elif role == "lovedone":
        contact_loved_ones()
        
    elif role == "caregiver":
        st.title("Caregiver Dashboard")
        st.write("- ✅ Monitor All Features")
        st.write("- 📊 Elderly Health Dashboard")
        st.write("- 💬 Communicate with Volunteers & Loved Ones")

# --- Main App Logic ---
def main():
    st.set_page_config(page_title="AIKA – Elderly Care App", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None

    if not st.session_state.logged_in:
        login()
    else:
        show_dashboard(st.session_state.role)

if __name__ == "__main__":
    main()
