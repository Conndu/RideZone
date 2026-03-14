--
-- PostgreSQL database dump
--

\restrict FAgWuAVdHYmFLTeiaZPsLh8jpkb1gAYYFAy5YIb9mn1aeXqUyv9NDoD0MggV6St

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_categorie; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_categorie (id, nume, descriere, culoare_identificare) VALUES (1, 'Chopper', 'Tip de motocicleta, cu o pozitie comoda, mai lenta, des intalnita in SUA', '#000000');
INSERT INTO django.magazin_moto_categorie (id, nume, descriere, culoare_identificare) VALUES (2, 'Sport', 'Viteza si performanta', '#DC143C');
INSERT INTO django.magazin_moto_categorie (id, nume, descriere, culoare_identificare) VALUES (3, 'Touring', 'Confort pentru distante lungi', '#1E90FF');


--
-- Name: magazin_moto_categorie_id_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_categorie_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict FAgWuAVdHYmFLTeiaZPsLh8jpkb1gAYYFAy5YIb9mn1aeXqUyv9NDoD0MggV6St

--
-- PostgreSQL database dump
--

\restrict 4YNmdSSy2zEIsJLqA9cXSieYoJHnjMRYUljHT5s15AESvsihgbaIEvTlFA7mQf1

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_furnizor; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_furnizor (id_furnizor, nume, tara_origine, email) VALUES (1, 'Brembo', 'Italia', 'contact@brembo.com');
INSERT INTO django.magazin_moto_furnizor (id_furnizor, nume, tara_origine, email) VALUES (2, 'Ohlins', 'Suedia', 'contact@ohlins.com');
INSERT INTO django.magazin_moto_furnizor (id_furnizor, nume, tara_origine, email) VALUES (3, 'Akrapovic', 'Slovenia', 'contact@akrapovic.com');
INSERT INTO django.magazin_moto_furnizor (id_furnizor, nume, tara_origine, email) VALUES (4, 'Michelin', 'Franta', 'contact@michelin.com');


--
-- Name: magazin_moto_furnizor_id_furnizor_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_furnizor_id_furnizor_seq', 4, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 4YNmdSSy2zEIsJLqA9cXSieYoJHnjMRYUljHT5s15AESvsihgbaIEvTlFA7mQf1

--
-- PostgreSQL database dump
--

\restrict luiltPodofwC0aTiZqkUnfekKvPKCvLXtfiKbLtakoQ6fIUNb9ehdezTMaecLSw

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_marca; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_marca (id_marca, nume, data_creare, tara_origine, fondator, descriere) VALUES (1, 'Yamaha', '1955-06-01', 'Japonia', 'Genichi Kawakami', 'Brand nipon de motociclete, cunoscut in toata lumea pentru confort si performanta.');
INSERT INTO django.magazin_moto_marca (id_marca, nume, data_creare, tara_origine, fondator, descriere) VALUES (2, 'Ducati', '1926-01-01', 'Italia', 'Antonio Cavalieri Ducati', 'Brand italienesc, cunoscut pentru rafinamentul cu care produc motoarele.');
INSERT INTO django.magazin_moto_marca (id_marca, nume, data_creare, tara_origine, fondator, descriere) VALUES (3, 'BMW Motorrad', '1916-03-07', 'Germania', 'Karl Rapp', 'Cunoscut pentru inovatia si ingineria germana de top, BMW Motorrad aduc mereu plusuri industriei moto.');


--
-- Name: magazin_moto_marca_id_marca_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_marca_id_marca_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict luiltPodofwC0aTiZqkUnfekKvPKCvLXtfiKbLtakoQ6fIUNb9ehdezTMaecLSw

--
-- PostgreSQL database dump
--

\restrict qaWX6VY2GjRR8IhlcYAYiTG63ExigZ8zx5SSiNjia4Oi6L5XihDS59iI8kWxXvt

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_motor; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_motor (id_motor, tip, capacitate_cc, consum, putere_cp) VALUES (1, 'Boxer ShiftCam', 1254, 4.8, 136);
INSERT INTO django.magazin_moto_motor (id_motor, tip, capacitate_cc, consum, putere_cp) VALUES (2, 'CP4 Crossplane', 998, 7.2, 200);
INSERT INTO django.magazin_moto_motor (id_motor, tip, capacitate_cc, consum, putere_cp) VALUES (3, 'V4 Granturismo', 1158, 6.5, 170);
INSERT INTO django.magazin_moto_motor (id_motor, tip, capacitate_cc, consum, putere_cp) VALUES (4, 'Testatretta Twin', 937, 5.4, 111);


--
-- Name: magazin_moto_motor_id_motor_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_motor_id_motor_seq', 4, true);


--
-- PostgreSQL database dump complete
--

\unrestrict qaWX6VY2GjRR8IhlcYAYiTG63ExigZ8zx5SSiNjia4Oi6L5XihDS59iI8kWxXvt

--
-- PostgreSQL database dump
--

