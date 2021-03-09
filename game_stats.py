class GameStats():
    """Класс для статистики"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.record = self.get_record_from_file()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def get_record_from_file(self):
        record = 0

        try:
            with open(self.settings.record_file, encoding='utf-8') as f:
                record = f.read()
        except FileNotFoundError:
            print('There is no ' + self.settings.record_file + ' file!')

        return round(int(record))

    def set_record_to_file(self, new_record):
        if self.record < new_record:
            try:
                with open(self.settings.record_file, 'w') as f:
                    f.write(str(new_record))
            except FileNotFoundError:
                print('There is no ' + self.settings.record_file + ' file!')
