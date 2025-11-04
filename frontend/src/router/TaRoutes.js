import TaAssessmentGenerator from '@/components/TA/TaAssesmentGenerator.vue'
import TADashboard from '@/components/TA/TADashboard.vue'
import QueryTracker from '@/components/TA/QueryTracker.vue'
import TaSlideDeckGenerator from '@/components/TA/TaSlideDeckGenerator.vue'

export default [
    { path: 'dashboard', name: 'TaDashboard', component: TADashboard },
    {path: 'query-tracker', name: 'TaQueryTracker', component: QueryTracker},
    { path: 'assessment-generator', name: 'TaAssessmentGenerator', component: TaAssessmentGenerator },
    {path: 'slide-deck-creator', name: 'TaSlideDeckGenerator', component: TaSlideDeckGenerator},
]
