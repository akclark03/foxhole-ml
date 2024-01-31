--
-- PostgreSQL database dump
--

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: ndustrial
--

-- *not* creating schema, since initdb creates it

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dynamic_data; Type: TABLE; Schema: public;
--

CREATE TABLE public.dynamic_data (
    map varchar NOT NULL,
    "time" timestamp with time zone NOT NULL,
    dynamic_data jsonb,
    report jsonb
);

--
-- PostgreSQL database dump complete
--