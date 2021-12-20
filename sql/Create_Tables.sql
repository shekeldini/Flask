CREATE TABLE IF NOT EXISTS "district"(
"id_district" SERIAL,
"district_name" VARCHAR(30) NOT NULL,
CONSTRAINT "K26" PRIMARY KEY ("id_district")
);

CREATE TABLE IF NOT EXISTS "oo_location_type"(
"id_oo_location_type" SERIAL,
"location_type" VARCHAR(85) NOT NULL,
CONSTRAINT "K27" PRIMARY KEY ("id_oo_location_type")
);

CREATE TABLE IF NOT EXISTS "name_of_the_settlement"(
"id_name_of_the_settlement" SERIAL,
"id_district" INTEGER NOT NULL,
"id_oo_location_type" INTEGER NOT NULL,
"name" VARCHAR(30) NOT NULL,
UNIQUE("id_district", "id_oo_location_type", "name"),
CONSTRAINT "K29" PRIMARY KEY ("id_name_of_the_settlement"),
CONSTRAINT "C29" FOREIGN KEY ("id_district")
    REFERENCES "district" ("id_district"),
CONSTRAINT "C30" FOREIGN KEY ("id_oo_location_type")
    REFERENCES "oo_location_type" ("id_oo_location_type")
);

CREATE TABLE IF NOT EXISTS "organizational_and_legal_form"(
"id_organizational_and_legal_form" SERIAL,
"type_of_organizational_and_legal_form" VARCHAR(30) NOT NULL,
CONSTRAINT "K31" PRIMARY KEY ("id_organizational_and_legal_form")
);

CREATE TABLE IF NOT EXISTS "population_of_the_settlement"(
"id_population_of_the_settlement" SERIAL,
"interval" VARCHAR(30) NOT NULL,
CONSTRAINT "K32" PRIMARY KEY ("id_population_of_the_settlement")
);

CREATE TABLE IF NOT EXISTS "internet_speed"(
"id_internet_speed" SERIAL,
"interval"VARCHAR(30) NOT NULL,
CONSTRAINT "K45" PRIMARY KEY ("id_internet_speed")
);

CREATE TABLE IF NOT EXISTS "the_involvement_of_students_in_additional_education"(
"id_the_involvement_of_students_in_additional_education" SERIAL,
"interval" VARCHAR(30) NOT NULL,
CONSTRAINT "K33" PRIMARY KEY ("id_the_involvement_of_students_in_additional_education")
);

CREATE TABLE IF NOT EXISTS "count_of_parents_attending_events"(
"id_count_of_parents_attending_events" SERIAL,
"description" VARCHAR(40) NOT NULL,
CONSTRAINT "K34" PRIMARY KEY ("id_count_of_parents_attending_events")
);

CREATE TABLE IF NOT EXISTS "count_of_parents_ready_to_help"(
"id_count_of_parents_ready_to_help" SERIAL,
"description" VARCHAR(40) NOT NULL,
CONSTRAINT "K35" PRIMARY KEY ("id_count_of_parents_ready_to_help")
);

CREATE TABLE IF NOT EXISTS "regular_transport_link"(
"id_regular_transport_link" SERIAL,
"description" VARCHAR(120) NOT NULL,
CONSTRAINT "K36" PRIMARY KEY ("id_regular_transport_link")
);

CREATE TABLE IF NOT EXISTS "frequency_of_regular_transport_link"(
"id_frequency_of_regular_transport_link" SERIAL,
"description" VARCHAR(120) NOT NULL,
CONSTRAINT "K37" PRIMARY KEY ("id_frequency_of_regular_transport_link")
);

CREATE TABLE IF NOT EXISTS "possibility_to_get_to_the_oo_by_public_transport"(
"id_possibility_to_get_to_the_oo_by_public_transport" SERIAL,
"description" VARCHAR(200) NOT NULL,
CONSTRAINT "K38" PRIMARY KEY ("id_possibility_to_get_to_the_oo_by_public_transport")
);

