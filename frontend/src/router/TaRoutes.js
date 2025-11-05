import TaAssessmentGenerator from '@/components/TA/TaAssesmentGenerator.vue'
import TADashboard from '@/components/TA/TADashboard.vue'
import QueryTracker from '@/components/TA/QueryTracker.vue'
import TaSlideDeckGenerator from '@/components/TA/TaSlideDeckGenerator.vue'
import DoubtSummarizer from '../components/TA/DoubtSummarizer.vue'
import OnboardingMentor from '../components/TA/OnboardingMentor.vue'
import TaResourseshub from '@/components/TA/TaResourses_hub.vue'
import TaProfile from '../components/TA/TaProfile.vue'


export default [
    { path: 'dashboard', name: 'TaDashboard', component: TADashboard },
    {path: 'query-tracker', name: 'TaQueryTracker', component: QueryTracker},
    { path: 'assessment-generator', name: 'TaAssessmentGenerator', component: TaAssessmentGenerator },
    {path: 'slide-deck-creator', name: 'TaSlideDeckGenerator', component: TaSlideDeckGenerator},
    { path: 'doubt-summarizer', name: 'DoubtSummarizer', component: DoubtSummarizer },
    { path: 'onboarding-mentor', name: 'OnboardingMentor', component: OnboardingMentor },
    { path: 'resource', name: 'TaResoursesHub', component: TaResourseshub }, 
    { path: 'profile', name: 'TaProfile', component: TaProfile },

]
