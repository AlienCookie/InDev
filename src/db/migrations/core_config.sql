--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = public, pg_catalog;


CREATE TABLE gp (
    schema_version integer NOT NULL
);


INSERT INTO gp VALUES (1);

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "user" (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    username character varying(255),
    avatar_url character varying(255),
    name character varying(255),
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    email character varying(255),
    password character varying(255)
);

--
-- Name: message; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE message (
    id uuid DEFAULT get_ramndom_uuid() NOT NULL,
    sender uuid NOT NULL,
    receiver uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    data text NOT NULL
);

--
-- Name: post; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE post (
    id uuid DEFAULT get_ramndom_uuid() NOT NULL,
    owner uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    data text NOT NULL
);

--
-- Name: "connection"; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "connection" (
    id uuid DEFAULT get_ramndom_uuid() NOT NULL,
    follower uuid NOT NULL,
    connected_user uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
);

--
-- Name: chat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE chat (
    name string NOT NULL,
    connected_user uuid NOT NULL,
    connected_at timestamp with time zone DEFAULT now() NOT NULL,
);

--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: message_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--
ALTER TABLE ONLY message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;