CREATE TABLE IF NOT EXISTS "oo_logins"(
"oo_login" VARCHAR(20) NOT NULL,
CONSTRAINT "K2" PRIMARY KEY ("oo_login")
);

CREATE TABLE IF NOT EXISTS "oo"(
"id_oo" SERIAL,
"oo_login" VARCHAR(20) NOT NULL,
"year" VARCHAR(4) NOT NULL,
"id_name_of_the_settlement"INTEGER,
"id_organizational_and_legal_form" INTEGER,
"id_population_of_the_settlement" INTEGER,
"id_internet_speed" INTEGER,
"id_the_involvement_of_students_in_additional_education" INTEGER,
"id_count_of_parents_attending_events" INTEGER,
"id_count_of_parents_ready_to_help" INTEGER,
"id_regular_transport_link" INTEGER,
"id_frequency_of_regular_transport_link" INTEGER,
"id_possibility_to_get_to_the_oo_by_public_transport" INTEGER,
"oo_name"  VARCHAR(300),
"oo_full_name" VARCHAR(300),
"oo_address" VARCHAR(300),
"full_name_of_the_director" VARCHAR(60),
"email_oo" VARCHAR(40),
"phone_number" VARCHAR(20),
"oo_is_corrective" boolean,
"oo_is_night" boolean,
"oo_is_special_educational_institution_of_a_closed_type" boolean,
"oo_attached_to_an_organization_executing_a_sentence_of_imprisonment" boolean,
"oo_is_a_boarding" boolean,
"count_of_teachers" INTEGER,
"count_of_teachers_of_the_highest_category" INTEGER,
"count_of_teachers_not_older_than_30_years" INTEGER,
"count_of_teachers_reached_retirement_age" INTEGER,
"count_of_classrooms_in_which_classes_are_held" INTEGER,
"count_of_classrooms_in_which_the_teacher_place_is_equipped_with_a_computer" INTEGER,
"count_of_cabinets_with_a_projector_or_interactive_whiteboard" INTEGER,
"count_of_computers_that_students_can_use_in_the_learning_process" INTEGER, 
"count_of_old_computers" INTEGER,
"count_of_computers_with_internet_access" INTEGER,
CONSTRAINT "K1" PRIMARY KEY ("id_oo"),
CONSTRAINT "C1" FOREIGN KEY ("oo_login")
    REFERENCES "oo_logins" ("oo_login"),
CONSTRAINT "C36" FOREIGN KEY ("id_name_of_the_settlement")
    REFERENCES "name_of_the_settlement" ("id_name_of_the_settlement"),
CONSTRAINT "C37" FOREIGN KEY ("id_organizational_and_legal_form")
    REFERENCES "organizational_and_legal_form" ("id_organizational_and_legal_form"),
CONSTRAINT "C38" FOREIGN KEY ("id_population_of_the_settlement")
    REFERENCES "population_of_the_settlement" ("id_population_of_the_settlement"),
CONSTRAINT "C47" FOREIGN KEY ("id_internet_speed")
    REFERENCES "internet_speed" ("id_internet_speed"),
CONSTRAINT "C39" FOREIGN KEY ("id_the_involvement_of_students_in_additional_education")
    REFERENCES "the_involvement_of_students_in_additional_education" ("id_the_involvement_of_students_in_additional_education"),
CONSTRAINT "C41" FOREIGN KEY ("id_count_of_parents_attending_events")
    REFERENCES "count_of_parents_attending_events" ("id_count_of_parents_attending_events"),
CONSTRAINT "C42" FOREIGN KEY ("id_count_of_parents_ready_to_help")
    REFERENCES "count_of_parents_ready_to_help" ("id_count_of_parents_ready_to_help"),
CONSTRAINT "C43" FOREIGN KEY ("id_regular_transport_link")
    REFERENCES "regular_transport_link" ("id_regular_transport_link"),
CONSTRAINT "C44" FOREIGN KEY ("id_frequency_of_regular_transport_link")
    REFERENCES "frequency_of_regular_transport_link" ("id_frequency_of_regular_transport_link"),
CONSTRAINT "C45" FOREIGN KEY ("id_possibility_to_get_to_the_oo_by_public_transport")
    REFERENCES "possibility_to_get_to_the_oo_by_public_transport" ("id_possibility_to_get_to_the_oo_by_public_transport")
);

