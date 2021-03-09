class GameStats():
    """Класс для статистики"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.get_record_from_file()


    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_record_from_file(self):
        try:
            with open(self.settings.record_file, encoding='utf-8') as f:
                record = f.read()
        except FileNotFoundError:
            print('There is no ' + self.settings.record_file + ' file!')

        if not record:
            record = 0

        return round(int(record))

    def set_record_to_file(self, record):
        try:
            with open(self.settings.record_file, 'w') as f:
                f.write(str(record))
        except FileNotFoundError:
            print('There is no ' + self.settings.record_file + ' file!')