\restrict xmNp9FC15LOhYcj5eyUVhZe1NaRtzc5lbcbp08c6M5vz7haWybD9abthjItabxz

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_piesa; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_piesa (id_piesa, nume, pret, garantie_luni, furnizor_id) VALUES (1, 'Placute Frana Carbon', 150.00, 24, 1);
INSERT INTO django.magazin_moto_piesa (id_piesa, nume, pret, garantie_luni, furnizor_id) VALUES (2, 'Suspensie Fata Gold', 1200.00, 36, 2);
INSERT INTO django.magazin_moto_piesa (id_piesa, nume, pret, garantie_luni, furnizor_id) VALUES (3, 'Sistem Evacuare Full Titanium', 2500.00, 36, 3);
INSERT INTO django.magazin_moto_piesa (id_piesa, nume, pret, garantie_luni, furnizor_id) VALUES (4, 'Set Anvelope Pilot Road 6', 350.00, 12, 4);
INSERT INTO django.magazin_moto_piesa (id_piesa, nume, pret, garantie_luni, furnizor_id) VALUES (5, 'Kit Crash Bar', 200.00, 24, 2);


--
-- Name: magazin_moto_piesa_id_piesa_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_piesa_id_piesa_seq', 5, true);


--
-- PostgreSQL database dump complete
--

\unrestrict xmNp9FC15LOhYcj5eyUVhZe1NaRtzc5lbcbp08c6M5vz7haWybD9abthjItabxz

--
-- PostgreSQL database dump
--

\restrict XF6fBBka41WHqMu8nnLVorUF5pg0sTcR1ccsvl72SmIFZGhl6TZWKdtOjv29RDT

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_motocicleta; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (1, 'YAM001', 'R1', 2024, 21000.00, '2010-02-01', 2, 1, 2);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (2, 'DUCA001', 'Panigale V4', 2023, 28000.00, '2013-02-02', 2, 2, 3);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (3, 'DUCA002', 'Multistrada V4', 2019, 24000.00, '2005-03-05', 3, 2, 3);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (4, 'YAM002', 'Tracer 9', 2022, 12500.00, '2016-02-02', 3, 1, 2);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (5, 'DUCA003', 'Monster', 2020, 11000.00, '2000-01-01', 1, 2, 4);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (6, 'YAM003', 'MT-10', 2021, 16000.00, '2020-02-04', 2, 1, 2);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (7, 'DUCA004', 'Streetfighter', 2022, 22500.00, '2022-02-03', 2, 2, 3);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (8, 'BMW001', 'S 1000 RR', 2024, 21500.00, '2021-06-06', 2, 3, 3);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (9, 'BMW002', 'R 1250 GS', 2023, 25000.00, '2021-06-06', 3, 3, 1);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (10, 'BMW003', 'R 18', 2021, 19000.00, '2015-02-02', 1, 3, 1);
INSERT INTO django.magazin_moto_motocicleta (id_motocicleta, serie_sasiu, model, an_fabricatie, pret, data_introducere, categorie_id, marca_id, motor_id) VALUES (11, 'BMW004', 'M 1000 RR', 2023, 35200.00, '2026-01-14', 2, 3, 1);


--
-- Name: magazin_moto_motocicleta_id_motocicleta_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_motocicleta_id_motocicleta_seq', 11, true);


--
-- PostgreSQL database dump complete
--

\unrestrict XF6fBBka41WHqMu8nnLVorUF5pg0sTcR1ccsvl72SmIFZGhl6TZWKdtOjv29RDT

--
-- PostgreSQL database dump
--

\restrict kEae1Z451qxQ0Bc7QddxAXsOx0e7TGWljN2sts4BhSSLx73h2wdcd9KOkdNPqG5

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: magazin_moto_motocicleta_piese; Type: TABLE DATA; Schema: django; Owner: user_condu
--

INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (1, 1, 2);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (2, 1, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (3, 2, 1);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (4, 2, 2);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (5, 2, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (6, 2, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (7, 3, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (8, 3, 5);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (9, 4, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (10, 4, 5);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (11, 5, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (12, 5, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (13, 5, 5);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (14, 6, 1);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (15, 6, 2);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (16, 6, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (17, 6, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (18, 7, 1);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (19, 7, 2);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (20, 7, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (21, 7, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (22, 8, 1);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (23, 8, 2);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (24, 8, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (25, 8, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (26, 9, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (27, 9, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (28, 9, 5);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (29, 10, 3);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (30, 10, 4);
INSERT INTO django.magazin_moto_motocicleta_piese (id, motocicleta_id, piesa_id) VALUES (31, 10, 5);


--
-- Name: magazin_moto_motocicleta_piese_id_seq; Type: SEQUENCE SET; Schema: django; Owner: user_condu
--

SELECT pg_catalog.setval('django.magazin_moto_motocicleta_piese_id_seq', 31, true);


--
-- PostgreSQL database dump complete
--

\unrestrict kEae1Z451qxQ0Bc7QddxAXsOx0e7TGWljN2sts4BhSSLx73h2wdcd9KOkdNPqG5

