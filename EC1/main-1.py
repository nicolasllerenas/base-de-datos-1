import pandas as pd

def main():
    # Cargar datos
    world_cups = pd.read_csv('WorldCups.csv')
    world_cup_matches = pd.read_csv('WorldCupMatches.csv')
    world_cup_players = pd.read_csv('WorldCupPlayers.csv')
    
    print("=" * 60)
    print("C1: Paraguay en Copas Mundiales")
    print("=" * 60)
    paraguay_matches = world_cup_matches[
        (world_cup_matches['Home Team Name'] == 'Paraguay') | 
        (world_cup_matches['Away Team Name'] == 'Paraguay')
    ]
    years = sorted(paraguay_matches['Year'].unique())
    print(f"Participó en {len(years)} Copas: {', '.join(map(str, [int(y) for y in years]))}")
    
    print("\n" + "=" * 60)
    print("C2: Argentina vs Chile")
    print("=" * 60)
    argentina_chile = world_cup_matches[
        ((world_cup_matches['Home Team Name'] == 'Argentina') &
         (world_cup_matches['Away Team Name'] == 'Chile')) |
        ((world_cup_matches['Home Team Name'] == 'Chile') &
         (world_cup_matches['Away Team Name'] == 'Argentina'))]
    encounters_count = len(argentina_chile)
    print(f"Argentina vs Chile: {encounters_count} vez")
    
    print("\n" + "=" * 60)
    print("C3: Final 2010")
    print("=" * 60)
    final_2010 = world_cup_matches[(world_cup_matches['Year'] == 2010) & (world_cup_matches['Stage'] == 'Final')].iloc[0]

    if final_2010['Home Team Goals'] > final_2010['Away Team Goals']:
        winner_name = final_2010['Home Team Name']
        winner_initials = final_2010['Home Team Initials']
    else:
        winner_name = final_2010['Away Team Name']
        winner_initials = final_2010['Away Team Initials']

    print(f"El ganador de la final de la copa del mundo en 2010 fue {winner_name}.")

    match_id = final_2010['MatchID']
    starters = world_cup_players[
        (world_cup_players['MatchID'] == match_id) &
        (world_cup_players['Team Initials'] == winner_initials) &
        (world_cup_players['Line-up'] == 'S')
    ]

    print("11 titulares:")
    for i, player in enumerate(starters['Player Name'].tolist(), 1):
        print(f"  {i}. {player}")

    print("\n" + "=" * 60)
    print("C4: RONALDINHO")
    print("=" * 60)
    
    ronaldinho = world_cup_players[world_cup_players["Player Name"].str.contains(r"\bRONALDINHO\b")].copy()
    ronaldinho_matches = ronaldinho.merge(world_cup_matches[["MatchID", "Year", "Home Team Name", "Away Team Name", "Stage"]])

    if ronaldinho_matches["Year"].any():
        mundiales_participados = (ronaldinho_matches["Year"].drop_duplicates().sort_values().tolist())
        print("Mundiales en los que participó Ronaldinho:", mundiales_participados)

        suplente = ronaldinho_matches["Line-up"].ne("S")
        suplente_matches = (ronaldinho_matches.loc[suplente,["Year", "Stage", "Home Team Name", "Away Team Name"]]
                            .sort_values(["Year", "Stage", "Home Team Name", "Away Team Name"]).drop_duplicates())

        print("\nPartidos donde Ronaldinho inicio como suplente:")
        for _, match in suplente_matches.iterrows():
            print(f"  {int(match['Year'])} - {match['Stage']}: {match['Home Team Name']} vs {match['Away Team Name']}")

    print("\n" + "=" * 60)
    print("C5: Entrenador más Copas")
    print("=" * 60)
    
    players_with_years = world_cup_players.merge(world_cup_matches[['MatchID', 'Year']], on='MatchID', how='left')
    coach_years = players_with_years.groupby('Coach Name')['Year'].nunique().sort_values(ascending=False)
    top_coach = coach_years.index[0]
    top_coach_years = coach_years.iloc[0]
    
    print(f"El entrenador que ha asistido a más Copas Mundiales es: {top_coach}")
    print(f"Total: {top_coach_years} Copas Mundiales")
    
    years_participated = players_with_years[players_with_years['Coach Name'] == top_coach]['Year'].unique()
    years_sorted = sorted(years_participated)
    print(f"Años: {', '.join(map(str, [int(y) for y in years_sorted]))}")

    print("\n" + "=" * 60)
    print("C6: Campeones México 70")
    print("=" * 60)
    
    winner_1970 = world_cups[world_cups['Year'] == 1970].iloc[0]['Winner']
    print(f"Campeón: {winner_1970}")
    
    match_ids = world_cup_matches[(world_cup_matches['Year'] == 1970) & 
                                 ((world_cup_matches['Home Team Name'] == winner_1970) | 
                                  (world_cup_matches['Away Team Name'] == winner_1970))]['MatchID'].unique()
    
    players = world_cup_players[(world_cup_players['MatchID'].isin(match_ids)) & 
                               (world_cup_players['Team Initials'] == 'BRA')]['Player Name'].unique()
    
    print(f"Total de jugadores: {len(players)}")
    print(f"Partidos jugados: {len(match_ids)}")
    
    print("\nJugadores campeones:")
    for i, player in enumerate(sorted(players), 1):
        print(f"  {i}. {player}")

if __name__ == "__main__":
    main()