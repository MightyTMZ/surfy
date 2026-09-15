# Surfy and the Infinity Gauntlet Skill

> *Snap out of the prompt loop.* 🫰
<img width="413" height="483" alt="image" src="https://github.com/user-attachments/assets/99d4ce0d-0946-4b02-8ccc-c12a4e5560ed" />

---

### **Problem**
When Claude or Codex repeatedly grills you with clarifying questions on an idea, answering them feels like a chore with little to no reward at the end.

### **Goal**
Build an easily installable skill that turns this grilling process into an interactive, rewarding experience.

---

### **Implementation Plan**

1. **Fork & Integrate:**  
   Fork a "grill me" skill (or close equivalent) and modify it to trigger Surfy once full clarity and context are achieved.

2. **Handoff Prompt:**  
   Display a completion message such as:  
   > *"Great! I have all the context I need. Time to snap your Infinity Gauntlet so I can start building!"*

3. **Launch Surfy:**  
   Prompt the user to launch the Surfy software (an OpenCV script powered by Google MediaPipe).

4. **Camera Setup & Fallback:**  
   Prompt the user to open their webcam. If they cannot or prefer not to use a camera, launch a local desktop GUI featuring an on-screen button to click and trigger the snap.

5. **The Snap:**  
   The user snaps their fingers on camera (detected via Google MediaPipe) or clicks the Gauntlet button in the GUI—and the automated workflow begins!

6. **Reset / State:**  
   For subsequent prompts, Claude will hide the Infinity Stones unless another grilling sequence is triggered.

---

### **UI / UX Requirements**

* **CLI Progress Bar:**  
  Display a "rounded-down" Infinity Gauntlet progress bar in the CLI output for each response during the grilling phase.  
  <img width="1919" height="1035" alt="screen1" src="https://github.com/user-attachments/assets/f4093e7c-4b72-44e2-82a2-df08eeafcc5c" />

* **CLI Only:**  
  The Infinity Gauntlet progress visualization must be rendered strictly in the CLI (no browser/web implementation).
  <img width="1911" height="1021" alt="screen2" src="https://github.com/user-attachments/assets/cdc6c478-8e68-4503-93ab-4906a1945762" />

* **Dynamic Scope:**  
  If Claude or Codex decides to extend the required context scope mid-conversation for extra clarity, the Infinity Stone progress will recalculate or reset accordingly.
