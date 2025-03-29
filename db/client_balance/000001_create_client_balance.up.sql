create table client_balance(
    id bigserial not null primary key,
    id_client int,
    permanent_points numeric(10,2),
    temporary_points numeric(10,2),
    updated_at timestamp,
    FOREIGN key(id_client) REFERENCES clients(id)
);