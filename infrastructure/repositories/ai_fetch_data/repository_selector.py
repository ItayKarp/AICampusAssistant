class AIRepositorySelector:
    def __init__(self, repositories_map: dict):
        self.repositories_map = repositories_map

    def get_repository(self, category: str):
        repository = self.repositories_map.get(category)
        if repository is None:
            raise ValueError(f"Invalid category: {category}")
        return repository
