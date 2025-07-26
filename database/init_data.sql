-- init_data.sql
-- Initialize all tables with sample data for elderly care app
-- Target: 10 elderly, 10 volunteers, 5 loved ones, 2 caregivers, and related data
-- Date: April 13, 2025

-- Disable constraints temporarily for bulk insert
SET CONSTRAINTS ALL DEFERRED;

-- 1. Regions (5 Chennai regions with supervisors)
INSERT INTO regions (name, latitude, longitude, supervisor_name, supervisor_phone) VALUES
    ('North Chennai', 13.1477, 80.2859, 'Rajesh Kumar', '+91 9876543210'),
    ('South Chennai', 12.9507, 80.2047, 'Lakshmi Narayan', '+91 9876543211'),
    ('East Chennai', 13.0827, 80.2707, 'Priya Venkatesh', '+91 9876543212'),
    ('West Chennai', 13.0477, 80.1831, 'Karthik Raman', '+91 9876543213'),
    ('Central Chennai', 13.0802, 80.2838, 'Meena Sundaram', '+91 9876543214');

-- 2. Users (10 elderly, 10 volunteers, 5 loved ones, 2 caregivers)
-- Elderly users (10)
INSERT INTO users (
    name, email, password, phone, address, region_id, role, age, gender, blood_group,
    dob, emergency_contact, aadhaar_no, state, pin_code, landmark, residence_type,
    years_at_address, medical_conditions, allergies, dietary_restrictions, special_needs,
    primary_doctor_name, primary_doctor_contact, primary_hospital, last_doctor_visit,
    next_appointment
) VALUES
    ('Ramesh Krishnan', 'ramesh.k@gmail.com', '123', '+91 9876543210', '45, Gandhi Street, Adyar', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'elderly', 72, 'Male', 'O+', 
     '1953-03-15', '+91 8765432109', 'XXXX-XXXX-7890', 'Tamil Nadu', '600020', 'Near Apollo Hospital', 
     'Own', 23, '{"Diabetes Type 2": "Since 2010", "Hypertension": "Since 2008"}', '["Penicillin"]', 
     'Vegetarian, Low Sugar', 'Walking stick', 'Dr. Anita Sharma', '+91 4428293333', 
     'Apollo Hospitals, Chennai', '2025-03-15', '2025-05-12'),
    ('Lalitha Subramanian', 'lalitha.s@gmail.com', '123', '+91 9876543211', '12, Anna Nagar', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'elderly', 68, 'Female', 'A+', 
     '1957-06-10', '+91 8765432110', 'XXXX-XXXX-7891', 'Tamil Nadu', '600040', 'Near Tower Park', 
     'Own', 20, '{"Arthritis": "Since 2015"}', '[]', 'Vegetarian', 'Hearing aid', 
     'Dr. Vijay Kumar', '+91 4426172222', 'Fortis Malar Hospital', '2025-02-20', '2025-04-25'),
    ('Suresh Menon', 'suresh.m@gmail.com', '123', '+91 9876543212', '78, Mylapore', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'elderly', 75, 'Male', 'B+', 
     '1950-01-22', '+91 8765432111', 'XXXX-XXXX-7892', 'Tamil Nadu', '600004', 'Near Kapaleeswarar Temple', 
     'Rented', 15, '{"Hypertension": "Since 2005", "Heart Disease": "Since 2012"}', '["Peanuts"]', 
     'Low Salt', 'Wheelchair', 'Dr. Rekha Nair', '+91 4424998888', 'MIOT Hospital', 
     '2025-03-01', '2025-05-01'),
    ('Geetha Ravi', 'geetha.r@gmail.com', '123', '+91 9876543213', '23, T. Nagar', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'elderly', 70, 'Female', 'O-', 
     '1955-09-12', '+91 8765432112', 'XXXX-XXXX-7893', 'Tamil Nadu', '600017', 'Near Panagal Park', 
     'Own', 25, '{"Diabetes Type 2": "Since 2008"}', '["Shellfish"]', 'Low Sugar', NULL, 
     'Dr. Sanjay Gupta', '+91 4424341234', 'Gleneagles Global Health City', '2025-03-10', '2025-06-10'),
    ('Venkatesh Iyer', 'venkatesh.i@gmail.com', '123', '+91 9876543214', '56, Velachery', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'elderly', 73, 'Male', 'AB+', 
     '1952-04-05', '+91 8765432113', 'XXXX-XXXX-7894', 'Tamil Nadu', '600042', 'Near Phoenix Mall', 
     'Own', 18, '{"Asthma": "Since 1990"}', '[]', NULL, 'Oxygen concentrator', 
     'Dr. Meena Pillai', '+91 4422567777', 'SRM Institutes for Medical Science', '2025-02-15', '2025-04-20'),
    ('Kamala Natarajan', 'kamala.n@gmail.com', '123', '+91 9876543215', '89, Royapuram', 
     (SELECT region_id FROM regions WHERE name = 'North Chennai'), 'elderly', 71, 'Female', 'A-', 
     '1954-07-19', '+91 8765432114', 'XXXX-XXXX-7895', 'Tamil Nadu', '600013', 'Near Harbour', 
     'Own', 22, '{"Hypertension": "Since 2010"}', '[]', 'Vegetarian', NULL, 
     'Dr. Anil Menon', '+91 4425922222', 'Stanley Medical College', '2025-03-05', '2025-05-15'),
    ('Mohan Das', 'mohan.d@gmail.com', '123', '+91 9876543216', '34, Triplicane', 
     (SELECT region_id FROM regions WHERE name = 'East Chennai'), 'elderly', 74, 'Male', 'B-', 
     '1951-02-28', '+91 8765432115', 'XXXX-XXXX-7896', 'Tamil Nadu', '600005', 'Near Marina Beach', 
     'Rented', 10, '{"Diabetes Type 2": "Since 2009", "Arthritis": "Since 2014"}', '["Dust"]', 
     'Low Sugar', 'Reading glasses', 'Dr. Lakshmi Devi', '+91 4424512345', 'Adyar Cancer Institute', 
     '2025-03-20', '2025-05-25'),
    ('Radha Balaji', 'radha.b@gmail.com', '123', '+91 9876543217', '67, Porur', 
     (SELECT region_id FROM regions WHERE name = 'West Chennai'), 'elderly', 69, 'Female', 'O+', 
     '1956-05-15', '+91 8765432116', 'XXXX-XXXX-7897', 'Tamil Nadu', '600116', 'Near SRM University', 
     'Own', 17, '{"Heart Disease": "Since 2010"}', '["Pollen"]', 'Low Salt', NULL, 
     'Dr. Arvind Rao', '+91 4424781234', 'Sri Ramachandra Medical Centre', '2025-03-12', '2025-05-20'),
    ('Krishnan Pillai', 'krishnan.p@gmail.com', '123', '+91 9876543218', '12, Besant Nagar', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'elderly', 76, 'Male', 'A+', 
     '1949-08-10', '+91 8765432117', 'XXXX-XXXX-7898', 'Tamil Nadu', '600090', 'Near Beach', 
     'Own', 30, '{"Hypertension": "Since 2000"}', '[]', 'Vegetarian', 'Walking stick', 
     'Dr. Shalini Kumar', '+91 4424997777', 'Kauvery Hospital', '2025-03-08', '2025-05-10'),
    ('Padma Srinivasan', 'padma.s@gmail.com', '123', '+91 9876543219', '45, Kilpauk', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'elderly', 70, 'Female', 'B+', 
     '1955-12-01', '+91 8765432118', 'XXXX-XXXX-7899', 'Tamil Nadu', '600010', 'Near Garden', 
     'Own', 21, '{"Diabetes Type 2": "Since 2011"}', '["Milk"]', 'Low Sugar', NULL, 
     'Dr. Ramesh Nair', '+91 4426445555', 'Billroth Hospitals', '2025-03-18', '2025-05-30');

