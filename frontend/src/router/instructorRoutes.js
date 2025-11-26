import InstructorAssessmentGenerator from '../components/instructor/InstructorAssessmentGenerator.vue'
import InstructorDashboard from '../components/instructor/InstructorDashboard.vue'
import InstructorDiscussionSummaries from '../components/instructor/InstructorDiscussionSummaries.vue'
import InstructorSlideGenerator from '../components/instructor/InstructorSlideGenerator.vue'
import InstructorProfile from '../components/instructor/InstructorProfile.vue'
import QuizList from '../components/instructor/QuizList.vue'
import QuizDetail from '../components/instructor/QuizDetail.vue'

export default {
  path: '/instructor',
  children: [
    { path: 'dashboard', name : 'InstructorDashboard', component : InstructorDashboard},
    { path: 'assessment-generator', name: 'InstructorAssessmentGenerator', component: InstructorAssessmentGenerator },
    { path: 'discussion-summaries', name: 'InstructorDiscussionSummaries', component: InstructorDiscussionSummaries },
    { path: 'slide-generator', name: 'InstructorSlideGenerator', component: InstructorSlideGenerator},
    { path: 'profile', name: 'InstructorProfile', component: InstructorProfile },
    {path: 'quizzes', name: 'QuizList', component: QuizList},
    {path:'quizzes/:id', name: 'QuizDetail', component: QuizDetail},
    
  ],
}
