---
name: websockets-realtime-ops
description: Real-time WebSocket architectures, reconnection strategies, heartbeat mechanisms, and pub/sub scaling.
license: MIT
compatibility: opencode
---

# WebSockets & Real-Time Architecture

Standards for reliable, bidirectional real-time communications.

## Resilience Architecture
1. **Heartbeat / Ping-Pong**: Implement periodic keep-alive pings to detect half-open connections.
2. **Exponential Backoff Reconnect**: Clients must reconnect with randomized jitter to avoid Thundering Herd on server restarts.
3. **Message Acknowledgements**: Use message sequence IDs and ACK frames to guarantee delivery.
4. **Horizontal Scaling**: Use Redis Pub/Sub or Socket.io Redis adapter to broadcast events across multiple server nodes.
