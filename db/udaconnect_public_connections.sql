INSERT INTO connection (person_id, exposed_person_id, location_id, creation_time)
SELECT 
    l1.person_id, 
    l2.person_id, 
    l2.id, 
    l2.creation_time
FROM location l1
JOIN location l2 
  ON l1.person_id < l2.person_id  -- Evita duplicados (A,B) y (B,A)
  AND l1.creation_time = l2.creation_time -- Coincidencia exacta de tiempo
WHERE ST_DWithin(
    ST_SetSRID(l1.coordinate, 4326)::geography, 
    ST_SetSRID(l2.coordinate, 4326)::geography, 
    5 -- 5 metros de radio
)
ON CONFLICT (person_id, exposed_person_id, location_id) 
DO NOTHING; -- Si ya existe la conexión, ignórala y sigue adelante