CREATE TABLE IF NOT EXISTS "properties"(
"id_properties" SERIAL,
"name" VARCHAR(30) NOT NULL,
CONSTRAINT "K4" PRIMARY KEY ("id_properties")
);

CREATE TABLE IF NOT EXISTS "oo_properties"(
"id_properties" INTEGER NOT NULL,
"id_oo" INTEGER NOT NULL,
"Value" VARCHAR (20) NOT NULL,
CONSTRAINT "K5" PRIMARY KEY ("id_properties", "id_oo"),
CONSTRAINT "C3" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C2" FOREIGN KEY ("id_properties")
    REFERENCES "properties" ("id_properties")
);

CREATE TABLE IF NOT EXISTS "duration_of_refresher_courses"(
"id_duration_of_refresher_courses" SERIAL,
"duration" VARCHAR (50) NOT NULL,
CONSTRAINT "K16" PRIMARY KEY ("id_duration_of_refresher_courses")
);

CREATE TABLE IF NOT EXISTS "completed_advanced_training_courses_for_teachers"(
"id_oo" INTEGER NOT NULL,
"id_duration_of_refresher_courses" INTEGER NOT NULL,
"count_of_teachers" INTEGER NOT NULL,
CONSTRAINT "K17" PRIMARY KEY ("id_oo", "id_duration_of_refresher_courses"),
CONSTRAINT "C18" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C19" FOREIGN KEY ("id_duration_of_refresher_courses")
    REFERENCES "duration_of_refresher_courses" ("id_duration_of_refresher_courses")
);

CREATE TABLE IF NOT EXISTS "description_of_work_with_teachers_taking_advanced_training_courses"(
"id_description_of_work_with_teachers_taking_advanced_training_courses" SERIAL,
"description" VARCHAR (73) NOT NULL,
CONSTRAINT "K18" PRIMARY KEY ("id_description_of_work_with_teachers_taking_advanced_training_courses")
);

CREATE TABLE IF NOT EXISTS "work_with_teachers_taking_advanced_training_courses"(
"id_oo" INTEGER NOT NULL,
"id_description_of_work_with_teachers_taking_advanced_training_courses" INTEGER NOT NULL,
"value" VARCHAR (10) NOT NULL,
CONSTRAINT "K19" PRIMARY KEY ("id_oo", "id_description_of_work_with_teachers_taking_advanced_training_courses"),
CONSTRAINT "C21" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C20" FOREIGN KEY ("id_description_of_work_with_teachers_taking_advanced_training_courses")
    REFERENCES "description_of_work_with_teachers_taking_advanced_training_courses" ("id_description_of_work_with_teachers_taking_advanced_training_courses")
);

CREATE TABLE IF NOT EXISTS "description_of_career_guidance"(
"id_description_of_career_guidance" SERIAL,
"description" VARCHAR (55) NOT NULL,
CONSTRAINT "K21" PRIMARY KEY ("id_description_of_career_guidance")
);

CREATE TABLE IF NOT EXISTS "oo_description_of_career_guidance"(
"id_oo" INTEGER NOT NULL,
"id_description_of_career_guidance" INTEGER NOT NULL,
"value" VARCHAR (10) NOT NULL,
CONSTRAINT "K22" PRIMARY KEY ("id_oo", "id_description_of_career_guidance"),
CONSTRAINT "C24" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C23" FOREIGN KEY ("id_description_of_career_guidance")
    REFERENCES "description_of_career_guidance" ("id_description_of_career_guidance")
);

