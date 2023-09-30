from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from watch2gether import experimental_logger as logger
from watch2gether.experimental.core.websockets import ConnectionManager


router = APIRouter()
manager = ConnectionManager()  # 实例化WebSocket连接管理器.


@router.websocket('/experimental/ws/{client_id}/')
async def create_websocket_endpoint(client_id: int, websocket: WebSocket):
    """创建WebSocket服务.

    Args:
        client_id: int,
            WebSocket客户端ID.
        websocket: WebSocket,
            WebSocket实例.
    """
    # 首先进行客户端ID校验.
    if client_id in manager.active_connections:
        await websocket.close(code=1008,  # Policy Violation.
                              reason='具有相同ID的客户端已存在, 连接被拒绝!')

        logger.warning(f'客户端({websocket.client.host}:{websocket.client.port})'
                       f'试图以已存在客户端ID#{client_id}连接被拒!')
    else:
        await manager.connect(client_id, websocket)

        try:
            # 接收并转发数据.
            data = await websocket.receive_json()  # noqa: F841
        except WebSocketDisconnect:
            manager.disconnect(client_id)
