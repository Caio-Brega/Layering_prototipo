-- Schema do protótipo de layering de perfumes
-- Rodar via pgAdmin4 (ou psql) para criar/recriar o banco

DROP TABLE IF EXISTS perfume_notes CASCADE;
DROP TABLE IF EXISTS perfume_accords CASCADE;
DROP TABLE IF EXISTS notes CASCADE;
DROP TABLE IF EXISTS accords CASCADE;
DROP TABLE IF EXISTS perfumes CASCADE;

CREATE TABLE perfumes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    brand VARCHAR(150) NOT NULL,
    fragrantica_url VARCHAR(500) UNIQUE,
    gender VARCHAR(20),
    UNIQUE (name, brand)
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE accords (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- notas com posição na pirâmide (top/middle/base) e proeminência (opacity)
CREATE TABLE perfume_notes (
    perfume_id INT REFERENCES perfumes(id) ON DELETE CASCADE,
    note_id INT REFERENCES notes(id) ON DELETE CASCADE,
    position VARCHAR(10) CHECK (position IN ('top', 'middle', 'base')),
    prominence FLOAT DEFAULT 1.0,
    PRIMARY KEY (perfume_id, note_id, position)
);

-- acordes com força (width %)
CREATE TABLE perfume_accords (
    perfume_id INT REFERENCES perfumes(id) ON DELETE CASCADE,
    accord_id INT REFERENCES accords(id) ON DELETE CASCADE,
    strength FLOAT DEFAULT 1.0,
    PRIMARY KEY (perfume_id, accord_id)
);