-- Volunteers (10, 2 per region)
INSERT INTO users (
    name, email, password, phone, address, region_id, role
) VALUES
    ('Sridevi Nair', 'sridevi.n@example.com', '123', '+91 9876543220', '12, Marina Beach Rd', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'volunteer'),
    ('Arjun Menon', 'arjun.m@example.com', '123', '+91 9876543221', '45, Adyar', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'volunteer'),
    ('Aditya Sharma', 'aditya.s@example.com', '123', '+91 9876543222', '34, Royapuram', 
     (SELECT region_id FROM regions WHERE name = 'North Chennai'), 'volunteer'),
    ('Divya Krishnan', 'divya.k@example.com', '123', '+91 9876543223', '67, Washermanpet', 
     (SELECT region_id FROM regions WHERE name = 'North Chennai'), 'volunteer'),
    ('Gayathri Venkatesan', 'gayathri.v@example.com', '123', '+91 9876543224', '56, Triplicane', 
     (SELECT region_id FROM regions WHERE name = 'East Chennai'), 'volunteer'),
    ('Abdul Raheem', 'abdul.r@example.com', '123', '+91 9876543225', '89, Chepauk', 
     (SELECT region_id FROM regions WHERE name = 'East Chennai'), 'volunteer'),
    ('Suresh Narayanan', 'suresh.n@example.com', '123', '+91 9876543226', '56, Porur', 
     (SELECT region_id FROM regions WHERE name = 'West Chennai'), 'volunteer'),
    ('Anitha Devan', 'anitha.d@example.com', '123', '+91 9876543227', '89, Valasaravakkam', 
     (SELECT region_id FROM regions WHERE name = 'West Chennai'), 'volunteer'),
    ('Ramya Subramanian', 'ramya.s@example.com', '123', '+91 9876543228', '56, Anna Nagar', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'volunteer'),
    ('Vijay Kumar', 'vijay.k@example.com', '123', '+91 9876543229', '89, Kilpauk', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'volunteer');

