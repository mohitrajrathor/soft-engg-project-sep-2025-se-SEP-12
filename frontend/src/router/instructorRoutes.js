import AssessmentWorkspace from '../components/shared/assessment/AssessmentWorkspace.vue'
import InstructorDashboard from '../components/instructor/InstructorDashboard.vue'
import InstructorDiscussionSummaries from '../components/instructor/InstructorDiscussionSummaries.vue'
import SlideDeckWorkspace from '../components/shared/slideDeck/SlideDeckWorkspace.vue'
import InstructorProfile from '../components/instructor/InstructorProfile.vue'
import QuizDetails from '../components/shared/assessment/QuizDetail.vue'
import QuizList from '../components/shared/assessment/QuizList.vue'
import SlideDeckViewer from '../components/shared/slideDeck/SlideDeckViewer.vue'
import SlideDeckDetail from '../components/shared/slideDeck/SlideDeckDetail.vue'
import SlideDeckEdit from '../components/shared/slideDeck/SlideDeckEdit.vue'

export default {
  path: '/instructor',
  children: [
    { path: 'dashboard', name : 'InstructorDashboard', component : InstructorDashboard},
    { path: 'assessment-generator', name: 'InstructorAssessmentWorkspace', component: AssessmentWorkspace, props: () => ({ role:'instructor' }) },
    { path: 'discussion-summaries', name: 'InstructorDiscussionSummaries', component: InstructorDiscussionSummaries },
    { path: 'slide-deck-generator', name: 'InstructorSlideDeckWorkspace', component: SlideDeckWorkspace, props: () => ({ role:'instructor' })},
    { path: 'slide-decks', name: 'SlideDeckViewer', component: SlideDeckViewer, props: () => ({ role:'instructor' }) },
    { path: 'slide-deck/:id', name: 'SlideDeckDetail', component: SlideDeckDetail, props: (route) => ({ role:'instructor', id: route.params.id }) },
    { path: 'slide-deck/:id/edit', name: 'SlideDeckEdit', component: SlideDeckEdit, props: (route) => ({ role:'instructor', id: route.params.id }) },
    { path: 'quiz-list', name: 'QuizList', component: QuizList, props: () => ({ role:'instructor' }) },
    { path: 'quiz-details/:id', name: 'QuizDetails', component: QuizDetails, props: (route) => ({ role:'instructor', id: route.params.id }) },
    { path: 'profile', name: 'InstructorProfile', component: InstructorProfile },
  ],
}
