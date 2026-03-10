from typing import Any


class RepositoryResponseBuilder:
    @staticmethod
    def success(*,category: str,table: str,results: list[dict[str, Any]],applied_filters: dict[str, Any] | None = None,message: str = "Results found.",) -> dict[str, Any]:
        return {
            "success": True,
            "category": category,
            "table": table,
            "applied_filters": applied_filters or {},
            "results_count": len(results),
            "results": results,
            "message": message,
        }

    @staticmethod
    def empty(*,category: str,table: str,applied_filters: dict[str, Any] | None = None,message: str = "No matching results found.",) -> dict[str, Any]:
        return {
            "success": True,
            "category": category,
            "table": table,
            "applied_filters": applied_filters or {},
            "results_count": 0,
            "results": [],
            "message": message,
        }

    @staticmethod
    def error(*,category: str,table: str,message: str,applied_filters: dict[str, Any] | None = None,) -> dict[str, Any]:
        return {
            "success": False,
            "category": category,
            "table": table,
            "applied_filters": applied_filters or {},
            "results_count": 0,
            "results": [],
            "message": message,
        }