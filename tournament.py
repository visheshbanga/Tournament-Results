#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db,c
    except:
        print("Error in connecting to database")

def deleteMatches():
    """Remove all the match records from the database."""
    db,c = connect()
    query = "TRUNCATE TABLE matches RESTART IDENTITY CASCADE"
    c.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db,c = connect();
    query = "TRUNCATE TABLE players RESTART IDENTITY CASCADE"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db,c = connect();
    c.execute("select count(name) from players")
    count = c.fetchone()[0]
    db.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db,c = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    c.execute(query, parameter)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db,c = connect()
    c.execute("select * from standings")
    standings = c.fetchall()
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db,c = connect()
    c.execute("insert into matches(winner,loser) values(%s,%s)", (winner, loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    pairings = []

    for i in range(0, len(standings), 2):
        pair = (standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1])
        pairings.append(pair)

    return pairings
