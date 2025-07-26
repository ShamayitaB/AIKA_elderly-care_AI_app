import streamlit as st
from PIL import Image
import base64
import pandas as pd
import geopy.distance
import datetime
import requests
import random
import io
import json
import logging
import plotly.express as px
import plotly.graph_objects as go

# --- API Configuration ---
API_BASE_URL = "http://localhost:5000/api"

# --- Helper Function for API Calls ---
def make_api_request(endpoint, method="GET", data=None, headers=None):
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# --- Load Background Image ---
def set_login_background(image_path):
    try:
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
    except FileNotFoundError:
        st.warning("Background image not found. Using default background.")

# --- Personal Information ---
def personal_information():
    st.subheader("👤 Personal Information")
    
    if "user_id" not in st.session_state:
        st.error("User not logged in.")
        return
    
    # Fetch user data (includes region info)
    user_data = make_api_request(f"users/{st.session_state.user_id}")
    if not user_data:
        st.error("Failed to load personal information.")
        return
    
    # Basic info styling
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
        st.markdown(f"**Name:** {user_data.get('name', 'N/A')}")
        st.markdown(f"**Age:** {user_data.get('age', 'N/A')} years")
        st.markdown(f"**Gender:** {user_data.get('gender', 'N/A')}")
        st.markdown(f"**Blood Group:** {user_data.get('blood_group', 'N/A')}")
        st.markdown(f"**Date of Birth:** {user_data.get('dob', 'N/A')}")
        
    with col2:
        st.markdown("#### Contact Information")
        st.markdown(f"**Mobile:** {user_data.get('phone', 'N/A')}")
        st.markdown(f"**Email:** {user_data.get('email', 'N/A')}")
        st.markdown(f"**Emergency Contact:** {user_data.get('emergency_contact', 'N/A')}")
        st.markdown(f"**Aadhaar No:** {user_data.get('aadhaar_no', 'N/A')}")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Address information
    st.markdown("#### 🏠 Residential Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Address:** {user_data.get('address', 'N/A')}")
        st.markdown(f"**State:** {user_data.get('state', 'N/A')}")
        st.markdown(f"**PIN Code:** {user_data.get('pin_code', 'N/A')}")
        
    with col2:
        st.markdown(f"**Region:** {user_data.get('region_name', 'N/A')}")
        st.markdown(f"**Landmark:** {user_data.get('landmark', 'N/A')}")
        st.markdown(f"**Residence Type:** {user_data.get('residence_type', 'N/A')}")
        st.markdown(f"**Years at Address:** {user_data.get('years_at_address', 'N/A')}")
    
    # Family information
    st.markdown("#### 👪 Family Information")
    
    family_data = make_api_request(f"family-contacts/{st.session_state.user_id}")
    if family_data:
        for member in family_data:
            with st.expander(f"{member['name']} ({member['relation']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Contact:** {member.get('phone', 'N/A')}")
                with col2:
                    st.write(f"**Location:** {member.get('address', 'N/A')}")
                    if member.get('is_local_guardian'):
                        st.write("**Role:** Local Guardian")
    
    # Local Guardian
    st.markdown("#### 🛡️ Local Guardian")
    local_guardian = next((m for m in family_data if m.get('is_local_guardian')), None) if family_data else None
    if local_guardian:
        st.info(f"**{local_guardian['name']} ({local_guardian['relation']})** is designated as local guardian.")
    else:
        st.write("No local guardian assigned.")
    
    # Area supervisor
    st.markdown("#### 👥 Area Support Information")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Area Supervisor:** {user_data.get('supervisor_name', 'N/A')}")
        st.markdown(f"**Contact:** {user_data.get('supervisor_phone', 'N/A')}")
        st.markdown("**Response Time:** ~15 minutes")
    
    with col2:
        st.markdown(f"**Nearby Facility:** {user_data.get('primary_hospital', 'N/A')}")
        st.markdown("**Emergency Services:** 108")
        address= user_data.get('address','')
        police_station = address.split(',')[-1].strip() if address and ',' in address else 'N/A'
        st.markdown(f"**Police Station:** {police_station} Police Station (044-24547878)")
    
    # Medical information
    st.markdown("#### 🏥 Medical Information")
    
    medical_conditions = user_data.get('medical_conditions', {})
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
        st.markdown(f"**Doctor:** {user_data.get('primary_doctor_name', 'N/A')}")
        st.markdown("**Specialization:** General Medicine")
        st.markdown(f"**Hospital:** {user_data.get('primary_hospital', 'N/A')}")
    
    with col2:
        st.markdown(f"**Contact:** {user_data.get('primary_doctor_contact', 'N/A')}")
        st.markdown(f"**Last Visit:** {user_data.get('last_doctor_visit', 'N/A')}")
        st.markdown(f"**Next Appointment:** {user_data.get('next_appointment', 'N/A')}")
    
    # Allergies and preferences
    st.markdown("#### ⚠️ Allergies & Special Considerations")
    
    allergies = user_data.get('allergies', [])
    if allergies:
        st.write("**Allergies:**")
        for allergy in allergies:
            st.write(f"- {allergy}")
    else:
        st.write("**Allergies:** None")
    
    st.write(f"**Dietary Restrictions:** {user_data.get('dietary_restrictions', 'None')}")
    st.write(f"**Special Needs:** {user_data.get('special_needs', 'None')}")

