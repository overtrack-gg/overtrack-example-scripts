
# OverTrack Teamcomp Data Extraction

This script creates CSV output of the teamcomp and game result of all games from a specified share link.
Each line is `'teamcomp', 'result', 'SR change' (if known)`.

The `teamcomp` string of each player's most-played-hero separated by an underscore, then sorted alphabetically by hero name
e.g. 
`mccree_mercy_pharah_reinhardt_roadhog_zarya`
 

Example use
```bash
python my-games-teamcomps.py
OverTrack share key? eeveea
```

Output
```csv
dva_mercy_roadhog_s76_sombra_zenyatta, WIN, 22
ana_junkrat_mercy_reinhardt_tracer_zarya, LOSS, -31
genji_mercy_reinhardt_torb_tracer_zenyatta, WIN, 22
mercy_orisa_roadhog_torb_tracer_zenyatta, WIN, 20
...
```
