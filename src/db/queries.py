# TEAMS
GET_TEAM_IDS_BY_IDS_QUERY = """
  SELECT team_id
  FROM teams
  WHERE team_id IN (%s)
  """

GET_TEAMS_QUERY = """
    SELECT
        t.team_id AS team_id,
        t.name AS name,
        t.nickname AS nickname,
        t.logo as logo,
        (SELECT JSON_ARRAYAGG(s.name)
          FROM sponsors s
          JOIN sponsors_graph sg ON s.sponsor_id = sg.sponsor_id
          WHERE sg.team_id = t.team_id) AS sponsors,
        (SELECT JSON_ARRAYAGG(
          JSON_OBJECT(
              'team_id', pm.team_id,
              'name', p.name,
              'number', p.number,
              'position', p.position)
            ) AS players
          FROM players_map pm
          inner join players p on pm.player_id = p.player_id
          where pm.team_id = p.team_id
        ) AS players
    FROM teams t
  """

# VIEWED TEAMS
GET_VIEWED_TEAMS_QUERY = """
    SELECT
        CONVERT_TZ(date_updated, @@session.time_zone, '+00:00') AS date_updated,
        teams
    FROM user_viewed_teams
    WHERE email = %s
  """

UPDATE_VIEWED_TEAMS_QUERY = """
    INSERT INTO user_viewed_teams (email, date_updated, teams)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        date_updated = VALUES(date_updated),
        teams = VALUES(teams)
    """
