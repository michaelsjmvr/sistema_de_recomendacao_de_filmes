import sys
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QListWidget, QComboBox

# Classe que define a interface do aplicativo
class MovieRecommendationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.setWindowTitle("Sistema de Recomendação de Filmes")
        self.setGeometry(100, 100, 600, 400)

        # Configuração do widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout vertical para organizar widgets
        self.layout = QVBoxLayout()

        # Rótulo para a seleção de gênero
        self.label_genre = QLabel("Selecione o Gênero:")
        self.layout.addWidget(self.label_genre)

        # Dropdown para selecionar o gênero
        self.combo_genre = QComboBox()
        self.combo_genre.addItem("Ação")
        self.combo_genre.addItem("Comédia")
        self.combo_genre.addItem("Drama")
        self.layout.addWidget(self.combo_genre)

        # Rótulo para as recomendações
        self.label_recommendations = QLabel("Filmes Recomendados:")
        self.layout.addWidget(self.label_recommendations)

        # Lista para exibir os filmes recomendados
        self.movie_list = QListWidget()
        self.layout.addWidget(self.movie_list)

        # Botão para recomendar filmes
        self.button_recommend = QPushButton("Recomendar Filmes")
        self.layout.addWidget(self.button_recommend)

        # Conectar o botão a uma função de recomendação
        self.button_recommend.clicked.connect(self.recommend_movies)

        # Configurar o layout no widget central
        self.central_widget.setLayout(self.layout)

    # Função para recomendar filmes com base no gênero selecionado
    def recommend_movies(self):
        genre = self.combo_genre.currentText()

        # Configurar a chave da API e fazer a chamada para obter os filmes
        api_key = 'sua_api_key_aqui'  # Substitua pela sua chave da API do TMDb
        url = f'https://api.themoviedb.org/3/discover/movie'
        params = {
            'api_key': api_key,
            'with_genres': self.get_genre_id(genre),
            'sort_by': 'popularity.desc',
            'page': 1
        }

        try:
            # Fazer uma solicitação GET para a API do TMDb
            response = requests.get(url, params=params)
            data = response.json()
            movies = data.get('results', [])

            # Limpar a lista de filmes e exibir os 5 filmes recomendados
            self.movie_list.clear()
            for movie in movies[:5]:
                self.movie_list.addItem(movie['title'])
        except Exception as e:
            print(e)

    # Função para obter o ID do gênero com base no nome do gênero
    def get_genre_id(self, genre_name):
        # Mapeamento de nomes de gêneros para IDs de gêneros do TMDb
        genre_mapping = {
            "Ação": 28,
            "Comédia": 35,
            "Drama": 18
            # Adicione outros gêneros conforme necessário
        }

        return genre_mapping.get(genre_name, 28)  # Gênero padrão é "Ação"

# Função principal que inicia o aplicativo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieRecommendationApp()
    window.show()
    sys.exit(app.exec())
