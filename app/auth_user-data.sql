--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Ubuntu 15.2-1.pgdg22.04+1)
-- Dumped by pg_dump version 15.2 (Ubuntu 15.2-1.pgdg22.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: lockhart_r
--

INSERT INTO public.auth_user VALUES (1, 'pbkdf2_sha256$390000$9M9JA7M8idZVfZsb6oZSZo$SPbR5SNvGFUqdQZujO1QXZUjue3F9ZsoQfVrFieC+K4=', '2023-03-09 19:57:18.304477+00', true, 'lockhart_r', '', '', 'rob.lockhart@yahoo.co.uk', true, true, '2023-03-08 13:56:24.726372+00');
INSERT INTO public.auth_user VALUES (2, 'pbkdf2_sha256$390000$lZ5nOHK3Nwtferh8oHERGi$BpFkGhGG/AnuLuAXheT+Cp6Xc8MYbPc7z0VIuk5OjCQ=', '2023-03-10 12:45:33.275313+00', true, 'admin', '', '', 'rob.lockhart@yahoo.co.uk', true, true, '2023-03-10 12:44:27.800197+00');
INSERT INTO public.auth_user VALUES (3, 'fgsfg8sfg5fgfsgzf', NULL, true, 'admin1', 'rob', 'craig', 'rob.lockhart@yahoo.co.uk', true, true, '2023-03-10 12:44:27.800197+00');
INSERT INTO public.auth_user VALUES (4, 'fgsfg8sfg5fgfsgzf', '2023-03-09 19:57:18.304477+00', true, 'admin2', 'rob', 'craig', 'rob.lockhart@yahoo.co.uk', true, true, '2023-03-10 12:44:27.800197+00');


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lockhart_r
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