CREATE TABLE IF NOT EXISTS "levels_of_the_educational_program"(
"id_levels_of_the_educational_program" SERIAL,
"educational_program" VARCHAR (40) NOT NULL,
CONSTRAINT "K23" PRIMARY KEY ("id_levels_of_the_educational_program")
);

CREATE TABLE IF NOT EXISTS "oo_levels_of_the_educational_program"(
"id_oo" INTEGER NOT NULL,
"id_levels_of_the_educational_program" INTEGER NOT NULL,
"value" VARCHAR (10) NOT NULL,
CONSTRAINT "K25" PRIMARY KEY ("id_oo", "id_levels_of_the_educational_program"),
CONSTRAINT "C28" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C27" FOREIGN KEY ("id_levels_of_the_educational_program")
    REFERENCES "levels_of_the_educational_program" ("id_levels_of_the_educational_program")
);

CREATE TABLE IF NOT EXISTS "percentage_of_parents_attending_parentteacher_meeting"(
"id_oo" INTEGER NOT NULL,
"id_levels_of_the_educational_program" INTEGER NOT NULL,
"value" INTEGER NOT NULL,
CONSTRAINT "K24" PRIMARY KEY ("id_oo", "id_levels_of_the_educational_program"),
CONSTRAINT "C25" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C26" FOREIGN KEY ("id_levels_of_the_educational_program")
    REFERENCES "levels_of_the_educational_program" ("id_levels_of_the_educational_program")
);

CREATE TABLE IF NOT EXISTS "parallels"(
"parallel" INTEGER NOT NULL,
CONSTRAINT "K44" PRIMARY KEY ("parallel")
);

CREATE TABLE IF NOT EXISTS "oo_parallels"(
"id_oo_parallels" SERIAL,
"parallel" INTEGER NOT NULL,
"id_oo" INTEGER NOT NULL,
CONSTRAINT "K3" PRIMARY KEY ("id_oo_parallels"),
CONSTRAINT "C4" FOREIGN KEY ("id_oo")
    REFERENCES "oo" ("id_oo"),
CONSTRAINT "C9" FOREIGN KEY ("parallel")
    REFERENCES "parallels" ("parallel")
);

CREATE TABLE IF NOT EXISTS "classes"(
"id_classes" SERIAL,
"id_oo_parallels" INTEGER NOT NULL,
"liter" VARCHAR(10) NOT NULL,
CONSTRAINT "K7" PRIMARY KEY ("id_classes","id_oo_parallels"),
CONSTRAINT "C46" FOREIGN KEY ("id_oo_parallels")
    REFERENCES "oo_parallels" ("id_oo_parallels")
);

CREATE TABLE IF NOT EXISTS "subjects"(
"id_subjects" SERIAL,
"subject_name" VARCHAR(20) NOT NULL,
CONSTRAINT "K6" PRIMARY KEY ("id_subjects")
);

CREATE TABLE IF NOT EXISTS "textbooks"(
"id_textbooks" SERIAL,
"id_subjects" INTEGER NOT NULL,
"key" VARCHAR(20) NOT NULL,
"name" VARCHAR(300) NOT NULL,
CONSTRAINT "K10" PRIMARY KEY ("id_textbooks"),
CONSTRAINT "C14" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects")
);

CREATE TABLE IF NOT EXISTS "classes_textbooks"(
"id_classes" INTEGER NOT NULL,
"id_textbooks" INTEGER NOT NULL,
"id_oo_parallels" INTEGER NOT NULL,
CONSTRAINT "K9" PRIMARY KEY ("id_classes","id_textbooks", "id_oo_parallels"),
CONSTRAINT "C7" FOREIGN KEY ("id_classes","id_oo_parallels")
    REFERENCES "classes" ("id_classes","id_oo_parallels"),
CONSTRAINT "C8" FOREIGN KEY ("id_textbooks")
    REFERENCES "textbooks" ("id_textbooks")
);


