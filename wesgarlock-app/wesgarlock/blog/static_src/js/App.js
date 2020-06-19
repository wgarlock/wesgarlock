import React, { Fragment, Suspense } from 'react'
import { MuiThemeProvider, CssBaseline } from '@material-ui/core'
import theme from '../../../base/static_src/js/theme'
import GlobalStyles from '../../../base/static_src/js/GlobalStyles'
import Pace from '../../../base/static_src/js/components/Pace'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
import Blog from './views/Blog'

library.add(fab)

function App () {
  return (
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        <GlobalStyles />
        <Pace color={theme.palette.primary.light} />
        <Suspense fallback={<Fragment />}>
            <Blog />
        </Suspense>
      </MuiThemeProvider>
  )
}

export default App
