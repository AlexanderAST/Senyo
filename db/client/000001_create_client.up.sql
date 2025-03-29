CREATE table clients(
    id bigserial not null primary key,
    surname varchar not null, 
    name varchar not null,
    phone VARCHAR(20) NOT NULL CHECK (phone ~ '^\+?[0-9]{8,15}$'),
    id_gender int,
    login varchar not null,
    password varchar not null,
    FOREIGN KEY (id_gender) REFERENCES gender(id)
);