# --- Volunteer Connect ---
def volunteer_connect():
    st.subheader("🤝 Connect with Nearby Volunteers")
    
    if "user_id" not in st.session_state:
        st.error("User not logged in.")
        return
    
    # Fetch user data (includes region info)
    user_data = make_api_request(f"users/{st.session_state.user_id}")
    if not user_data or not user_data.get('region_name'):
        st.error("Failed to load user region.")
        return
    
    selected_region = user_data['region_name']
    
    # Display supervisor info
    st.info(f"📢 **Area Supervisor:** {user_data['supervisor_name']} ({user_data['supervisor_phone']})")
    st.caption("The supervisor will be notified of all emergency requests in this area")
    
    # Fetch volunteers
    volunteers = make_api_request(f"volunteers/region/{selected_region.replace(' ', '%20')}")
    if not volunteers:
        st.error("No volunteers found.")
        return
    
    # Sort volunteers by distance
    sorted_volunteers = sorted(volunteers, key=lambda x: x["distance"])
    
    # Emergency button
    st.warning("🚨 In case of emergency, click below to notify all nearby volunteers.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Emergency Broadcast"):
            st.success(f"📢 Emergency alert sent to all volunteers and supervisor {user_data['supervisor_name']} in {selected_region}!")
    
    with col2:
        help_type = st.selectbox("Select type of help needed:", [
            "Medical Emergency", "Fall Assistance", "Medication Help",
            "Transportation", "Grocery/Food", "Other"
        ])
    
    # Show volunteers
    st.markdown("### 👥 Available Volunteers Near You")
    
    map_data = []
    for vol in sorted_volunteers:
        color_icon = {"Available": "🟢", "Busy": "🟡", "Offline": "🔴"}
        distance = float(vol["distance"]) if vol["distance"] is not None else 0.0
        eta = round((distance / 5) * 60)  # 5 km/hr walking speed
        
        # Random map coordinates
        lat_offset = random.uniform(-0.01, 0.01)
        lon_offset = random.uniform(-0.01, 0.01)
        vol_lat = user_data.get('latitude', 13.0) + lat_offset
        vol_lon = user_data.get('longitude', 80.2) + lon_offset
        map_data.append({"lat": vol_lat, "lon": vol_lon})
        
        if vol["status"] != "Offline":
            with st.expander(f"👤 {vol['name']} ({vol['status']}) - {vol['distance']} km away"):
                st.write(f"{color_icon[vol['status']]} Status: **{vol['status']}**")
                st.write(f"📍 Distance: **{vol['distance']} km**")
                st.write(f"🕒 Estimated arrival time: **{eta} minutes**")
                st.write(f"📞 Contact: {vol.get('phone', 'N/A')}")
                st.write(f"🛠️ **Skills:** {', '.join(vol.get('skills', []))}")
                
                if st.button(f"📢 Request Help – {vol['name']}", key=f"help_{vol['user_id']}"):
                    st.success(f"✅ Help request sent to {vol['name']}!")
                    st.info(f"💬 Message from {vol['name']}: I will be arriving in approximately {eta} minutes")
                    st.markdown("📝 *After assistance is complete, please rate:*")
                    st.slider(f"Rate {vol['name']}'s assistance (1-5)", 1, 5, key=f"rating_{vol['user_id']}")
    
    # Map
    st.markdown("### 🗺️ Volunteers in Your Area")
    user_lat = user_data.get('latitude', 13.0) + random.uniform(-0.003, 0.003)
    user_lon = user_data.get('longitude', 80.2) + random.uniform(-0.003, 0.003)
    sup_lat = user_data.get('latitude', 13.0) + random.uniform(-0.02, 0.02)
    sup_lon = user_data.get('longitude', 80.2) + random.uniform(-0.02, 0.02)
    
    map_df = pd.DataFrame(map_data + [
        {"lat": user_lat, "lon": user_lon},
        {"lat": sup_lat, "lon": sup_lon}
    ])
    
    st.map(map_df)
    st.caption("📍 Blue markers show volunteer locations. Your location is also shown on the map.")
    
    # Region info
    st.markdown("### 📊 Region Information")
    available_count = sum(1 for v in volunteers if v['status'] == 'Available')
    st.write(f"**{selected_region}** has **{available_count}** available volunteers right now")
    st.write(f"Average response time in this area: **{random.randint(8, 15)} minutes**")
    st.write(f"Most common service requests in {selected_region}: Medical Assistance, Transportation")