-- Loved ones (5)
INSERT INTO users (
    name, email, password, phone, address, region_id, role, age, gender
) VALUES
    ('Priya Suresh', 'priya.s@example.com', '123', '+91 8765432109', 'Bengaluru', NULL, 'lovedone', 45, 'Female'),
    ('Karthik Krishnan', 'karthik.k@example.com', '123', '+91 7654321098', 'USA', NULL, 'lovedone', 42, 'Male'),
    ('Deepa Sundaram', 'deepa.s@example.com', '123', '+91 6543210987', '12, Adyar', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'lovedone', 65, 'Female'),
    ('Anand Ravi', 'anand.r@example.com', '123', '+91 8765432110', 'Mumbai', NULL, 'lovedone', 40, 'Male'),
    ('Meera Venkatesh', 'meera.v@example.com', '123', '+91 7654321099', 'Delhi', NULL, 'lovedone', 38, 'Female');

-- Caregivers (2)
INSERT INTO users (
    name, email, password, phone, address, region_id, role
) VALUES
    ('Dr. Rekha Nair', 'rekha.n@example.com', '123', '+91 9876543230', '67, Adyar', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), 'caregiver'),
    ('Dr. Vijay Kumar', 'vijay.k2@example.com', '123', '+91 9876543231', '78, Anna Nagar', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), 'caregiver');

-- 3. Volunteer Attributes (for 10 volunteers)
INSERT INTO volunteer_attributes (volunteer_id, status, skills, distance) VALUES
    ((SELECT user_id FROM users WHERE email = 'sridevi.n@example.com'), 'Available', '["First Aid Certified", "Driver"]', 0.8),
    ((SELECT user_id FROM users WHERE email = 'arjun.m@example.com'), 'Busy', '["Medical Background"]', 1.5),
    ((SELECT user_id FROM users WHERE email = 'aditya.s@example.com'), 'Available', '["Cooking", "Heavy Lifting"]', 1.2),
    ((SELECT user_id FROM users WHERE email = 'divya.k@example.com'), 'Available', '["First Aid Certified"]', 1.8),
    ((SELECT user_id FROM users WHERE email = 'gayathri.v@example.com'), 'Available', '["Driver"]', 1.0),
    ((SELECT user_id FROM users WHERE email = 'abdul.r@example.com'), 'Available', '["Medication Management"]', 1.7),
    ((SELECT user_id FROM users WHERE email = 'suresh.n@example.com'), 'Available', '["First Aid Certified", "Cooking"]', 0.5),
    ((SELECT user_id FROM users WHERE email = 'anitha.d@example.com'), 'Busy', '["Driver"]', 1.2),
    ((SELECT user_id FROM users WHERE email = 'ramya.s@example.com'), 'Available', '["Medical Background"]', 0.7),
    ((SELECT user_id FROM users WHERE email = 'vijay.k@example.com'), 'Offline', '["Heavy Lifting"]', 1.4);

