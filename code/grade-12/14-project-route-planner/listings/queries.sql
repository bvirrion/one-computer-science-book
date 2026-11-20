-- load: town
SELECT kind, COUNT(*) AS places FROM places GROUP BY kind ORDER BY places DESC, kind LIMIT 4;
SELECT r.road_id, a.name AS from_name, b.name AS to_name, r.length_m, r.speed_kmh
FROM roads AS r
  JOIN places AS a ON r.from_place = a.place_id
  JOIN places AS b ON r.to_place = b.place_id
ORDER BY r.length_m DESC LIMIT 3;
SELECT ROUND(SUM(length_m) / 1000.0, 2) AS km_of_road FROM roads;
