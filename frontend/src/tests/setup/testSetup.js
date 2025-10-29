import { config } from '@vue/test-utils'

// Example: globally stub Vue components or plugins
config.global.stubs = {
  FontAwesomeIcon: true,
}