-- 4. Family Contacts (20, 2–3 per elderly)
INSERT INTO family_contacts (
    elderly_id, name, relation, phone, address, last_contact, reminder, is_local_guardian
) VALUES
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'Lakshmi Krishnan', 'Wife', '+91 9876543232', '45, Gandhi Street, Adyar', 
     '2025-04-13 10:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'Priya Suresh', 'Daughter', '+91 8765432109', 'Bengaluru', 
     '2025-04-12 19:30:00', 'Visiting on Sunday at 11 AM', TRUE),
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'Karthik Krishnan', 'Son', '+91 7654321098', 'USA', 
     '2025-04-08 14:15:00', 'Video call tomorrow at 9 PM', FALSE),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 'Subramanian Ravi', 'Husband', '+91 9876543233', '12, Anna Nagar', 
     '2025-04-10 09:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 'Anand Ravi', 'Son', '+91 8765432110', 'Mumbai', 
     '2025-04-11 18:00:00', 'Check-in call on Monday', TRUE),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 'Radha Menon', 'Wife', '+91 9876543234', '78, Mylapore', 
     '2025-04-12 08:30:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 'Meera Venkatesh', 'Daughter', '+91 7654321099', 'Delhi', 
     '2025-04-09 20:00:00', 'Doctor appointment reminder', FALSE),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 'Ravi Shankar', 'Husband', '+91 9876543235', '23, T. Nagar', 
     '2025-04-11 10:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 'Deepa Sundaram', 'Sister', '+91 6543210987', '12, Adyar', 
     '2025-04-10 17:00:00', 'Birthday on April 22', FALSE),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 'Shalini Iyer', 'Wife', '+91 9876543236', '56, Velachery', 
     '2025-04-12 11:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 'Vikram Iyer', 'Son', '+91 8765432111', 'Chennai', 
     '2025-04-11 15:00:00', 'Family dinner on Saturday', TRUE),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 'Natarajan Suresh', 'Husband', '+91 9876543237', '89, Royapuram', 
     '2025-04-10 12:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 'Latha Nair', 'Daughter', '+91 8765432112', 'Hyderabad', 
     '2025-04-09 19:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 'Saraswathi Das', 'Wife', '+91 9876543238', '34, Triplicane', 
     '2025-04-12 09:30:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 'Arjun Das', 'Son', '+91 8765432113', 'Chennai', 
     '2025-04-11 14:00:00', 'Visit next week', TRUE),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 'Balaji Kumar', 'Husband', '+91 9876543239', '67, Porur', 
     '2025-04-10 10:30:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 'Shalini Kumar', 'Daughter', '+91 8765432114', 'Pune', 
     '2025-04-09 18:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 'Parvathi Pillai', 'Wife', '+91 9876543240', '12, Besant Nagar', 
     '2025-04-12 12:00:00', NULL, FALSE),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 'Rajan Pillai', 'Son', '+91 8765432115', 'Chennai', 
     '2025-04-11 16:00:00', 'Check-up reminder', TRUE),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), 'Srinivasan Rao', 'Husband', '+91 9876543241', '45, Kilpauk', 
     '2025-04-10 11:00:00', NULL, FALSE);

-- 5. Fall Detections (10)
INSERT INTO fall_detections (
    user_id, timestamp, region_id, is_fall, status
) VALUES
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), '2025-04-10 08:30:00', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), TRUE, 'resolved'),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), '2025-04-12 09:00:00', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), TRUE, 'pending'),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), '2025-04-11 16:45:00', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), TRUE, 'resolved'),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), '2025-04-09 11:30:00', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), FALSE, 'resolved'),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), '2025-04-08 07:00:00', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), TRUE, 'pending'),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), '2025-04-13 10:00:00', 
     (SELECT region_id FROM regions WHERE name = 'North Chennai'), TRUE, 'pending'),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), '2025-04-07 14:20:00', 
     (SELECT region_id FROM regions WHERE name = 'East Chennai'), FALSE, 'resolved'),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), '2025-04-11 08:15:00', 
     (SELECT region_id FROM regions WHERE name = 'West Chennai'), TRUE, 'resolved'),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), '2025-04-10 15:30:00', 
     (SELECT region_id FROM regions WHERE name = 'South Chennai'), TRUE, 'pending'),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), '2025-04-12 11:45:00', 
     (SELECT region_id FROM regions WHERE name = 'Central Chennai'), FALSE, 'resolved');

-- 6. Volunteer Connections (10)
INSERT INTO volunteer_connections (
    elderly_id, volunteer_id, status
) VALUES
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'sridevi.n@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'ramya.s@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'arjun.m@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'vijay.k@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'sridevi.n@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'aditya.s@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'gayathri.v@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'suresh.n@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'arjun.m@example.com'), 'active'),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), 
     (SELECT user_id FROM users WHERE email = 'ramya.s@example.com'), 'active');

