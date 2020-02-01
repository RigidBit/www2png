--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

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
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: www2png
--

INSERT INTO public.users (id, email, disabled, "timestamp") VALUES (2, 'support@www2png.com', false, '2020-02-01 14:34:12.268259');


--
-- Data for Name: api_keys; Type: TABLE DATA; Schema: public; Owner: www2png
--

INSERT INTO public.api_keys (id, api_key, user_id, use_count, "timestamp") VALUES (1, 'b813d0a3-f82f-4128-b1b6-a13957a42440', 2, 0, '2020-02-01 14:34:12.268259');


--
-- Data for Name: data; Type: TABLE DATA; Schema: public; Owner: www2png
--

INSERT INTO public.data (id, request_id, url, block_id, user_id, queued, pruned, flagged, removed, failed, "timestamp") VALUES (1, '5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605', 'http://bing.com/', 42154, 1, false, false, false, false, false, '2020-02-01 14:35:56.77072');
INSERT INTO public.data (id, request_id, url, block_id, user_id, queued, pruned, flagged, removed, failed, "timestamp") VALUES (2, 'ed0ccb03-0d69-425b-a1d7-e8cea3bd2420', 'http://google.com/', 0, 1, true, false, false, false, false, '2020-02-01 14:36:49.218941');


--
-- Data for Name: unverified_users; Type: TABLE DATA; Schema: public; Owner: www2png
--

INSERT INTO public.unverified_users (id, email, challenge, "timestamp") VALUES (1, 'test@www2png.com', '8723971f-b44b-4d83-aead-634d7e6b2eac', '2020-02-01 14:33:54.882009');


--
-- Name: api_keys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: www2png
--

SELECT pg_catalog.setval('public.api_keys_id_seq', 1, true);


--
-- Name: data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: www2png
--

SELECT pg_catalog.setval('public.data_id_seq', 2, true);


--
-- Name: unverified_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: www2png
--

SELECT pg_catalog.setval('public.unverified_users_id_seq', 2, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: www2png
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

