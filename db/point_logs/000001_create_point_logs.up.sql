create table point_logs(
    id bigserial primary key not null;
    id_client int,
    id_point_type int,
    points numeric(10,2),
    id_direction int,
    id_type_accural int,
    expiratoin_date date,
    created_at timestamp,
    FOREIGN key(id_client) REFERENCES clients(id),
    FOREIGN key(id_point_type) REFERENCES point_type(id),
    FOREIGN key(id_direction) REFERENCES direction(id),
    FOREIGN key(id_type_accural) REFERENCES type_accural(id)
);
