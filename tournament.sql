-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop existing database
DROP DATABASE IF EXISTS tournament;

-- Create Database
CREATE DATABASE tournament;

\c tournament;

-- Create players table
CREATE TABLE players ( id serial primary key, name text );

-- Create matches tables
CREATE TABLE matches (
    id serial primary key,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id)
);

CREATE VIEW standings AS SELECT players.id, players.name,
(SELECT count(matches.winner) FROM matches WHERE players.id = matches.winner) AS wins,
(SELECT count(matches.id) FROM matches WHERE players.id = matches.winner OR players.id = matches.loser) AS matches
FROM players GROUP BY players.id ORDER BY wins DESC;
