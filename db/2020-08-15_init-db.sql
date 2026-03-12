CREATE TABLE person (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    company_name VARCHAR NOT NULL
);


CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    coordinate GEOMETRY NOT NULL,
    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (person_id) REFERENCES person(id)
);
CREATE INDEX coordinate_idx ON location (coordinate);
CREATE INDEX creation_time_idx ON location (creation_time);



CREATE TABLE connection (
    id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    exposed_person_id INT NOT NULL,
    location_id INT NOT NULL,
    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (person_id) REFERENCES person(id),
    FOREIGN KEY (exposed_person_id) REFERENCES person(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);

CREATE INDEX connection_person_idx ON connection (person_id);
CREATE INDEX connection_exposed_person_idx ON connection (exposed_person_id);
