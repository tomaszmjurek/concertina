from datetime import date, timedelta

guitar = Instruments.create('Guitar')
drums = Instruments.create('Drums')
vocal = Instruments.create('Vocal')
bass = Instruments.create('Kass')
keyboard = Instruments.create('Keyboard')

fusion = Genres.create('Fusion')
blues = Genres.create('Blues')
rock = Genres.create('Rock')
soft_rock = Genres.create('Soft rock', rock)
psychodelic_rock = Genres.create('Psychodelic Rock', rock)
progressive_rock = Genres.create('Progressive Rock', rock)

stadium = Places.create('Stadium', 'Poznan', 'Bulgarska 17')
arena = Places.create('Arena', 'Poznan', 'Stanislawa Wyspianskiego 33')
blue_note = Places.create('Blue Note', 'Poznan', 'Kosciuszki 79')
u_bazyla = Places.create('U Bazyla', 'Poznan', 'Norwida 18A')

## ROLLING STONES

rolling_stones = Bands.create('The Rolling Stones', date(1962, 1, 1))

jagger = Musicians.create('Mick Jagger', rolling_stones, vocal)
richards = Musicians.create('Keith Richards', rolling_stones, guitar)
wood = Musicians.create('Ron Wood', rolling_stones, bass)
watts = Musicians.create('Charlie Watts', rolling_stones, bass)

blue_and_lonesome = rolling_stones.release_album('Blue and Lonesome', blues)
blue_and_lonesome.add_songs([
    'Just Your Fool', 'Commit a Crime', 'Blue and Lonesome',
    'All of Your Love', 'I Gotta Go', 'Everybody Knows About My Good Thing',
    'RideEm on Down', 'Hate To See You Ho', 'Hoo Doo Blues',
    'Little Rain', 'Just Like I Treat You', ' I Cant Quit You Baby'
])

## CASIOPEA

casiopea = Bands.create('Casiopea', date(1976, 1, 1))


noro = Musicians.create('Issei Noro', casiopea, guitar)
otaka = Musicians.create('Kiyomi Otaka', casiopea, keyboard)
naruse = Musicians.create('Yoshihiko Naruse', casiopea, bass)
jimbo = Musicians.create('Akira Jimbo', casiopea, drums)

casiopea.release_album('Casiopea', fusion)
casiopea.release_album('Super Flight', fusion)
casiopea.release_album('Thunder Live', fusion)
casiopea.release_album('Make Up City', fusion)
casiopea.release_album('Eyes of the Mind', fusion)
casiopea.release_album('Cross Point', fusion)
casiopea.release_album('Mint Jams', fusion)
casiopea.release_album('4x4', fusion)

## CONCERTS

rolling_stones.play_concert(stadium, date.today() + timedelta(days=1))
rolling_stones.play_concert(arena, date.today() + timedelta(days=2))
rolling_stones.play_concert(blue_note, date.today() + timedelta(days=3))
rolling_stones.play_concert(u_bazyla, date.today() + timedelta(days=4))

casiopea.play_concert(stadium, date.today() + timedelta(days=10))
casiopea.play_concert(arena, date.today() + timedelta(days=11))
casiopea.play_concert(blue_note, date.today() + timedelta(days=12))
casiopea.play_concert(u_bazyla, date.today() + timedelta(days=13))
    casiopea.play_concert(u_bazyla, date.today() + timedelta(days=i))