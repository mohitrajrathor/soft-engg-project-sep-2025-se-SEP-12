import AssessmentWorkspace from '@/components/shared/assessment/AssessmentWorkspace.vue'
import TADashboard from '@/components/TA/TADashboard.vue'
import QueryTracker from '@/components/TA/QueryTracker.vue'
import SlideDeckWorkspace from '@/components/shared/slideDeck/SlideDeckWorkspace.vue'
import SlideDeckViewer from '@/components/shared/slideDeck/SlideDeckViewer.vue'
import SlideDeckDetail from '@/components/shared/slideDeck/SlideDeckDetail.vue'
import SlideDeckEdit from '@/components/shared/slideDeck/SlideDeckEdit.vue'
import DoubtSummarizer from '../components/TA/DoubtSummarizer.vue'
import OnboardingMentor from '../components/TA/OnboardingMentor.vue'
import TaResourseshub from '@/components/TA/TaResourses_hub.vue'
import TaProfile from '../components/TA/TaProfile.vue'
import QuizDetails from '@/components/shared/assessment/QuizDetail.vue'
import QuizList from '@/components/shared/assessment/QuizList.vue'


export default [
    { path: 'dashboard', name: 'TaDashboard', component: TADashboard },
    {path: 'query-tracker', name: 'TaQueryTracker', component: QueryTracker},
    { path: 'assessment-generator', name: 'TaAssessmentWorkspace', component: AssessmentWorkspace, props: () => ({ role:'ta' }) },
    { path: 'quiz-list', name: 'TaQuizList', component: QuizList, props: () => ({ role:'ta' }) },
    { path: 'quiz-details/:id', name: 'TaQuizDetails', component: QuizDetails, props: (route) => ({ role:'ta', id: route.params.id }) },
    { path: 'slide-deck-creator', name: 'TaSlideDeckWorkspace', component: SlideDeckWorkspace, props: () => ({ role:'ta' })},
    { path: 'slide-decks', name: 'TaSlideDeckViewer', component: SlideDeckViewer, props: () => ({ role:'ta' })},
    { path: 'slide-deck/:id', name: 'TaSlideDeckDetail', component: SlideDeckDetail, props: (route) => ({ role:'ta', id: route.params.id })},
    { path: 'slide-deck/:id/edit', name: 'TaSlideDeckEdit', component: SlideDeckEdit, props: (route) => ({ role:'ta', id: route.params.id })},
    { path: 'doubt-summarizer', name: 'DoubtSummarizer', component: DoubtSummarizer },
    { path: 'onboarding-mentor', name: 'OnboardingMentor', component: OnboardingMentor },
    { path: 'resource', name: 'TaResoursesHub', component: TaResourseshub }, 
    { path: 'profile', name: 'TaProfile', component: TaProfile },

]
