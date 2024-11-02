import csv
import os
import datetime

class Player:
    def __init__(self, name, rating=1200):
        self.name = name
        self.rating = rating

    def update_rating(self, opponent_rating, score):
        K = 32
        expected_score = 1 / (1 + 10 ** ((opponent_rating - self.rating) / 400))
        self.rating += K * (score - expected_score)

def save_to_csv(players, results):
    filename = 'chess_results.csv'
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Data', 'Hora', 'Jogadores', 'Resultados', 'Ratings'])

        jogadores = ', '.join([player.name for player in players])
        resultados = ', '.join(results)
        ratings = ', '.join([str(player.rating) for player in players])

        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d"), 
                         datetime.datetime.now().strftime("%H:%M:%S"), 
                         jogadores, 
                         resultados, 
                         ratings])

def ranking(players):
    return sorted(players, key=lambda x: x.rating, reverse=True)

def main():
    players = []

    while True:
        print("1. Adicionar jogador")
        print("2. Jogar")
        print("3. Ranking")
        print("4. Sair")
        print("5. Limpar ranking")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            name = input("Digite o nome do jogador: ")
            players.append(Player(name))
        elif escolha == "2":
            if len(players) < 2:
                print("Adicione mais jogadores.")
                continue

            results = []
            for i in range(len(players)):
                for j in range(i+1, len(players)):
                    result = input(f"Resultado da partida entre {players[i].name} e {players[j].name} (1/0/2): ")
                    results.append(f"{players[i].name} vs {players[j].name}: {result}")

                    if result == "1":
                        players[i].update_rating(players[j].rating, 1)
                        players[j].update_rating(players[i].rating, 0)
                    elif result == "2":
                        players[i].update_rating(players[j].rating, 0)
                        players[j].update_rating(players[i].rating, 1)
                    else:
                        players[i].update_rating(players[j].rating, 0.5)
                        players[j].update_rating(players[i].rating, 0.5)

            save_to_csv(players, results)
            ranked_players = ranking(players)
            print("Ranking:")
            for i, player in enumerate(ranked_players):
                print(f"{i+1}. {player.name} - Rating: {player.rating:.2f}")
        elif escolha == "3":
            ranked_players = ranking(players)
            print("Ranking:")
            for i, player in enumerate(ranked_players):
                print(f"{i+1}. {player.name} - Rating: {player.rating:.2f}")
        elif escolha == "4":
            break
        elif escolha == "5":
            for player in players:
                player.rating = 1200
            print("Ranking limpo com sucesso!")
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

