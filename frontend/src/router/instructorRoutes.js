import InstructorAssessmentGenerator from '../components/instructor/InstructorAssessmentGenerator.vue'
import InstructorDashboard from '../components/instructor/InstructorDashboard.vue'
import InstructorDiscussionSummaries from '../components/instructor/InstructorDiscussionSummaries.vue'
// import InstructorDashboard from '../components/instructor/InstructorDashboard.vue'
import InstructorSlideGenerator from '../components/instructor/InstructorSlideGenerator.vue'

export default {
  path: '/instructor',
  children: [
    { path: 'dashboard', name : 'InstructorDashboard', component : InstructorDashboard},
    { path: 'assessment-generator', name: 'InstructorAssessmentGenerator', component: InstructorAssessmentGenerator },
    { path: 'discussion-summaries', name: 'InstructorDiscussionSummaries', component: InstructorDiscussionSummaries },
    {path: 'slide-generator', name: 'InstructorSlideGenerator', component: InstructorSlideGenerator},
  ],
}
