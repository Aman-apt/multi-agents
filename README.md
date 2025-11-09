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

<img width="397" height="249" alt="first_graph" src="https://github.com/user-attachments/assets/04eb72ee-0aa8-4f91-8827-754722881a04" />


---

### **2. Documentation Team**
📝 Focuses on writing, editing, and updating documentation based on the supervisor’s input, which originates from the research team’s findings.

<img width="612" height="249" alt="lang" src="https://github.com/user-attachments/assets/ff8f423b-fe7a-4c59-aa49-af4a760068a5" />


---

### **3. Supervisor (Final Graph)**
🧩 Manages and coordinates the entire workflow.  
The supervisor combines all nodes and organizes them into two logical teams that work together efficiently to complete the overall task.

<img width="462" height="249" alt="new_lang" src="https://github.com/user-attachments/assets/e3a72d65-6a2c-4cbf-bbf4-4ab866fd22ea" />


---
Thank's for your visit. In future i will be building more useful and complex projects.
