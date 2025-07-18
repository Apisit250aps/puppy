from rest_framework.response import Response
from typing import Any, Optional


class ApiResponse:
    @staticmethod
    def json(
        message: str, success: bool, data: Optional[Any] = None, status: int = 200
    ):
        return Response(
            {
                "message": message,
                "success": success,
                "data": data,
            },
            status=status,
        )