# --- Medicine Reminders ---
def medicine_reminders():
    st.subheader("📋 Medicine & Medical Records")
    
    if "user_id" not in st.session_state:
        st.error("User not logged in.")
        return
    
    # Fetch user data
    user_data = make_api_request(f"users/{st.session_state.user_id}")
    if not user_data:
        st.error("Failed to load user data.")
        return
    
    # Patient info
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
                <div style="background-color:#f0f0f0; width:120px; height:120px; 
                border-radius:10px; display:flex; align-items:center; justify-content:center; 
                text-align:center; color:#555; font-size:14px;">
                    Patient Photo<br>(Not Available)
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### Patient: {user_data.get('name', 'N/A')}")
            st.markdown(f"**Age:** {user_data.get('age', 'N/A')} years")
            st.markdown(f"**Blood Group:** {user_data.get('blood_group', 'N/A')}")
            st.markdown(f"**Primary Doctor:** {user_data.get('primary_doctor_name', 'N/A')}")
            st.markdown(f"**Hospital:** {user_data.get('primary_hospital', 'N/A')}")
    
    # Checkup dates
    st.markdown("### 🏥 Medical Appointments")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Last Checkup:** {user_data.get('last_doctor_visit', 'N/A')}")
    with col2:
        st.warning(f"**Next Appointment:** {user_data.get('next_appointment', 'N/A')}")
    
    # Prescription view (placeholder)
    st.markdown("### 📝 Prescriptions")
    tabs = st.tabs(["Current Prescription", "Previous Prescriptions"])
    
    with tabs[0]:
        st.markdown(f"**Prescribed on:** {user_data.get('last_doctor_visit', 'N/A')}")
        if st.button("View Prescription Document"):
            st.markdown("![Prescription](https://via.placeholder.com/600x400?text=Prescription+Document)")
            st.download_button("Download Prescription", "prescription_data", "prescription.pdf")
    
    with tabs[1]:
        st.write("No previous prescriptions available via API.")
    
    # Medicine schedule
    st.markdown("### 💊 Medicine Schedule")
    
    medicine_data = make_api_request(f"medication-reminders/{st.session_state.user_id}")
    if medicine_data:
        for med in medicine_data:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
            col1.write(f"**{med['medication_name']}**")
            
            morning_status = "✅" if med["morning"] else "❌"
            afternoon_status = "✅" if med["afternoon"] else "❌"
            evening_status = "✅" if med["evening"] else "❌"
            
            col2.write(f"Morning: {morning_status}")
            col3.write(f"Afternoon: {afternoon_status}")
            col4.write(f"Evening: {evening_status}")
            col5.write(f"{med['dosage']} - {med['purpose']}")
            
            # Simulated adherence
            adherence = random.choice(["High", "Medium", "Low"])
            adherence_color = {"High": "green", "Medium": "orange", "Low": "red"}
            st.markdown(f"<div style='height:8px; background-color:{adherence_color[adherence]}; margin-bottom:15px;'></div>", unsafe_allow_html=True)
    
    # Upcoming reminders
    st.markdown("### ⏰ Today's Reminders")
    current_hour = datetime.datetime.now().hour
    reminders = []
    for med in medicine_data or []:
        if current_hour < 12 and med["morning"]:
            reminders.append(med["medication_name"])
        elif 12 <= current_hour < 16 and med["afternoon"]:
            reminders.append(med["medication_name"])
        elif current_hour >= 16 and med["evening"]:
            reminders.append(med["medication_name"])
    
    if reminders:
        time_slot = "9:00 AM" if current_hour < 12 else "2:00 PM" if current_hour < 16 else "8:00 PM"
        st.success(f"🔔 **{time_slot}** - Take medications ({', '.join(reminders)})")
    else:
        st.write("No reminders for now.")

