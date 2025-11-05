# AURA Frontend (Vue + Tailwind)

Multi-role dashboard—including Admin, Student, Instructor, and TA panels—built with Vue 3 and Tailwind CSS.

---

## 🚦 Quick Setup & Run Guide

1. **Get the Project**
   - **Clone (Recommended):**
     ```
     git clone https://github.com/mohitrajrathor/soft-engg-project-sep-2025-se-SEP-12.git
     cd soft-engg-project-sep-2025-se-SEP-12/frontend
     ```
   - **OR, Download as zip:**  
      - Click "Code" → "Download ZIP" on the repo front page.
      - Extract the zip.
      - Open the `frontend` folder in any code editor.

2. **Install Dependencies**
   npm install
- (Node.js v16+ recommended. Get it from [nodejs.org](https://nodejs.org/).)

3. **Start the App Locally**
   npm run dev
- Open the given local URL (often `http://localhost:5173`) to explore in your browser.

---

## 🧑‍💻 Project Tour (Where to Look)

- **Admin Dashboard:**  
`src/components/Admin/`  
Everything for admin analytics, user management, and charts.
- **Student Features:**  
`src/components/student/`
- **Instructor Tools:**  
`src/components/instructor/`
- **TA Section:**  
`src/components/TA/`
- **Routing:**  
`src/router/` — Main navigation, admin, student, and instructor route files.
- **Styling:**  
Tailwind classes are used in all `.vue` components.

---

## 🗂️ Key Files and Structure (For Review)

- `frontend/src/components/Admin/AdminDashboard.vue` (core admin UI)
- `frontend/src/components/Admin/FAQAnalyticsChart.vue` (charts)
- `frontend/src/router/adminRoutes.js`, `studentRoutes.js`, `index.js` (all route definitions)
- All project structure can be browsed within the `src/components/` and `src/router/` folders.

---

## 📝 Contributing/Modifying

- Edit any component in its folder and save.
- To add features, follow the existing folder/component pattern.
- After code changes:

git add .
git commit -m "Describe your edit"
git pull origin main # Always pull before pushing!
git push origin main


---

## 🧐 Reviewer Notes

- No authentication or backend connection required to preview the dashboard UI/features.
- All changes can be run/tested locally—just follow the steps above!
- For any new component or feature, see the matching subfolder in `src/components/`.

---

## ⚙️ Troubleshooting

- If `npm install` fails, try deleting `node_modules/` and repeating the command.
- For any missing package error, run `npm install` again.

---

## 📜 License

Academic/educational demo.

---


