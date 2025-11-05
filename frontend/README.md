# AURA Frontend (Vue + Tailwind)

Multi-role dashboard including Admin, Student, Instructor, and TA panels built with Vue 3 and Tailwind CSS.

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

## 🌐 How to Access Each Dashboard Page

When running the app (`npm run dev`), use these URLs directly in your browser to view each role’s main page:

1. **Admin Dashboard**  
   - `/admin/dashboard`  
   - Shows the full admin overview, metrics, charts, and user management.

2. **Student Home**  
   - `/student/dashboard`  
   - Shows the student homepage, header, new query form, and student tools.

3. **Instructor Dashboard**  
   - `/instructor/dashboard`  
   - Access the instructor’s analytics, reports, and content creation areas.

4. **TA Dashboard**  
   - `/ta/dashboard`  
   - See the TA portal for answering queries, managing sessions, etc.

You can also navigate in-app using the side/navbar, but entering these routes in your browser’s address bar will take you directly where you want to go.

---

**Add this block to the top of your README file.**  
This will help every new user or reviewer instantly access and test each section of your app—no guessing needed. Adjust route names as per your router setup if needed!


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
- All changes can be run/tested locally, just follow the steps above!
- For any new component or feature, see the matching subfolder in `src/components/`.

---

## ⚙️ Troubleshooting

- If `npm install` fails, try deleting `node_modules/` and repeating the command.
- For any missing package error, run `npm install` again.

---

## 📜 License

Academic/educational demo.

---


