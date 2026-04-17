# OBSERVATIONS.md

## 1. Image Size
The alpine:3.19 image is very small (around 8MB). This is because Alpine Linux is a minimal distribution designed for containers, so it includes only essential packages and avoids unnecessary components.

## 2. Image Layers
The image has 2 layers. One layer is the base Alpine filesystem (alpine-minirootfs), and the other is a small configuration layer. The largest layer contains the main operating system files.

## 3. OS and Architecture
From the docker inspect command:
- OS: linux
- Architecture: amd64

This means the container runs a Linux-based system on a 64-bit architecture.

## 4. Alpine-specific Observation
Inside the container, I installed curl using apk add curl, and it worked successfully. However, after exiting the container and starting a new one, curl was no longer installed. This is because containers are ephemeral by default — any changes made inside a container are lost unless the container is saved or committed.

## 5. What surprised me
What surprised me the most is how lightweight the Alpine image is and how fast it runs. Also, I found it interesting that changes inside the container do not persist after it stops, which shows how Docker containers are isolated and temporary by nature.