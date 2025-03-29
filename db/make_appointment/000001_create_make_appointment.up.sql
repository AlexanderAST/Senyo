create table make_appointment(
    id bigserial not null primary key,
    id_client int,
    date timestamp,
    title varchar not null,
    id_status_type int,
    final_sum NUMERIC(10, 2),
    FOREIGN KEY (id_client) REFERENCES clients(id),
    FOREIGN KEY (id_status_type) REFERENCES status_type(id)
);