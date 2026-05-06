# LINKEDIN.md

## LinkedIn Post Text

Today I completed a real-time polling application using FastAPI and WebSockets.

In this project, users can create polls and vote in real time. The most important part was making sure that multiple browser tabs update instantly without refreshing the page. I used WebSockets to keep a continuous connection between the client and the server.

One challenge I faced was making different tabs connect to the same poll correctly. At first, every tab was creating a new poll instead of sharing the same one. I fixed this by using the poll ID inside the URL and reconnecting all clients to the same WebSocket endpoint.

I also implemented REST API endpoints, Docker support, and a simple real-time frontend for testing.

This project helped me better understand the difference between REST APIs and WebSocket communication in backend development.

GitHub: https://github.com/ahmettsnl/fastapi-journey/tree/asenel-mini-project-4

#FastAPI #WebSockets #BackendDevelopment #Python #100DaysOfCode

---

## Public LinkedIn URL

https://www.linkedin.com/posts/ahmet0senel_fastapi-websockets-backenddevelopment-share-7457745217669201920-hLeN