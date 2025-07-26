-- Regions
INSERT INTO regions (name, latitude, longitude, supervisor_name, supervisor_phone) VALUES
    ('North Chennai', 13.1477, 80.2859, 'Rajesh Kumar', '+91 9876543210'),
    ('South Chennai', 12.9507, 80.2047, 'Lakshmi Narayan', '+91 9876543211'),
    ('East Chennai', 13.0827, 80.2707, 'Priya Venkatesh', '+91 9876543212'),
    ('West Chennai', 13.0477, 80.1831, 'Karthik Raman', '+91 9876543213'),
    ('Central Chennai', 13.0802, 80.2838, 'Meena Sundaram', '+91 9876543214');

-- Users
INSERT INTO users (
    name, email, password, phone, address, region_id, role, age, gender, blood_group,
    dob, emergency_contact, aadhaar_no, state, pin_code, landmark, residence_type,
    years_at_address, medical_conditions, allergies, dietary_restrictions, special_needs,
    primary_doctor_name, primary_doctor_contact, primary_hospital, last_doctor_visit,
    next_appointment
) VALUES (
    'Ramesh Krishnan', 'ramesh.k@gmail.com', '123', '+91 9876543210', '45, Gandhi Street, Adyar', 
    (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'elderly', 72, 'Male', 'O+',
    '1953-03-15', '+91 8765432109', 'XXXX-XXXX-7890', 'Tamil Nadu', '600020', 'Near Apollo Hospital', 'Own',
    23, '{"Diabetes Type 2": "Since 2010", "Hypertension": "Since 2008", "Arthritis": "Since 2015"}', 
    '["Penicillin", "Peanuts"]', 'Vegetarian, Low Sugar', 'Reading glasses, Walking stick',
    'Dr. Anita Sharma', '+91 44 28293333', 'Apollo Hospitals, Chennai', '2025-03-15', '2025-05-12'
),
(
    'Sridevi Nair', 'sridevi@example.com', '123', '+91 9876543212', '12, Marina Beach Rd', 
    (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'volunteer', NULL, NULL, NULL,
    NULL, NULL, NULL, 'Tamil Nadu', '600020', NULL, NULL,
    NULL, '{}', '[]', NULL, NULL,
    NULL, NULL, NULL, NULL, NULL
),
(
    'Priya Suresh', 'priya@example.com', '123', '+91 8765432109', 'Bengaluru', 
    NULL, 'lovedone', 45, 'Female', NULL,
    '1980-05-20', NULL, NULL, NULL, NULL, NULL, NULL,
    NULL, '{}', '[]', NULL, NULL,
    NULL, NULL, NULL, NULL, NULL
);

-- Volunteers
INSERT INTO volunteer_attributes (volunteer_id, status, skills, distance) VALUES
    ((SELECT user_id FROM users WHERE email = 'sridevi@example.com'), 'Available', 
     '["First Aid Certified", "Driver"]', 0.8);

-- Family contacts
INSERT INTO family_contacts (
    elderly_id, name, relation, phone, address, last_contact, reminder, is_local_guardian
) VALUES (
    (SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'),
    'Lakshmi Krishnan', 'Wife', '+91 9876543211', '45, Gandhi Street, Adyar', 
    '2025-04-13 10:00:00', NULL, FALSE
),
(
    (SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'),
    'Karthik Krishnan', 'Son', '+91 7654321098', 'USA', 
    '2025-04-08 14:15:00', 'Video call tomorrow at 9 PM', FALSE
);

-- Medication reminders
INSERT INTO medication_reminders (
    user_id, medication_name, dosage, morning, afternoon, evening, purpose, frequency
) VALUES (
    (SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'),
    'Telma 40', '1 tablet', TRUE, FALSE, TRUE, 'Blood Pressure', 'daily'
),
(
    (SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'),
    'Ecosprin 75', '1 tablet', TRUE, FALSE, FALSE, 'Blood Thinner', 'daily'
);