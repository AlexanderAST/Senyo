create table promotion(
    id bigserial not null primary key,
    title varchar not null,
    description varchar, 
    added_points NUMERIC(10, 2),
    id_gender int,
    start_date date,
    expiration_date date,
    FOREIGN KEY (id_gender) REFERENCES gender(id)
);