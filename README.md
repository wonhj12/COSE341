# Final Project Proposal COSE341: Operating Systems

## Distributed Cafe Order Processing System Using Operating System Concepts

### Team OSBucks

- 2020320018 Won, Ha Jin (Team Leader)
- 2019320128 Kim, Jin Seo
- 2021320073 Lee, Il Seob
- 2022350021 Kim, Hyeon Gyeong

### Introduction

The purpose of this project is to develop a cafe order processing system that implements core operating system concepts to ensure efficient order management. This project aims to create a system that handles multiple orders concurrently while efficiently managing shared resources through the application of OS principles such as process management, synchronization, and resource allocation.

### Implementation Plan

The system will be developed using Python and will consist of two main components: the order processing system and the user interface. The order processing system will utilize Python's threading library for concurrent processing, while the user interface will be implemented using Streamlit for smooth interaction. Additionally, a shared memory system will be implemented to manage order states and resource allocation.

STEP 1: When a customer inputs a new order, the system creates a new process thread and assigns appropriate resources (coffee machines). The orders are given priority based on FCFS basis, and when multiple menus are ordered at same time, they are given the same priority and are processed in RR manner.

STEP 2: The system manages multiple orders concurrently using process scheduling and synchronization mechanisms. Each menu has data for making time, ingredients, and price.

STEP 3: Shared resources (coffee machines, order data) are managed using semaphores and mutex locks to prevent conflicts.

STEP 4: The system updates order status in real-time through the shared memory system.

### Core OS Concepts Application

1. Process Management

   - Multi-threading for concurrent order processing
   - Priority with RR based scheduling for order management

2. Process Synchronization

   - Semaphores for coffee machine access control
   - Mutex locks for shared data protection

3. Memory Management
   - Shared memory for order status tracking
   - Resource allocation management

### Conclusion

The proposed cafe order processing system addresses the challenges of managing multiple orders and resources in a busy cafe environment by applying operating system concepts. We believe this system will represent a significant step toward achieving efficient and scalable order processing in food service environments.