-- 7. Orders (10)
INSERT INTO orders (
    user_id, type, details, status, volunteer_id, created_at
) VALUES
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'grocery', 
     '{"items": ["Rice", "Dal"], "total": 500}', 'delivered', 
     (SELECT user_id FROM users WHERE email = 'sridevi.n@example.com'), '2025-04-10 09:00:00'),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 'medication', 
     '{"items": ["Amlodipine"], "pharmacy": "Apollo"}', 'pending', NULL, '2025-04-12 14:00:00'),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 'grocery', 
     '{"items": ["Milk", "Bread"], "total": 200}', 'in_progress', 
     (SELECT user_id FROM users WHERE email = 'arjun.m@example.com'), '2025-04-11 10:00:00'),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 'medication', 
     '{"items": ["Metformin"], "pharmacy": "MedPlus"}', 'delivered', 
     (SELECT user_id FROM users WHERE email = 'vijay.k@example.com'), '2025-04-09 08:00:00'),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 'grocery', 
     '{"items": ["Vegetables"], "total": 300}', 'pending', NULL, '2025-04-10 12:00:00'),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 'grocery', 
     '{"items": ["Sugar", "Tea"], "total": 400}', 'delivered', 
     (SELECT user_id FROM users WHERE email = 'aditya.s@example.com'), '2025-04-12 11:00:00'),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 'medication', 
     '{"items": ["Salbutamol"], "pharmacy": "Apollo"}', 'pending', NULL, '2025-04-11 15:00:00'),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 'grocery', 
     '{"items": ["Flour", "Oil"], "total": 600}', 'in_progress', 
     (SELECT user_id FROM users WHERE email = 'suresh.n@example.com'), '2025-04-10 09:30:00'),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 'medication', 
     '{"items": ["Losartan"], "pharmacy": "MedPlus"}', 'delivered', 
     (SELECT user_id FROM users WHERE email = 'arjun.m@example.com'), '2025-04-09 07:00:00'),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), 'grocery', 
     '{"items": ["Rice", "Spices"], "total": 450}', 'pending', NULL, '2025-04-13 10:00:00');

-- 8. Medication Reminders (20, 2 per elderly)
INSERT INTO medication_reminders (
    user_id, medication_name, dosage, morning, afternoon, evening, purpose, frequency
) VALUES
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'Telma 40', '1 tablet', TRUE, FALSE, TRUE, 'Blood Pressure', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'ramesh.k@gmail.com'), 'Glycomet 500', '1 tablet', TRUE, TRUE, TRUE, 'Diabetes', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 'Amlodipine', '5 mg', FALSE, FALSE, TRUE, 'Blood Pressure', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'lalitha.s@gmail.com'), 'Calcitrol D3', '1 capsule', FALSE, FALSE, TRUE, 'Vitamin D', 'weekly'),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 'Losartan', '50 mg', TRUE, FALSE, FALSE, 'Hypertension', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'suresh.m@gmail.com'), 'Aspirin', '75 mg', TRUE, FALSE, FALSE, 'Heart Disease', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 'Metformin', '500 mg', TRUE, TRUE, FALSE, 'Diabetes', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'geetha.r@gmail.com'), 'Atorvastatin', '10 mg', FALSE, FALSE, TRUE, 'Cholesterol', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 'Salbutamol', '2 puffs', TRUE, FALSE, FALSE, 'Asthma', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'venkatesh.i@gmail.com'), 'B-Complex', '1 tablet', TRUE, FALSE, FALSE, 'Supplement', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 'Telmisartan', '40 mg', TRUE, FALSE, TRUE, 'Blood Pressure', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'kamala.n@gmail.com'), 'Vitamin D3', '1 capsule', FALSE, FALSE, TRUE, 'Supplement', 'weekly'),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 'Glimepiride', '2 mg', TRUE, FALSE, FALSE, 'Diabetes', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'mohan.d@gmail.com'), 'Paracetamol', '500 mg', FALSE, TRUE, FALSE, 'Pain Relief', 'custom'),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 'Ecosprin', '75 mg', TRUE, FALSE, FALSE, 'Heart Disease', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'radha.b@gmail.com'), 'Rosuvastatin', '5 mg', FALSE, FALSE, TRUE, 'Cholesterol', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 'Amlodipine', '5 mg', TRUE, FALSE, FALSE, 'Hypertension', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'krishnan.p@gmail.com'), 'Vitamin B12', '1 tablet', TRUE, FALSE, FALSE, 'Supplement', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), 'Metformin', '500 mg', TRUE, TRUE, TRUE, 'Diabetes', 'daily'),
    ((SELECT user_id FROM users WHERE email = 'padma.s@gmail.com'), 'Telmisartan', '40 mg', TRUE, FALSE, TRUE, 'Blood Pressure', 'daily');

-- Re-enable constraints
SET CONSTRAINTS ALL IMMEDIATE;

-- Commit transaction
COMMIT;