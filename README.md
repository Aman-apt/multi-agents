# 🧠 Research Agent System

This project demonstrates a **simple research agent architecture** composed of multiple interconnected parts working together to complete a given task.  
Several specialized agents run **in parallel**, each focusing on a specific responsibility within the workflow.

---

## 🔹 Overview

The system consists of three main graphs (or teams), each handling a distinct stage of the process:

---

### **1. Research Team**
📊 Helps perform research and scrape web pages.  
This team contains multiple nodes responsible for collecting and processing data from online sources.

![Research Team Graph](./first_graph.png)

---

### **2. Documentation Team**
📝 Focuses on writing, editing, and updating documentation based on the supervisor’s input, which originates from the research team’s findings.

![Documentation Team Graph](./lang.png)

---

### **3. Supervisor (Final Graph)**
🧩 Manages and coordinates the entire workflow.  
The supervisor combines all nodes and organizes them into two logical teams that work together efficiently to complete the overall task.

![Supervisor Graph](./new_lang.png)

---
Thank's for your visit. In future i will be building more useful and complex projects.
