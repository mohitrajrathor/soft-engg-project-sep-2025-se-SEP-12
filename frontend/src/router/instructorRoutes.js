import InstructorAssessmentGenerator from '../components/instructor/InstructorAssessmentGenerator.vue'
import InstructorDiscussionSummaries from '../components/instructor/InstructorDiscussionSummaries.vue'
import InstructorSlideGenerator from '../components/instructor/InstructorSlideGenerator.vue'
import InstructorProfile from '../components/instructor/InstructorProfile.vue'

export default {
  path: '/instructor',
  children: [
    { path: 'assessment-generator', name: 'InstructorAssessmentGenerator', component: InstructorAssessmentGenerator },
    { path: 'discussion-summaries', name: 'InstructorDiscussionSummaries', component: InstructorDiscussionSummaries },
    { path: 'slide-generator', name: 'InstructorSlideGenerator', component: InstructorSlideGenerator},
    { path: 'profile', name: 'InstructorProfile', component: InstructorProfile },
    
  ],
}
