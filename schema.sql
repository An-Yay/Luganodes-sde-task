CREATE TABLE deposits (
    hash VARCHAR PRIMARY KEY,
    block_number INT NOT NULL,
    block_timestamp TIMESTAMP NOT NULL,
    fee VARCHAR,
    pubkey VARCHAR NOT NULL
);