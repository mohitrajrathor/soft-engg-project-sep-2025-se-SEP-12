import StudentDashboard from '../components/student/StudentDashboard.vue'
import StudentQueries from '../components/student/studentQueries.vue'
import StudentResource from '../components/student/StudentResource.vue'
import AIassistant from '../components/student/studentAIAssistance.vue'
import StudentMyQuery from '../components/student/StudentNewQuery.vue'
import StudyBreak from '../components/student/StudyBreak.vue'
import Profile from '../components/student/Profile.vue'
import StudentSummary from '../components/student/StudentSummary.vue'

export default [
  { path: 'dashboard', name: 'StudentDashboard', component: StudentDashboard },
  { path: 'queries', name: 'StudentQueries', component: StudentQueries },
  { path: 'resources', name: 'StudentResource', component: StudentResource },
  { path: 'AI-assistant', name: 'StudentAIAssistant', component: AIassistant },
  { path: 'my-query', name: 'StudentMyQuery', component: StudentMyQuery },
  { path: 'new-query', name: 'StudentNewQuery', component: StudentMyQuery },
  { path: 'study-break', name: 'StudyBreak', component: StudyBreak },
  { path: 'Profile', name: 'StudentProfile', component: Profile },
  { path: 'summary', name: 'StudentSummary ', component: StudentSummary },
]