CREATE TABLE IF NOT EXISTS "students"(
"id_students" SERIAL,
"id_oo_parallels" INTEGER NOT NULL,
"id_classes" INTEGER NOT NULL,
"gender" VARCHAR(10) NOT NULL,
"student_number" INTEGER NOT NULL,
CONSTRAINT "K13" PRIMARY KEY ("id_students","id_oo_parallels"),
CONSTRAINT "C11" FOREIGN KEY ("id_oo_parallels","id_classes")
    REFERENCES "classes" ("id_oo_parallels","id_classes")
);

CREATE TABLE IF NOT EXISTS "oo_parallels_subjects"(
"id_oo_parallels_subjects" SERIAL,
"id_subjects" INTEGER NOT NULL,
"id_oo_parallels" INTEGER NOT NULL,
"mark_three" INTEGER NOT NULL,
"mark_four" INTEGER NOT NULL,
"mark_five" INTEGER NOT NULL,
CONSTRAINT "K8" PRIMARY KEY ("id_oo_parallels_subjects","id_subjects","id_oo_parallels"),
CONSTRAINT "C6" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects"),
CONSTRAINT "C5" FOREIGN KEY ("id_oo_parallels")
    REFERENCES "oo_parallels" ("id_oo_parallels")
);

CREATE TABLE IF NOT EXISTS "result_for_task"(
"id_result_for_task" SERIAL,
"task_number" INTEGER NOT NULL,
"id_oo_parallels_subjects" INTEGER NOT NULL,
"id_students" INTEGER NOT NULL,
"id_oo_parallels" INTEGER NOT NULL,
"id_subjects" INTEGER NOT NULL,
"variant" INTEGER NOT NULL,
"mark_for_last_semester" INTEGER NOT NULL,
"mark" INTEGER NOT NULL,
parallel INTEGER NOT NULL,
id_distributio_of_tasks_by_positions_of_codifiers INTEGER NOT NULL,
CONSTRAINT "K14" PRIMARY KEY ("id_result_for_task","task_number"),
CONSTRAINT "C13" FOREIGN KEY ("id_oo_parallels_subjects","id_oo_parallels","id_subjects")
    REFERENCES "oo_parallels_subjects" ("id_oo_parallels_subjects","id_oo_parallels","id_subjects"),
CONSTRAINT "C12" FOREIGN KEY ("id_students","id_oo_parallels")
    REFERENCES "students" ("id_students","id_oo_parallels"),
CONSTRAINT "C47" FOREIGN KEY (id_distributio_of_tasks_by_positions_of_codifiers, parallel, id_subjects, task_number)
    REFERENCES "distributio_of_tasks_by_positions_of_codifiers" (id_distributio_of_tasks_by_positions_of_codifiers, parallel, id_subjects, task_number)
);

CREATE TABLE IF NOT EXISTS "distributio_of_tasks_by_positions_of_codifiers"(
"id_distributio_of_tasks_by_positions_of_codifiers" SERIAL,
"id_subjects" INTEGER NOT NULL,
"parallel" INTEGER NOT NULL,
"task_number" INTEGER NOT NULL,
"task_number_from_kim" VARCHAR (10),
"fgos" text,
"poop_noo" text,
"level" text,
"max_mark" INTEGER NOT NULL,
UNIQUE (id_subjects, parallel, task_number, task_number_from_kim),
CONSTRAINT "K41" PRIMARY KEY ("id_distributio_of_tasks_by_positions_of_codifiers","id_subjects","parallel","task_number"),
CONSTRAINT "C42" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects"),
CONSTRAINT "C50" FOREIGN KEY ("parallel")
    REFERENCES "parallels" ("parallel")
);