# --- Contact Loved Ones ---
def contact_loved_ones():
    st.subheader("👪 Connect with Family & Loved Ones")
    
    if "user_id" not in st.session_state:
        st.error("User not logged in.")
        return
    
    # Fetch family contacts
    family_contacts = make_api_request(f"family-contacts/{st.session_state.user_id}")
    if not family_contacts:
        st.error("No family contacts found.")
        return
    
    # Upcoming reminders
    st.markdown("### 📅 Upcoming Family Reminders")
    upcoming_reminders = [contact for contact in family_contacts if contact["reminder"]]
    if upcoming_reminders:
        for contact in upcoming_reminders:
            st.info(f"🔔 **{contact['name']}** ({contact['relation']}): {contact['reminder']}")
    else:
        st.write("No upcoming reminders")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    daughter = next((c for c in family_contacts if c['relation'].lower() == 'daughter'), None)
    son = next((c for c in family_contacts if c['relation'].lower() == 'son'), None)
    
    with col1:
        if daughter and st.button("📞 Call Daughter"):
            st.success(f"📱 Calling {daughter['name']} (Daughter)...")
            st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/telephone_ring.wav", format="audio/wav")
    
    with col2:
        if son and st.button("📹 Video Call Son"):
            st.success(f"🎥 Starting video call with {son['name']} (Son)...")
    
    with col3:
        if st.button("🆘 Emergency Alert"):
            st.error("🚨 Emergency alert sent to all family members!")
    
    # Contact list
    st.markdown("### 📒 Contact List")
    for contact in family_contacts:
        with st.expander(f"👤 {contact['name']} • {contact['relation']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown("""
                    <div style="background-color:#f0f0f0; width:80px; height:80px; 
                    border-radius:50%; display:flex; align-items:center; justify-content:center; 
                    text-align:center; color:#555; font-size:10px;">
                        Photo
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.write(f"**Phone:** {contact['phone']}")
                st.write(f"**Last Contact:** {contact.get('last_contact', 'N/A')}")
                if contact["reminder"]:
                    st.write(f"**Reminder:** {contact['reminder']}")
            
            action_col1, action_col2, action_col3 = st.columns(3)
            with action_col1:
                if st.button(f"📞 Call", key=f"call_{contact['id']}"):
                    st.success(f"📱 Calling {contact['name']}...")
            
            with action_col2:
                if st.button(f"💬 Message", key=f"msg_{contact['id']}"):
                    st.text_area(f"Message to {contact['name']}", key=f"text_{contact['id']}")
                    if st.button(f"Send", key=f"send_{contact['id']}"):
                        st.success(f"✅ Message sent to {contact['name']}!")
            
            with action_col3:
                if st.button(f"📹 Video", key=f"video_{contact['id']}"):
                    st.success(f"🎥 Starting video call with {contact['name']}...")
    
    # Send new message
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
    
    # Recent messages (placeholder)
    st.markdown("### 📨 Recent Messages")
    st.write("No recent messages available via API.")

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
        .stTextInput label {
            color: black !important;
            background-color: rgba(255, 255, 255, 0.7) !important;
            padding: 5px 10px !important;
            border-radius: 5px !important;
            font-weight: bold !important;
        }
        .stTextInput input {
            background-color: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid #4B4B4B !important;
            color: black !important;
            font-weight: 500 !important;
        }
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            font-weight: bold !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-header">🧓 AIKA – An Elderly Care App</div>', unsafe_allow_html=True)
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        response = make_api_request("login", method="POST", data={"email": email, "password": password})
        if response and response.get("message") == "Login successful":
            st.session_state.logged_in = True
            st.session_state.role = response["user"]["role"]
            st.session_state.user_id = response["user"]["user_id"]
            st.session_state.user_name = response["user"]["name"]
            st.success("Login successful!")
        else:
            st.error("❌ Invalid email or password")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Elderly Dashboard ---
def elderly_dashboard():
    st.title(f"👵 Elderly Dashboard – {st.session_state.user_name}")
    
    option = st.sidebar.selectbox("Choose an option", [
        "Personal Information",
        "Connect with Volunteers",
        "Medicine Reminders",
        "Contact Loved Ones",
        "Health Alerts",
        "Health Record History",
        "Order History"
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

        # JSON file upload for fall detection
        st.markdown("#### 🧪 Upload Sensor Data for Fall Detection")
        uploaded_file = st.file_uploader("Choose a JSON file (2048 timesteps, 3 features)", type=["json"])
        
        if uploaded_file:
            try:
                # Read JSON file
                json_data = json.load(uploaded_file)
                sensor_data = json_data.get("input", [])
                logging.debug(f"Frontend JSON input length: {len(sensor_data)}")
                # Handle single nested list: [[[...], ...]] -> [[x, y, z], ...]
                flattened_data = sensor_data[0] if sensor_data and isinstance(sensor_data, list) and len(sensor_data) == 1 and isinstance(sensor_data[0], list) else sensor_data
                logging.debug(f"Frontend flattened data length: {len(flattened_data)}")
                logging.debug(f"Frontend first entry: {flattened_data[0] if flattened_data else 'empty'}")
                if not isinstance(flattened_data, list) or len(flattened_data) != 2048 or not all(len(item) == 3 and all(isinstance(x, (int, float)) for x in item) for item in flattened_data):
                    st.error(f"Invalid JSON format: Must contain 'input' key with 2048 entries, each with 3 numbers. Got {len(flattened_data)} entries.")
                    return
                
                # Fetch user data for region info
                user_data = make_api_request(f"users/{st.session_state.user_id}")
                if not user_data:
                    st.error("Failed to load user data.")
                    return
                
                # Prepare form data for API
                form_data = {
                    "user_id": str(st.session_state.user_id),
                    "region_name": user_data.get("region_name"),
                    "latitude": str(user_data.get("latitude", "")),
                    "longitude": str(user_data.get("longitude", "")),
                    "supervisor_name": user_data.get("supervisor_name"),
                    "supervisor_phone": user_data.get("supervisor_phone")
                }
                
                # Send original JSON to preserve format
                files = {"file": ("sensor_data.json", io.BytesIO(json.dumps(json_data).encode()), "application/json")}
                response = requests.post(
                    f"{API_BASE_URL}/detect-fall",
                    data=form_data,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                
                # Display result
                if result.get("is_fall"):
                    st.error(f"🚨 Fall detected! (Fall ID: {result['fall_id']})")
                    st.success("Nearby responsible people have been alerted (supervisor and volunteers).")
                else:
                    st.success(f"✅ No fall detected. (Fall ID: {result['fall_id']})")
                
            except json.JSONDecodeError:
                st.error("Invalid JSON file.")
            except requests.RequestException as e:
                st.error(f"API Error: {str(e)}")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
        
        # Display recent alerts
        alerts = make_api_request(f"fall-detections/{st.session_state.user_id}")
        if alerts:
            for alert in alerts:
                status = "🚨 Fall detected!" if alert["is_fall"] else "✅ No fall."
                st.write(f"{status} on {alert['timestamp']} ({alert['status']})")
        else:
            st.write("✅ No recent alerts.")
            
    elif option == "Health Record History":
        st.subheader("📊 Health Data (Last 30 Days)")
        df = pd.DataFrame(
            {   'Date': pd.date_range(start='2025-04-01', periods=30),
                'BP': [120 + (i % 5) for i in range(30)],
                'Heart Rate': [72 + (i % 3) for i in range(30)],
                'Steps': [1500 + (i * 20) for i in range(30)],
                })
        st.dataframe(df)
    
        # Graph 1: Line Chart for Blood Pressure
        st.subheader("Blood Pressure Trend")
        fig1 = px.line(df, x='Date', y='BP', title='Blood Pressure (mmHg) Over Time',
                    markers=True, color_discrete_sequence=['#FF4B4B'])
        fig1.update_layout(xaxis_title="Date", yaxis_title="Blood Pressure (mmHg)")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Graph 2: Area Chart for Heart Rate
        st.subheader("Heart Rate Trend")
        fig2 = px.area(df, x='Date', y='Heart Rate', title='Heart Rate (bpm) Over Time',
                    color_discrete_sequence=['#1F77B4'])
        fig2.update_layout(xaxis_title="Date", yaxis_title="Heart Rate (bpm)")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Graph 3: Bar Chart for Steps
        st.subheader("Daily Steps")
        fig3 = px.bar(df, x='Date', y='Steps', title='Steps Taken Per Day',
                    color_discrete_sequence=['#2CA02C'])
        fig3.update_layout(xaxis_title="Date", yaxis_title="Steps")
        st.plotly_chart(fig3, use_container_width=True)
        
        # Graph 4: Combined Line Chart for All Metrics
        st.subheader("Combined Health Metrics")
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=df['Date'], y=df['BP'], mode='lines+markers', name='BP (mmHg)',
                                line=dict(color='#FF4B4B')))
        fig4.add_trace(go.Scatter(x=df['Date'], y=df['Heart Rate'], mode='lines+markers', name='Heart Rate (bpm)',
                                line=dict(color='#1F77B4')))
        fig4.add_trace(go.Scatter(x=df['Date'], y=df['Steps']/100, mode='lines+markers', name='Steps (scaled)',
                                line=dict(color='#2CA02C')))
        fig4.update_layout(title='All Health Metrics Over Time (Steps Scaled for Visibility)',
                        xaxis_title="Date", yaxis_title="Value", legend_title="Metric")
        st.plotly_chart(fig4, use_container_width=True)
    
    elif option == "Order History":
        st.subheader("📦 Order History")
        
        # Fetch orders for the user
        orders = make_api_request(f"orders/{st.session_state.user_id}")
        
        if orders:
            # Separate medical and non-medical orders
            medical_orders = [o for o in orders if o["type"] == "medication"]
            non_medical_orders = [o for o in orders if o["type"] == "grocery"]
            
            # Medical Orders Section
            st.markdown("### 💊 Medical Orders")
            if medical_orders:
                # Prepare data for table
                medical_data = []
                for order in medical_orders:
                    details = json.loads(order["details"]) if isinstance(order["details"], str) else order["details"]
                    medical_data.append({
                        "Order ID": order["order_id"],
                        "Items": ", ".join(details.get("items", [])),
                        "Pharmacy": details.get("pharmacy", "N/A"),
                        "Status": order["status"].replace("_", " ").title(),
                        "Volunteer ID": order["volunteer_id"] if order["volunteer_id"] else "None",
                        "Ordered On": order["created_at"]
                    })
                # Display table
                st.dataframe(pd.DataFrame(medical_data), use_container_width=True)
            else:
                st.write("No medical orders found.")
            
            # Non-Medical Orders Section
            st.markdown("### 🛒 Non-Medical Orders")
            if non_medical_orders:
                # Prepare data for table
                non_medical_data = []
                for order in non_medical_orders:
                    details = json.loads(order["details"]) if isinstance(order["details"], str) else order["details"]
                    non_medical_data.append({
                        "Order ID": order["order_id"],
                        "Items": ", ".join(details.get("items", [])),
                        "Total (₹)": details.get("total", "N/A"),
                        "Status": order["status"].replace("_", " ").title(),
                        "Volunteer ID": order["volunteer_id"] if order["volunteer_id"] else "None",
                        "Ordered On": order["created_at"]
                    })
                # Display table
                st.dataframe(pd.DataFrame(non_medical_data), use_container_width=True)
            else:
                st.write("No non-medical orders found.")
        else:
            st.write("No orders found for this user.")

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
        st.session_state.user_id = None
        st.session_state.user_name = None
    
    if not st.session_state.logged_in:
        login()
    else:
        show_dashboard(st.session_state.role)

if __name__ == "__main__":
    main()