create table referrals(
    id bigserial not null primary key,
    id_client int,
    referral_phone VARCHAR(20) NOT NULL CHECK (phone ~ '^\+?[0-9]{8,15}$'),
    is_active boolean,
    FOREIGN KEY (id_client) REFERENCES clients(id)
);