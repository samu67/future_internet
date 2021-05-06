in src.py, i first try the grid solution by reading sat_links.txt into a 2d list with orbit_id and sat_id_in_orbit as index.
output would be for each sat the next in the same orbit and the sat with the same id in the next orbit.
for the second attempt, i read all valid_isls and peack 1600 randomly. prefering to output longer valid links improves the score.
we keep track of how many links each sats have with a list, check in each round of peaking a link, how many links each sats already have.
that's it.
