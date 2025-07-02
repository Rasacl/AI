const WebSocket = require('ws');

class WebSocketServer {
    constructor(port = 8080) {
        this.port = port; // 保存端口号到实例变量
        this.wss = new WebSocket.Server({ port });
        this.clients = new Map(); // 存储客户端连接
        this.init();
    }

    init() {
        this.wss.on('connection', (ws) => {
            console.log('新客户端连接');
            
            // 为每个客户端生成唯一ID
            const clientId = Date.now().toString();
            this.clients.set(clientId, ws);

            // 处理客户端消息
            ws.on('message', (message) => {
                try {
                    const data = JSON.parse(message);
                    
                    // 处理心跳消息
                    if (data.type === 'ping') {
                        ws.send(JSON.stringify({ type: 'pong' }));
                        return;
                    }
                    
                    console.log('收到消息:', data);
                    // 广播消息给所有客户端
                    this.broadcast(message, ws);
                    
                } catch (e) {
                    // 处理普通文本消息
                    console.log('收到文本消息:', message.toString());
                    this.broadcast(message, ws);
                }
            });

            // 处理连接关闭
            ws.on('close', () => {
                console.log('客户端断开连接');
                this.clients.delete(clientId);
            });

            // 处理错误
            ws.on('error', (error) => {
                console.error('WebSocket错误:', error);
                this.clients.delete(clientId);
            });

            // 发送欢迎消息
            ws.send(JSON.stringify({
                type: 'system',
                message: '连接成功'
            }));
        });

        console.log(`WebSocket服务器运行在 ws://localhost:${this.port}`); // 使用实例变量
    }

    // 广播消息给所有客户端（除了发送者）
    broadcast(message, sender) {
        this.clients.forEach((client) => {
            if (client !== sender && client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    }
}

// 启动服务器
const server = new WebSocketServer();