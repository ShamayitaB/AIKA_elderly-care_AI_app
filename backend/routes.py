from flask import Flask, jsonify, request
from db import get_db_connection
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import tensorflow as tf
import numpy as np
import logging

def init_routes(app):
    # Load LSTM model at startup
    try:
        fall_model = tf.keras.models.load_model("models/fall_detection_lstm.h5")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        fall_model = None

    def preprocess_sensor_data(data):
        try:
            # Flatten nested list: [[[...], ...]] -> [[x, y, z], ...]
            flattened_data = data[0] if data and isinstance(data, list) and len(data) == 1 and isinstance(data[0], list) else data
            data_array = np.array(flattened_data, dtype=np.float32)  # Shape: (2048, 3)
            max_abs = np.max(np.abs(data_array))
            normalized_data = data_array / max_abs if max_abs != 0 else data_array
            return normalized_data.reshape(1, 2048, 3)  # Shape: (1, 2048, 3)
        except Exception as e:
            logging.error(f"Preprocessing error: {str(e)}")
            raise ValueError(f"Preprocessing error: {str(e)}")
           
    # Helper function to get or create region
    def get_or_create_region(region_name, latitude=None, longitude=None, supervisor_name=None, supervisor_phone=None):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT region_id FROM regions WHERE name = %s", (region_name,))
            region = cur.fetchone()
            if region:
                return region[0]
            else:
                cur.execute(
                    """
                    INSERT INTO regions (name, latitude, longitude, supervisor_name, supervisor_phone)
                    VALUES (%s, %s, %s, %s, %s) RETURNING region_id
                    """,
                    (region_name, latitude, longitude, supervisor_name, supervisor_phone)
                )
                region_id = cur.fetchone()[0]
                conn.commit()
                return region_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()


    # Login endpoint
    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT user_id, name, email, role
                FROM users
                WHERE email = %s AND password = %s
                """,
                (email, password)
            )
            user = cur.fetchone()
            if user:
                return jsonify({"message": "Login successful", "user": user}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        finally:
            cur.close()
            conn.close()

    # Create a user
    @app.route("/api/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        region_name = data.get("region_name")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        supervisor_name = data.get("supervisor_name")
        supervisor_phone = data.get("supervisor_phone")
        
        try:
            region_id = get_or_create_region(
                region_name, latitude, longitude, supervisor_name, supervisor_phone
            ) if region_name else None
            
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                """
                INSERT INTO users (
                    name, email, password, phone, address, region_id, role, age, gender, blood_group, 
                    dob, emergency_contact, aadhaar_no, state, pin_code, landmark, residence_type,
                    years_at_address, medical_conditions, allergies, dietary_restrictions, special_needs,
                    primary_doctor_name, primary_doctor_contact, primary_hospital, last_doctor_visit,
                    next_appointment
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id
                """,
                (
                    data["name"],
                    data["email"],
                    data["password"],
                    data.get("phone"),
                    data.get("address"),
                    region_id,
                    data.get("role", "elderly"),
                    data.get("age"),
                    data.get("gender"),
                    data.get("blood_group"),
                    data.get("dob"),
                    data.get("emergency_contact"),
                    data.get("aadhaar_no"),
                    data.get("state"),
                    data.get("pin_code"),
                    data.get("landmark"),
                    data.get("residence_type"),
                    data.get("years_at_address"),
                    json.dumps(data.get("medical_conditions", {})),
                    json.dumps(data.get("allergies", [])),
                    data.get("dietary_restrictions"),
                    data.get("special_needs"),
                    data.get("primary_doctor_name"),
                    data.get("primary_doctor_contact"),
                    data.get("primary_hospital"),
                    data.get("last_doctor_visit"),
                    data.get("next_appointment")
                )
            )
            user_id = cur.fetchone()["user_id"]
            conn.commit()
            return jsonify({"message": "User created", "user_id": user_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

    # Get user by ID
    @app.route("/api/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT u.*, r.name AS region_name, r.supervisor_name, r.supervisor_phone
            FROM users u
            LEFT JOIN regions r ON u.region_id = r.region_id
            WHERE u.user_id = %s
            """,
            (user_id,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return jsonify(user)
        return jsonify({"error": "User not found"}), 404

    # Update volunteer attributes
    @app.route("/api/volunteers/<int:volunteer_id>", methods=["PUT"])
    def update_volunteer_attributes(volunteer_id):
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO volunteer_attributes (volunteer_id, status, skills, distance)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (volunteer_id)
                DO UPDATE SET
                    status = EXCLUDED.status,
                    skills = EXCLUDED.skills,
                    distance = EXCLUDED.distance,
                    last_updated = CURRENT_TIMESTAMP
                """,
                (
                    volunteer_id,
                    data.get("status", "Available"),
                    json.dumps(data.get("skills", [])),
                    data.get("distance")
                )
            )
            conn.commit()
            return jsonify({"message": "Volunteer attributes updated"}), 200
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

    # Get volunteers by region
    @app.route("/api/volunteers/region/<string:region_name>", methods=["GET"])
    def get_volunteers_by_region(region_name):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT u.user_id, u.name, u.phone, va.status, va.skills, va.distance,
                       r.supervisor_name, r.supervisor_phone
                FROM users u
                JOIN volunteer_attributes va ON u.user_id = va.volunteer_id
                JOIN regions r ON u.region_id = r.region_id
                WHERE r.name = %s AND u.role = 'volunteer'
                ORDER BY va.distance
                """,
                (region_name,)
            )
            volunteers = cur.fetchall()
            return jsonify(volunteers), 200
        finally:
            cur.close()
            conn.close()

    # Get fall detections by user ID
    @app.route("/api/fall-detections/<int:user_id>", methods=["GET"])
    def get_fall_detections(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT fall_id, timestamp, is_fall, status
                FROM fall_detections
                WHERE user_id = %s
                ORDER BY timestamp DESC
                """,
                (user_id,)
            )
            detections = cur.fetchall()
            return jsonify(detections), 200
        finally:
            cur.close()
            conn.close()

    # Create an order
    @app.route("/api/orders", methods=["POST"])
    def create_order():
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO orders (user_id, type, details, status)
                VALUES (%s, %s, %s, 'pending') RETURNING order_id
                """,
                (data["user_id"], data["type"], json.dumps(data["details"]))
            )
            order_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"message": "Order created", "order_id": order_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

    # Orders endpoint
    @app.route("/api/orders/<user_id>", methods=["GET"])
    def get_orders(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT order_id, user_id, type, details, status, volunteer_id, created_at
                FROM orders
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            orders = cur.fetchall()
            return jsonify(orders), 200
        except psycopg2.Error as e:
            logging.error(f"Database error: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()
            conn.close()

    # Get medication reminders by user ID
    @app.route("/api/medication-reminders/<int:user_id>", methods=["GET"])
    def get_medication_reminders(user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT reminder_id, medication_name, dosage, morning, afternoon, evening, purpose, frequency
                FROM medication_reminders
                WHERE user_id = %s
                """,
                (user_id,)
            )
            reminders = cur.fetchall()
            return jsonify(reminders), 200
        finally:
            cur.close()
            conn.close()

    # Set medication reminder
    @app.route("/api/reminders", methods=["POST"])
    def create_reminder():
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO medication_reminders (
                    user_id, medication_name, dosage, morning, afternoon, evening,
                    purpose, frequency, custom_days
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING reminder_id
                """,
                (
                    data["user_id"],
                    data["medication_name"],
                    data["dosage"],
                    data.get("morning", False),
                    data.get("afternoon", False),
                    data.get("evening", False),
                    data.get("purpose"),
                    data["frequency"],
                    data.get("custom_days")
                )
            )
            reminder_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"message": "Reminder set", "reminder_id": reminder_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

    # Create family contact
    @app.route("/api/family-contacts", methods=["POST"])
    def create_family_contact():
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO family_contacts (
                    elderly_id, name, relation, phone, address, last_contact,
                    reminder, is_local_guardian
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING contact_id
                """,
                (
                    data["elderly_id"],
                    data["name"],
                    data["relation"],
                    data["phone"],
                    data.get("address"),
                    data.get("last_contact"),
                    data.get("reminder"),
                    data.get("is_local_guardian", False)
                )
            )
            contact_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"message": "Family contact created", "contact_id": contact_id}), 201
        except psycopg2.Error as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            cur.close()
            conn.close()

    # Get family contacts (includes lovedone role users)
    @app.route("/api/family-contacts/<int:elderly_id>", methods=["GET"])
    def get_family_contacts(elderly_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute(
                """
                SELECT contact_id AS id, name, relation, phone, address, last_contact, reminder, is_local_guardian
                FROM family_contacts
                WHERE elderly_id = %s
                UNION
                SELECT user_id AS id, name, role AS relation, phone, address, NULL AS last_contact, NULL AS reminder, FALSE AS is_local_guardian
                FROM users
                WHERE role = 'lovedone' AND region_id = (
                    SELECT region_id FROM users WHERE user_id = %s
                )
                """,
                (elderly_id, elderly_id)
            )
            contacts = cur.fetchall()
            return jsonify(contacts), 200
        finally:
            cur.close()
            conn.close()

    # Fall detection endpoint
    @app.route("/api/detect-fall", methods=["POST"])
    def detect_fall():
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        user_id = request.form.get("user_id")
        region_name = request.form.get("region_name")
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        supervisor_name = request.form.get("supervisor_name")
        supervisor_phone = request.form.get("supervisor_phone")

        if not user_id or not file:
            return jsonify({"error": "Missing user_id or file"}), 400

        try:
            # Read and parse JSON file
            json_data = json.load(file)
            sensor_data = json_data.get("input", [])
            logging.debug(f"JSON input length: {len(sensor_data)}")
            # Validate single nested list
            flattened_data = sensor_data[0] if sensor_data and isinstance(sensor_data, list) and len(sensor_data) == 1 and isinstance(sensor_data[0], list) else sensor_data
            logging.debug(f"Flattened data length: {len(flattened_data)}")
            logging.debug(f"First entry: {flattened_data[0] if flattened_data else 'empty'}")
            if not isinstance(flattened_data, list) or len(flattened_data) != 2048 or not all(len(item) == 3 and all(isinstance(x, (int, float)) for x in item) for item in flattened_data):
                return jsonify({"error": f"Invalid JSON format: Must contain 'input' key with 2048 entries, each with 3 numbers. Got {len(flattened_data)} entries."}), 400

            # Get or create region
            region_id = get_or_create_region(
                region_name, latitude, longitude, supervisor_name, supervisor_phone
            ) if region_name else None

            # Preprocess and predict
            if not fall_model:
                return jsonify({"error": "Fall detection model not loaded"}), 500

            processed_data = preprocess_sensor_data(sensor_data)
            prediction = fall_model.predict(processed_data, verbose=0)
            predicted_class = np.argmax(prediction, axis=1)[0]
            is_fall = predicted_class in [1, 2]  # Pre-fall or Fall Detected
            logging.debug(f"Predicted class: {predicted_class}, is_fall: {is_fall}")

            # Store in database
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO fall_detections (user_id, region_id, is_fall, status)
                VALUES (%s, %s, %s, %s) RETURNING fall_id
                """,
                (user_id, region_id, is_fall, "pending" if is_fall else "no_action")
            )
            fall_id = cur.fetchone()[0]
            conn.commit()

            return jsonify({
                "message": "Fall detection processed",
                "fall_id": fall_id,
                "is_fall": is_fall
            }), 201
        except (ValueError, psycopg2.Error, json.JSONDecodeError) as e:
            if 'conn' in locals():
                conn.rollback()
            logging.error(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()