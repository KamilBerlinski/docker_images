CREATE TABLE pracownicy (
    id SERIAL PRIMARY KEY,
    imie VARCHAR(50),
    stanowisko VARCHAR(50)
);

INSERT INTO pracownicy (imie, stanowisko) VALUES 
('Kamil', 'Data Platform Engineer'),
('Jan', 'Analityk'),
('Anna', 'PM');