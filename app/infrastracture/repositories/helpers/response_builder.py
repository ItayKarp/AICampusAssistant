class RepositoryResponseBuilder:
    @staticmethod
    def empty(message: str = "No matching records found.") -> dict:
        return {
            "count": 0,
            "results": [],
            "message": message,
        }

    @staticmethod
    def success(results: list[dict], empty_message: str = "No matching records found.") -> dict:
        return {
            "count": len(results),
            "results": results,
            "message": None if results else empty_message,
        }