CREATE TABLE IF NOT EXISTS "ks"(
"id_ks" SERIAL,
"ks_key" VARCHAR (10),
"id_subjects" INTEGER NOT NULL,
"parallel" INTEGER NOT NULL,
"description" text,
CONSTRAINT "K39" PRIMARY KEY ("id_ks","id_subjects","parallel"),
CONSTRAINT "C40" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects"),
CONSTRAINT "C48" FOREIGN KEY ("parallel")
    REFERENCES "parallels" ("parallel")
);

CREATE TABLE IF NOT EXISTS "kt"(
"id_kt" SERIAL,
"kt_key" VARCHAR (10),
"id_subjects" INTEGER NOT NULL,
"parallel" INTEGER NOT NULL,
"description" text,
CONSTRAINT "K40" PRIMARY KEY ("id_kt","id_subjects","parallel"),
CONSTRAINT "C41" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects"),
CONSTRAINT "C49" FOREIGN KEY ("parallel")
    REFERENCES "parallels" ("parallel")
);

CREATE TABLE IF NOT EXISTS "ks_kt"(
"id_distributio_of_tasks_by_positions_of_codifiers" INTEGER NOT NULL,
"id_subjects" INTEGER NOT NULL,
"parallel" INTEGER NOT NULL,
"id_ks" INTEGER,
"id_kt" INTEGER,
"task_number" INTEGER NOT NULL,
CONSTRAINT "K42" PRIMARY KEY ("id_distributio_of_tasks_by_positions_of_codifiers","id_ks","id_kt","id_subjects","parallel","task_number"),
CONSTRAINT "C43" FOREIGN KEY ("id_kt","id_subjects","parallel")
    REFERENCES "kt" ("id_kt","id_subjects","parallel"),
CONSTRAINT "C44" FOREIGN KEY ("id_ks","id_subjects","parallel")
    REFERENCES "ks" ("id_ks","id_subjects","parallel"),
CONSTRAINT "C45" FOREIGN KEY ("id_distributio_of_tasks_by_positions_of_codifiers","id_subjects","parallel","task_number")
    REFERENCES "distributio_of_tasks_by_positions_of_codifiers" ("id_distributio_of_tasks_by_positions_of_codifiers","id_subjects","parallel","task_number")
);

CREATE TABLE IF NOT EXISTS "indepth_study_of_subjects"(
"id_oo_parallels" INTEGER NOT NULL,
"id_subjects" INTEGER NOT NULL,
CONSTRAINT "K20" PRIMARY KEY ("id_subjects","id_oo_parallels"),
CONSTRAINT "C15" FOREIGN KEY ("id_subjects")
    REFERENCES "subjects" ("id_subjects"),
CONSTRAINT "C51" FOREIGN KEY ("id_oo_parallels")
    REFERENCES "oo_parallels" ("id_oo_parallels")
);


CREATE TABLE IF NOT EXISTS roles(
id_role SERIAL,
role text NOT NULL,
UNIQUE (role),
CONSTRAINT "K11" PRIMARY KEY (id_role)
);

CREATE TABLE IF NOT EXISTS users(
id_user  SERIAL,
login text NOT NULL,
name text NOT NULL,
email text DEFAULT NULL,
phone VARCHAR(12) DEFAULT NULL,
password text NOT NULL,
avatar bytea DEFAULT NULL,
id_role INTEGER NOT NULL,
time integer NOT NULL,
UNIQUE (login),
CONSTRAINT "K12" PRIMARY KEY (id_user),
CONSTRAINT "C10" FOREIGN KEY (id_role)
    REFERENCES roles (id_role)
);

CREATE TABLE IF NOT EXISTS users_oo_logins(
id_user INTEGER NOT NULL,
oo_login VARCHAR(20) NOT NULL,
CONSTRAINT "K28" PRIMARY KEY (id_user, oo_login),
CONSTRAINT "C16" FOREIGN KEY (id_user)
    REFERENCES users (id_user),
CONSTRAINT "C17" FOREIGN KEY (oo_login)
    REFERENCES oo_logins (oo_login)
);
